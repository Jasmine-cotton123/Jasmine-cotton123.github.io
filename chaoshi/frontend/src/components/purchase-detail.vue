<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" type="primary" plain class="back-button">
          <el-icon><Back /></el-icon> 返回
        </el-button>
        <h2>购买详情</h2>
      </div>
    </div>

    <div class="content-container">
      <el-card class="detail-card" v-loading="loading">
        <div class="product-content">
          <div class="product-gallery">
            <el-image
              :src="itemDetail.src"
              fit="cover"
              class="product-image"
              :preview-src-list="[itemDetail.src]"
              :initial-index="0"
            >
              <template #placeholder>
                <div class="image-placeholder">
                  <el-icon><Loading /></el-icon>
                </div>
              </template>
              <template #error>
                <div class="image-error">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>
          </div>

          <div class="product-info">
            <div class="info-section">
              <h1 class="product-name">{{ itemDetail.name }}</h1>
              
              <div class="info-grid">
                <div class="info-item">
                  <span class="info-label">购买数量</span>
                  <span class="info-value">{{ itemDetail.quantity }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">总价</span>
                  <span class="info-value price">￥{{ itemDetail.total_price }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">购买时间</span>
                  <span class="info-value time">{{ itemDetail.purchase_time }}</span>
                </div>
              </div>
            </div>

            <div class="description-section">
              <h3>商品介绍</h3>
              <div class="description-content">
                {{ itemDetail.produce || '暂无商品介绍' }}
              </div>
            </div>

            <div class="comment-section">
              <h3>我的评价</h3>
              <div class="comment-content" v-if="itemDetail.comment">
                <el-icon class="comment-icon"><ChatDotRound /></el-icon>
                {{ itemDetail.comment }}
              </div>
              <div class="no-comment" v-else>
                <el-empty description="暂无评价" :image-size="60">
                  <el-button 
                    type="primary" 
                    @click="goToComment"
                  >
                    去评价
                  </el-button>
                </el-empty>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useRoute, useRouter } from 'vue-router'
import { 
  Back, 
  Picture,
  Loading,
  ChatDotRound
} from '@element-plus/icons-vue'

export default {
  name: 'PurchaseDetail',
  components: {
    Back,
    Picture,
    Loading,
    ChatDotRound
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const itemDetail = ref({})
    const loading = ref(true)

    const fetchItemDetail = async () => {
      const { name, purchase_time } = route.params
      if (!name || !purchase_time) {
        ElMessage.error('参数错误')
        router.push('/purchase-history')
        return
      }

      try {
        const response = await axios.get(`http://localhost:11000/api/purchase/item`, { 
          params: { name, purchase_time } 
        })
        itemDetail.value = response.data
      } catch (error) {
        console.error('获取商品详情失败:', error)
        ElMessage.error('获取商品详情失败')
      } finally {
        loading.value = false
      }
    }

    const goBack = () => {
      router.back()
    }

    const goToComment = () => {
      router.push({ 
        name: 'PurchaseComment', 
        params: { 
          name: itemDetail.value.name,
          purchase_time: itemDetail.value.purchase_time
        }
      })
    }

    onMounted(fetchItemDetail)

    return {
      itemDetail,
      loading,
      goBack,
      goToComment
    }
  }
}
</script>

<style scoped>
.page-container {

  min-height: calc(100vh - 40px);
  background: #f4f9ff;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  background: linear-gradient(to right, #616fff, #3949ab);
}
.header-left{
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px;
}
.header-left h2 {
  display: block;
  flex: 1;
  text-align: center;
  margin: 0;
  font-size: 24px;
  font-weight: 500;
  color: #fff;
}
.header-left .header-section {
  width: 60px;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
}

.detail-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.product-content {
  display: grid;
  grid-template-columns: minmax(300px, 2fr) 3fr;
  gap: 40px;
  padding: 24px;
}

.product-gallery {
  position: sticky;
  top: 24px;
}

.product-image {
  width: 100%;
  height: 400px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.image-placeholder,
.image-error {
  width: 100%;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f4f9ff;
  color: #909399;
  font-size: 24px;
  border-radius: 8px;
}

.product-info {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.info-section,
.description-section,
.comment-section {
  padding: 24px;
  background: #f8f9fa;
  border-radius: 8px;
}

.product-name {
  margin: 0 0 24px;
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  line-height: 1.4;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.info-label {
  font-size: 14px;
  color: #909399;
}

.info-value {
  font-size: 16px;
  color: #303133;
}

.info-value.price {
  color: #ff4500;
  font-weight: bold;
  font-size: 20px;
}

.info-value.time {
  font-family: monospace;
}

.description-section h3,
.comment-section h3 {
  margin: 0 0 16px;
  font-size: 18px;
  font-weight: 500;
  color: #3949ab;
}

.description-content,
.comment-content {
  font-size: 14px;
  line-height: 1.8;
  color: #606266;
  white-space: pre-wrap;
}

.comment-content {
  display: flex;
  gap: 8px;
  padding: 16px;
  background: #fff;
  border-radius: 4px;
}

.comment-icon {
  color: #409EFF;
  font-size: 16px;
  margin-top: 2px;
}

.no-comment {
  padding: 20px 0;
}

@media (max-width: 992px) {
  .product-content {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .product-gallery {
    position: static;
  }

  .product-image {
    height: 300px;
  }

  .info-section,
  .description-section,
  .comment-section {
    padding: 16px;
  }
}

@media (max-width: 576px) {
  .page-container {
    padding: 12px;
  }

  .product-content {
    padding: 16px;
  }

  .product-name {
    font-size: 24px;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>