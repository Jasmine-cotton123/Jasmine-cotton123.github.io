<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" type="primary" plain class="back-button">
          <el-icon><Back /></el-icon> 返回
        </el-button>
        <h2>商品详情</h2>
        <div class="header-section"></div>
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
              
              <div class="product-price">
                <span class="price-label">价格</span>
                <span class="price-value">￥{{ itemDetail.price }}</span>
              </div>

              <div class="product-stats">
                <div class="stat-group">
                  <el-tag 
                    size="large" 
                    :type="itemDetail.num > 0 ? 'success' : 'danger'" 
                    effect="light"
                    class="stock-tag"
                  >
                    库存: {{ itemDetail.num || 1 }}
                  </el-tag>
                </div>
              </div>
            </div>
            <div class="description-section">
              <h3>商品介绍</h3>
              <div class="description-content">
                {{ itemDetail.produce || '暂无商品介绍' }}
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
  Star,
  ShoppingCart
} from '@element-plus/icons-vue'

export default {
  name: 'ItemDetail',
  components: {
    Back,
    Picture,
    Star,
    ShoppingCart
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const itemDetail = ref({})

    const fetchItemDetail = async () => {
      const name = route.params.name
      try {
        const response = await axios.get(`http://localhost:11000/api/product/${name}`)

        
        itemDetail.value = response.data
        console.log(itemDetail.value);
      } catch (error) {
        console.error('获取商品详情失败:', error)
        ElMessage.error('获取商品详情失败')
      }
    }

    const toggleFavorite = async () => {
      // 实现收藏功能
    }

    const toggleCart = async () => {
      // 实现加入购物车功能
    }

    const goBack = () => {
      router.back()
    }

    onMounted(fetchItemDetail)

    return {
      itemDetail,
      toggleFavorite,
      toggleCart,
      goBack,
      Star,
      ShoppingCart
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
  margin: 40px auto;
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
  margin-top: 20px;
}

.info-section,
.action-section,
.description-section {
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

.product-price {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 24px;
}

.price-label {
  font-size: 16px;
  color: #909399;
}

.price-value {
  font-size: 32px;
  font-weight: bold;
  color: #ff4500;
}

.product-stats {
  margin-bottom: 24px;
}

.stat-group {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 24px;
}

.stock-tag {
  padding: 8px 16px;
  font-size: 14px;
}

.stat-items {
  display: flex;
  gap: 24px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #606266;
  font-size: 14px;
}

.quantity-selector {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.quantity-label {
  font-size: 16px;
  color: #606266;
}

.product-actions {
  display: flex;
  gap: 16px;
}

.product-actions .el-button {
  flex: 1;
  height: 48px;
  font-size: 16px;
}

.product-actions .is-active {
  background-color: #409EFF;
  border-color: #409EFF;
  color: #fff;
}

.description-section h3 {
  margin: 0 0 16px;
  font-size: 18px;
  font-weight: 500;
  color: #3949ab;
}

.description-content {
  font-size: 14px;
  line-height: 1.8;
  color: #606266;
  white-space: pre-wrap;
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
  .action-section,
  .description-section {
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

  .price-value {
    font-size: 28px;
  }

  .product-actions {
    flex-direction: column;
  }
}
</style>

