<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" type="primary" plain class="back-button">
          <el-icon><Back /></el-icon> 返回
        </el-button>
        <h2>我的评论</h2>
      </div>
    </div>

    <div class="content-container">
      <el-card class="comments-card" v-loading="loading" v-if="commentedItems.length">
        <el-table 
          :data="commentedItems" 
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

          <el-table-column label="数量" width="100" align="center">
            <template #default="{ row }">
              <el-tag size="small">{{ row.quantity }}</el-tag>
            </template>
          </el-table-column>

          <el-table-column label="总价" width="120" align="right">
            <template #default="{ row }">
              <span class="total-price">￥{{ row.total_price }}</span>
            </template>
          </el-table-column>

          <el-table-column label="评论内容" min-width="300">
            <template #default="{ row }">
              <div class="comment-content">
                <el-icon class="comment-icon"><ChatDotRound /></el-icon>
                {{ row.comment }}
              </div>
            </template>
          </el-table-column>

          <el-table-column label="操作" width="120" align="center">
            <template #default="{ row }">
              <el-button 
                type="primary" 
                link
                @click="viewItemDetail(row.name)"
              >
                <el-icon><View /></el-icon>
                查看商品
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>

      <el-empty 
        v-else
        description="暂无评论记录" 
        :image-size="200"
      >
        <el-button type="primary" @click="goToHistory">
          去评价
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
  View,
  ChatDotRound
} from '@element-plus/icons-vue'

export default {
  name: 'MyComments',
  components: {
    Back,
    Picture,
    View,
    ChatDotRound
  },
  setup() {
    const router = useRouter()
    const commentedItems = ref([])
    const loading = ref(true)

    const fetchCommentedItems = async () => {
      const userStr = localStorage.getItem('user')
      if (!userStr) {
        ElMessage.warning('请先登录')
        router.push('/login')
        return
      }

      const user = JSON.parse(userStr)
      try {
        const response = await axios.get(`http://localhost:11000/api/my-comments/${user.username}`)
        commentedItems.value = response.data
      } catch (error) {
        console.error('获取评论信息失败:', error)
        ElMessage.error('获取评论信息失败')
      } finally {
        loading.value = false
      }
    }

    const viewItemDetail = (name) => {
      router.push(`/item/${name}`)
    }

    const goBack = () => {
      router.back()
    }

    const goToHistory = () => {
      router.push('/purchase-history')
    }

    onMounted(fetchCommentedItems)

    return {
      commentedItems,
      loading,
      viewItemDetail,
      goBack,
      goToHistory
    }
  }
}
</script>

<style scoped>
.page-container {
  padding: 20px;
  min-height: calc(100vh - 40px);
  background: #f4f9ff;
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

.comments-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
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

.comment-content {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 8px;
  background: #f8f9fa;
  border-radius: 4px;
  line-height: 1.4;
}

.comment-icon {
  color: #409EFF;
  font-size: 16px;
  margin-top: 2px;
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