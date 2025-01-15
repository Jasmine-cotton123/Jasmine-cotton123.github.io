<template>
  <div class="view-stock-container">
    <div class="page-header">
      <el-button @click="goBack" type="primary" plain class="back-button">
        <el-icon><Back /></el-icon> 返回
      </el-button>
      <h2>售罄商品</h2>
    </div>

    <el-card class="stock-card">
      <div class="toolbar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索商品名称"
          class="search-input"
          :prefix-icon="Search"
        />
        
        <el-select
          v-model="sortKey"
          placeholder="选择排序方式"
          class="sort-select"
        >
          <el-option label="商品名称" value="name" />
          <el-option label="数量" value="num" />
          <el-option label="单价" value="price" />
          <el-option label="收藏人数" value="favorite" />
          <el-option label="购物车人数" value="cart" />
          <el-option label="购买数量" value="purchased" />
        </el-select>
      </div>

      <el-table
        :data="filteredProducts"
        style="width: 100%"
        height="calc(100vh - 280px)"
        :header-cell-style="{ background: '#f5f7fa' }"
        @sort-change="handleSortChange"
      >
        <el-table-column prop="name" label="商品名称" min-width="120" sortable="custom" />
        <el-table-column label="商品图片" min-width="120" align="center">
          <template #default="{ row }">
            <el-image
              :src="row.src"
              :preview-src-list="[row.src]"
              fit="cover"
              class="product-image"
            >
              <template #error>
                <div class="image-error">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>
          </template>
        </el-table-column>
        <el-table-column prop="num" label="数量" min-width="80" sortable="custom" align="center" />
        <el-table-column prop="price" label="单价" min-width="100" sortable="custom" align="center">
          <template #default="{ row }">
            <span class="price">￥{{ formatPrice(row.price) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="label" label="标签" min-width="100">
          <template #default="{ row }">
            <el-tag size="small" type="danger">{{ row.label }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="favorite" label="收藏人数" min-width="100" sortable="custom" align="center" />
        <el-table-column prop="cart" label="购物车人数" min-width="100" sortable="custom" align="center" />
        <el-table-column prop="purchased" label="购买数量" min-width="100" sortable="custom" align="center" />
        <el-table-column prop="produce" label="介绍" min-width="200" show-overflow-tooltip />
        
        <el-table-column v-if="user && user.role !== 'manager'" label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="editProduct(row.name)">
              <el-icon><Edit /></el-icon>修改
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { 
  Back, 
  Search, 
  Picture, 
  Edit 
} from '@element-plus/icons-vue'

export default {
  name: 'SoldOut',
  components: {
    Back,
    Search,
    Picture,
    Edit
  },
  setup() {
    const router = useRouter();
    const user = ref(null);
    const soldOutProducts = ref([]);
    const sortKey = ref('name');
    const sortOrder = ref('ascending');
    const searchQuery = ref('');

    const fetchSoldOutProducts = async () => {
      try {
        const response = await axios.get('http://localhost:11000/api/sold-out-products');
        soldOutProducts.value = response.data;
      } catch (error) {
        console.error('获取售罄商品错误:', error);
      }
    };

    onMounted(() => {
      const userStr = localStorage.getItem('user');
      if (userStr) {
        user.value = JSON.parse(userStr);
      } else {
        router.push('/login');
      }
      fetchSoldOutProducts();
    });

    const goBack = () => {
      router.push('/Shouye');
    };

    const handleSortChange = ({ prop, order }) => {
      sortKey.value = prop;
      sortOrder.value = order === 'ascending' ? 'asc' : 'desc';
    };

    const sortedProducts = computed(() => {
      return [...soldOutProducts.value].sort((a, b) => {
        if (sortKey.value === 'price' || sortKey.value === 'num') {
          return sortOrder.value === 'asc' ? a[sortKey.value] - b[sortKey.value] : b[sortKey.value] - a[sortKey.value];
        } else {
          return sortOrder.value === 'asc' ? a[sortKey.value].localeCompare(b[sortKey.value]) : b[sortKey.value].localeCompare(a[sortKey.value]);
        }
      });
    });

    const filteredProducts = computed(() => {
      return sortedProducts.value.filter(product =>
        product.name.toLowerCase().includes(searchQuery.value.toLowerCase())
      );
    });

    const editProduct = (productName) => {
      router.push({ name: 'EditProduct', params: { name: productName } });
    };

    const formatPrice = (price) => {
      const num = Number(price);
      return isNaN(num) ? price : num.toFixed(2);
    };

    return {
      user,
      soldOutProducts,
      goBack,
      sortKey,
      sortOrder,
      searchQuery,
      sortedProducts,
      filteredProducts,
      handleSortChange,
      editProduct,
      formatPrice,
      Search,
    }
  }
}
</script>

<style scoped>
.view-stock-container {
  padding: 20px;
  height: 100vh;
  background-color: #f5f7fa;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.back-button {
  padding: 8px 15px;
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
}

.stock-card {
  height: calc(100vh - 100px);
}

.toolbar {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.search-input {
  width: 300px;
}

.sort-select {
  width: 200px;
}

.product-image {
  width: 80px;
  height: 80px;
  border-radius: 4px;
}

.image-error {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: #f4f9ff;
  color: #909399;
  font-size: 20px;
}

.price {
  color: #ff4500;
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
  .toolbar {
    flex-direction: column;
  }
  
  .search-input,
  .sort-select {
    width: 100%;
  }
}
</style>