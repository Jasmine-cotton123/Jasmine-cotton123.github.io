<template>
  <div class="view-stock-container">
    <div class="page-header">
      <el-button @click="goBack" type="primary" plain class="back-button">
        <el-icon><Back /></el-icon> 返回
      </el-button>
      <h2>商品评论详情</h2>
    </div>

    <el-card class="stock-card">
      <div class="product-info">
        <el-image
          :src="product.src"
          :preview-src-list="[product.src]"
          fit="cover"
          class="product-image"
        >
          <template #error>
            <div class="image-error">
              <el-icon><Picture /></el-icon>
            </div>
          </template>
        </el-image>

        <div class="product-details">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="商品名称">
              {{ product.name }}
            </el-descriptions-item>
            <el-descriptions-item label="库存数量">
              <el-tag :type="product.num > 0 ? 'success' : 'danger'" size="small">
                {{ product.num }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="价格">
              <span class="price">￥{{ formatPrice(product.price) }}</span>
            </el-descriptions-item>
            <el-descriptions-item label="商品介绍">
              {{ product.produce }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </div>

      <div class="comments-section">
        <h3 class="section-title">评论列表</h3>
        <el-table
          :data="comments"
          style="width: 100%"
          :header-cell-style="{ background: '#f5f7fa' }"
        >
          <el-table-column label="用户" width="200">
            <template #default="{ row }">
              <div class="user-info">
                <el-avatar 
                  :size="32" 
                  :src="`https://api.dicebear.com/7.x/micah/svg?seed=${row.username}`"
                />
                <span class="username">{{ row.username }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="comment" label="评论内容" show-overflow-tooltip>
            <template #default="{ row }">
              <div class="comment-content">{{ row.comment }}</div>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { 
  Back, 
  Picture 
} from '@element-plus/icons-vue'

export default {
  name: 'CommentDetails',
  components: {
    Back,
    Picture
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const comments = ref([]);
    const product = ref({});

    const fetchComments = async () => {
      try {
        const response = await axios.get(`http://localhost:11000/api/comments/${route.query.name}`);
        comments.value = response.data;
      } catch (error) {
        console.error('获取评论信息失败:', error);
      }
    };

    const fetchProductDetails = async () => {
      try {
        const response = await axios.get(`http://localhost:11000/api/product/${route.query.name}`);
        product.value = response.data;
      } catch (error) {
        console.error('获取商品信息失败:', error);
      }
    };

    onMounted(() => {
      fetchComments();
      fetchProductDetails();
    });

    const goBack = () => {
      router.push('/view-comments');
    };

    const formatPrice = (price) => {
      const num = Number(price);
      return isNaN(num) ? price : num.toFixed(2);
    };

    return {
      comments,
      product,
      goBack,
      formatPrice
    };
  }
};
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
  padding: 20px;
}

.product-info {
  display: flex;
  gap: 24px;
  margin-bottom: 32px;
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.product-image {
  width: 200px;
  height: 200px;
  border-radius: 8px;
  flex-shrink: 0;
}

.product-details {
  flex: 1;
}

.image-error {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: #f4f9ff;
  color: #909399;
  font-size: 24px;
}

.price {
  color: #ff4500;
  font-weight: bold;
  font-size: 1.1rem;
}

.section-title {
  margin: 0 0 16px;
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.username {
  font-weight: 500;
  color: #409EFF;
}

.comment-content {
  line-height: 1.6;
  color: #606266;
}

:deep(.el-descriptions) {
  margin: 0;
}

:deep(.el-descriptions__cell) {
  padding: 12px 16px;
}

:deep(.el-table__header) {
  background-color: #f5f7fa;
}

:deep(.el-table) {
  --el-table-border-color: #ebeef5;
  --el-table-header-background-color: #f5f7fa;
}

@media (max-width: 768px) {
  .product-info {
    flex-direction: column;
  }

  .product-image {
    width: 100%;
    height: 200px;
  }
}
</style>