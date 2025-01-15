<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" type="primary" plain class="back-button">
          <el-icon><Back /></el-icon> 返回
        </el-button>
        <h2>我的购物车</h2>
      </div>
    </div>

    <div class="content-container">
      <el-card class="cart-card" v-if="cartItems.length">
        <el-table
          :data="cartItems"
          style="width: 100%"
          @selection-change="handleSelectionChange"
          :header-cell-style="{ background: '#f5f7fa' }"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column label="商品信息" min-width="400">
            <template #default="{ row }">
              <div class="product-info">
                <el-image
                  :src="`http://localhost:11000/api/image/${row.image_id}`"
                  fit="cover"
                  class="product-image"
                  :preview-src-list="[`http://localhost:11000/api/image/${row.image_id}`]"
                >
                  <template #error>
                    <div class="image-error">
                      <el-icon><Picture /></el-icon>
                    </div>
                  </template>
                </el-image>
                <div class="product-detail">
                  <div class="product-name">{{ row.name }}</div>
                  <div class="product-price">￥{{ row.price }}</div>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="数量" width="200" align="center">
            <template #default="{ row }">
              <el-input-number 
                v-model="row.quantity" 
                :min="1" 
                :max="row.maxQuantity"
                @change="updateTotalPrice(row)"
                size="small"
                controls-position="right"
              />
            </template>
          </el-table-column>
          <el-table-column label="小计" width="150" align="right">
            <template #default="{ row }">
              <span class="total-price">￥{{ row.totalPrice }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" align="center">
            <template #default="{ row }">
              <el-button 
                type="primary" 
                link
                @click="viewItemDetail(row.name)"
              >
                <el-icon><View /></el-icon>
                查看详情
              </el-button>
              <el-button 
                type="danger" 
                link
                @click="removeFromCart(row)"
              >
                <el-icon><Delete /></el-icon>
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="cart-footer">
          <div class="selected-info">
            已选择 <span class="highlight">{{ selectedItems.length }}</span> 件商品
            <span class="divider">|</span>
            合计：<span class="total-amount">￥{{ totalAmount }}</span>
          </div>
          <el-button 
            type="primary" 
            :disabled="!selectedItems.length"
            @click="pay"
          >
            <el-icon><ShoppingCartFull /></el-icon>
            结算
          </el-button>
        </div>
      </el-card>

      <el-empty 
        v-else 
        description="购物车是空的" 
        :image-size="200"
      >
        <el-button type="primary" @click="goToShopping">
          去购物
        </el-button>
      </el-empty>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import { 
  Back,
  Picture,
  View,
  Delete,
  ShoppingCartFull
} from '@element-plus/icons-vue'

export default {
  name: 'Cart',
  components: {
    Back,
    Picture,
    View,
    Delete,
    ShoppingCartFull
  },
  setup() {
    const router = useRouter();
    const cartItems = ref([]);
    const selectedItems = ref([]);

    onMounted(async () => {
      const userStr = localStorage.getItem('user');
      if (userStr) {
        const user = JSON.parse(userStr);
        try {
          const response = await axios.get(`http://localhost:11000/api/shopping/${user.username}`);
          const items = response.data;
          for (const item of items) {
            const pictureResponse = await axios.get(`http://localhost:11000/api/picture/${item.image_id}`);
            item.maxQuantity = pictureResponse.data.num;
            item.quantity = 1;
            item.totalPrice = item.price;
          }
          cartItems.value = items;
        } catch (error) {
          console.error('获取购物车失败:', error);
        }
      }
    });

    const updateTotalPrice = (item) => {
      if (item.quantity > item.maxQuantity) {
        ElMessage.error('商品数量不够');
        item.quantity = item.maxQuantity;
      }
      item.totalPrice = item.price * item.quantity;
    };

    const removeFromCart = async (item) => {
      const userStr = localStorage.getItem('user');
      if (userStr) {
        const user = JSON.parse(userStr);
        try {
          await axios.delete(`http://localhost:11000/api/shopping/${item.image_id}`, {
            params: { username: user.username }
          });
          cartItems.value = cartItems.value.filter(cartItem => cartItem.image_id !== item.image_id);
          ElMessage.success('商品已从购物车中删除');
        } catch (error) {
          console.error('删除购物车商品失败:', error);
          ElMessage.error('删除购物车商品失败');
        }
      }
    };

    const pay = async () => {
      try {
        const userStr = localStorage.getItem('user');
        if (userStr) {
          const user = JSON.parse(userStr);
          const selectedItemsData = selectedItems.value.map(item => ({
            image_id: item.image_id,
            username: user.username,
            quantity: item.quantity,
            name: item.name,
            price: item.price,
            produce: item.produce,
          }));
          await axios.post('http://localhost:11000/api/pay', { selected_items: selectedItemsData });
          cartItems.value = cartItems.value.filter(cartItem => !selectedItems.value.includes(cartItem));
          ElMessage.success('付款成功');
        }
      } catch (error) {
        console.error('付款失败:', error);
        ElMessage.error('付款失败');
      }
    };

    const goBack = () => {
      router.push('/Shouye');
    };

    const handleSelectionChange = (val) => {
      selectedItems.value = val;
    };

    const totalAmount = computed(() => {
      return selectedItems.value.reduce((sum, item) => sum + item.totalPrice, 0);
    });

    const viewItemDetail = (name) => {
      router.push({ name: 'ItemDetail', params: { name } });
    };

    const goToShopping = () => {
      router.push('/Shouye')
    }

    return {
      cartItems,
      selectedItems,
      updateTotalPrice,
      removeFromCart,
      pay,
      goBack,
      handleSelectionChange,
      totalAmount,
      viewItemDetail,
      goToShopping
    };
  }
};
</script>

<style scoped>
.page-container {
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.back-button {
  padding: 8px 15px;
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 500;
}

.cart-card {
  background: #fff;
  border-radius: 8px;
}

.product-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.product-image {
  width: 80px;
  height: 80px;
  border-radius: 4px;
}

.image-error {
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f4f9ff;
  color: #909399;
  font-size: 24px;
  border-radius: 4px;
}

.product-detail {
  flex: 1;
}

.product-name {
  font-size: 14px;
  color: #303133;
  margin-bottom: 8px;
}

.product-price {
  color: #ff4500;
  font-weight: bold;
}

.total-price {
  color: #ff4500;
  font-weight: bold;
  font-size: 16px;
}

.cart-footer {
  margin-top: 20px;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #ebeef5;
}

.selected-info {
  font-size: 14px;
  color: #606266;
}

.highlight {
  color: #409EFF;
  font-weight: bold;
}

.divider {
  margin: 0 10px;
  color: #dcdfe6;
}

.total-amount {
  color: #ff4500;
  font-size: 20px;
  font-weight: bold;
}

:deep(.el-table__header) {
  background-color: #f5f7fa;
}

:deep(.el-table) {
  --el-table-border-color: #ebeef5;
  --el-table-header-background-color: #f5f7fa;
}

@media (max-width: 768px) {
  .page-container {
    padding: 10px;
  }
  
  .product-info {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>