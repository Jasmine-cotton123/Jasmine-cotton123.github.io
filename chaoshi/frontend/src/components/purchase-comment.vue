<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" type="primary" plain class="back-button">
          <el-icon><Back /></el-icon> 返回
        </el-button>
        <h2>商品评价</h2>
      </div>
    </div>

    <div class="content-container">
      <el-card class="comment-card" v-loading="loading">
        <div class="product-content" v-if="itemDetail">
          <div class="product-info">
            <el-image
              :src="itemDetail.src"
              fit="cover"
              class="product-image"
              :preview-src-list="[itemDetail.src]"
            >
              <template #error>
                <div class="image-error">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>

            <div class="info-section">
              <h3 class="product-name">{{ itemDetail.name }}</h3>
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
          </div>

          <div class="comment-section">
            <h3>我的评价</h3>
            <el-input
              v-model="comment"
              type="textarea"
              :rows="4"
              :disabled="isCommented"
              :placeholder="isCommented ? '已评价' : '请输入您的评价内容...'"
              resize="none"
              maxlength="500"
              show-word-limit
            />
            
            <div class="comment-actions" v-if="!isCommented">
              <el-button @click="goBack">取消</el-button>
              <el-button 
                type="primary" 
                @click="submitComment"
                :disabled="!comment.trim()"
              >
                提交评价
              </el-button>
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
import { useRouter, useRoute } from 'vue-router'
import { Back, Picture } from '@element-plus/icons-vue'

export default {
  name: 'PurchaseComment',
  components: {
    Back,
    Picture
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const itemDetail = ref(null)
    const comment = ref('')
    const isCommented = ref(false)
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
        if (response.data.comment) {
          comment.value = response.data.comment
          isCommented.value = true
        }
      } catch (error) {
        console.error('获取商品详情失败:', error)
        ElMessage.error('获取商品详情失败')
      } finally {
        loading.value = false
      }
    }

    const submitComment = async () => {
      if (!comment.value.trim()) return

      const { name, purchase_time } = route.params
      try {
        await axios.post(`http://localhost:11000/api/purchase/comment`, {
          name,
          purchase_time,
          comment: comment.value.trim()
        })
        ElMessage.success('评价提交成功')
        router.push('/purchase-history')
      } catch (error) {
        console.error('提交评论失败:', error)
        ElMessage.error('评价提交失败')
      }
    }

    const goBack = () => {
      router.back()
    }

    onMounted(fetchItemDetail)

    return {
      itemDetail,
      comment,
      isCommented,
      loading,
      submitComment,
      goBack
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

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
}

.header-left h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 500;
}

.content-container {
  max-width: 800px;
  margin: 0 auto;
}

.comment-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.product-content {
  padding: 24px;
}

.product-info {
  display: flex;
  gap: 24px;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #ebeef5;
}

.product-image {
  width: 200px;
  height: 200px;
  border-radius: 8px;
  flex-shrink: 0;
}

.image-error {
  width: 200px;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f4f9ff;
  color: #909399;
  font-size: 24px;
  border-radius: 8px;
}

.info-section {
  flex: 1;
}

.product-name {
  margin: 0 0 16px;
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.info-grid {
  display: grid;
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 14px;
  color: #909399;
}

.info-value {
  font-size: 14px;
  color: #303133;
}

.info-value.price {
  color: #ff4500;
  font-weight: bold;
}

.info-value.time {
  font-family: monospace;
}

.comment-section h3 {
  margin: 0 0 16px;
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.comment-actions {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

@media (max-width: 768px) {
  .page-container {
    padding: 12px;
  }

  .product-info {
    flex-direction: column;
  }

  .product-image {
    width: 100%;
    height: 240px;
  }

  .image-error {
    width: 100%;
    height: 240px;
  }
}
</style>