<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" type="primary" plain class="back-button">
          <el-icon><Back /></el-icon> 返回
        </el-button>
        <h2>购买历史</h2>
      </div>
    </div>

    <div class="content-container">
      <el-card class="history-card" v-if="purchaseHistory.length">
        <el-table 
          :data="purchaseHistory" 
          style="width: 100%"
          :header-cell-style="{ background: '#f5f7fa' }"
        >
          <el-table-column label="商品信息" min-width="400">
            <template #default="{ row }">
              <div class="product-info">
                <el-image
                  :src="row.src"
                  fit="cover"
                  class="product-image"
                  :preview-src-list="[row.src]"
                >
                  <template #error>
                    <div class="image-error">
                      <el-icon><Picture /></el-icon>
                    </div>
                  </template>
                </el-image>
                <div class="product-detail">
                  <div class="product-name">{{ row.name }}</div>
                  <div class="purchase-time">{{ row.purchase_time }}</div>
                </div>
              </div>
            </template>
          </el-table-column>

          <el-table-column label="数量" width="120" align="center">
            <template #default="{ row }">
              <el-tag size="small">{{ row.quantity }}</el-tag>
            </template>
          </el-table-column>

          <el-table-column label="总价" width="150" align="right">
            <template #default="{ row }">
              <span class="total-price">￥{{ row.total_price }}</span>
            </template>
          </el-table-column>

          <el-table-column label="操作" width="200" align="center">
            <template #default="{ row }">
              <el-button 
                type="primary" 
                link
                @click="viewItemDetail(row.name, row.purchase_time)"
              >
                <el-icon><Document /></el-icon>
                查看详情
              </el-button>
              <el-button 
                :type="row.comment ? 'success' : 'warning'" 
                link
                @click="commentItem(row.name, row.purchase_time)"
              >
                <el-icon v-if="row.comment"><Check /></el-icon>
                <el-icon v-else><Edit /></el-icon>
                {{ row.comment ? '已评价' : '去评价' }}
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <el-empty 
        v-else 
        description="暂无购买记录" 
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
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { 
  Back,
  Picture,
  Document,
  Edit,
  Check
} from '@element-plus/icons-vue'

export default {
  name: 'PurchaseHistory',
  components: {
    Back,
    Picture,
    Document,
    Edit,
    Check
  },
  setup() {
    const router = useRouter()
    const purchaseHistory = ref([])

    const fetchPurchaseHistory = async () => {
      const userStr = localStorage.getItem('user')
      if (!userStr) {
        ElMessage.warning('请先登录')
        router.push('/login')
        return
      }

      const user = JSON.parse(userStr)
      try {
        const response = await axios.get(`http://localhost:11000/api/purchase-history/${user.username}`)
        purchaseHistory.value = response.data.map(item => ({
          ...item,
          comment: item.comment || null
        }))
      } catch (error) {
        console.error('获取购买记录失败:', error)
        ElMessage.error('获取购买记录失败')
      }
    }

    const viewItemDetail = (name, purchase_time) => {
      if (name && purchase_time) {
        router.push({ name: 'PurchaseDetail', params: { name, purchase_time } })
      }
    }

    const commentItem = (name, purchase_time) => {
      if (name && purchase_time) {
        router.push({ name: 'PurchaseComment', params: { name, purchase_time } })
      }
    }

    const goBack = () => {
      router.push('/Shouye')
    }

    const goToShopping = () => {
      router.push('/Shouye')
    }

    onMounted(fetchPurchaseHistory)

    return {
      purchaseHistory,
      viewItemDetail,
      commentItem,
      goBack,
      goToShopping
    }
  }
}
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

.history-card {
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

.purchase-time {
  color: #909399;
  font-size: 12px;
}

.total-price {
  color: #ff4500;
  font-weight: bold;
  font-size: 16px;
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