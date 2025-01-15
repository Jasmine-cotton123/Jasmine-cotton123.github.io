<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" type="primary" plain class="back-button">
          <el-icon><Back /></el-icon> 返回
        </el-button>
        <h2>我的收藏</h2>
      </div>
    </div>

    <div class="content-container">
      <template v-if="favoriteImages.length">
        <el-card 
          v-for="item in favoriteImages" 
          :key="item.image_id" 
          class="product-card"
          :body-style="{ padding: '0px' }"
        >
          <div class="product-image">
            <el-image
              :src="`http://localhost:11000/api/image/${item.image_id}`"
              fit="cover"
              :preview-src-list="[`http://localhost:11000/api/image/${item.image_id}`]"
            >
              <template #error>
                <div class="image-error">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>
          </div>

          <div class="product-info">
            <h3 class="product-name">{{ item.name }}</h3>
            <div class="product-price">
              <span class="price-label">价格：</span>
              <span class="price-value">￥{{ item.price }}</span>
            </div>
            <div class="product-desc">{{ item.produce }}</div>
            
            <div class="product-actions">
              <el-button 
                type="primary" 
                plain 
                size="small"
                @click="viewDetail(item)"
              >
                <el-icon><View /></el-icon>
                查看详情
              </el-button>
              <el-button 
                type="danger" 
                plain 
                size="small"
                @click="removeFavorite(item)"
              >
                <el-icon><Delete /></el-icon>
                取消收藏
              </el-button>
            </div>
          </div>
        </el-card>
      </template>

      <el-empty 
        v-else 
        description="暂无收藏商品" 
        :image-size="200"
      >
        <el-button type="primary" @click="goToShopping">
          去逛逛
        </el-button>
      </el-empty>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import { 
  Back, 
  Picture,
  View,
  Delete
} from '@element-plus/icons-vue'

export default {
  name: 'Favorites',
  components: {
    Back,
    Picture,
    View,
    Delete
  },
  setup() {
    const router = useRouter()
    const favoriteImages = ref([])
    const user = JSON.parse(localStorage.getItem('user') || '{}')

    const fetchFavorites = async () => {
      try {
        const response = await axios.get(`http://localhost:11000/api/favorites/${user.username}`)
        favoriteImages.value = response.data
      } catch (error) {
        console.error('获取收藏失败:', error)
        ElMessage.error('获取收藏失败')
      }
    }

    const removeFavorite = async (item) => {
      try {
        await ElMessageBox.confirm(
          '确定要取消收藏该商品吗？',
          '提示',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await axios.delete(`http://localhost:11000/api/favorites/${user.username}/${item.image_id}`)
        ElMessage.success('已取消收藏')
        await fetchFavorites()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('取消收藏失败:', error)
          ElMessage.error('取消收藏失败')
        }
      }
    }

    const viewDetail = (item) => {
      router.push(`/item/${item.name}`)
    }

    const goBack = () => {
      router.back()
    }

    const goToShopping = () => {
      router.push('/Shouye')
    }

    onMounted(() => {
      if (!user.username) {
        ElMessage.warning('请先登录')
        router.push('/login')
        return
      }
      fetchFavorites()
    })

    return {
      favoriteImages,
      goBack,
      viewDetail,
      removeFavorite,
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

.content-container {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

.product-card {
  transition: transform 0.3s, box-shadow 0.3s;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.product-image {
  height: 200px;
  overflow: hidden;
}

.product-image .el-image {
  width: 100%;
  height: 100%;
}

.image-error {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f4f9ff;
  color: #909399;
  font-size: 24px;
}

.product-info {
  padding: 15px;
}

.product-name {
  margin: 0 0 10px;
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.product-price {
  margin-bottom: 10px;
}

.price-label {
  color: #909399;
  font-size: 14px;
}

.price-value {
  color: #ff4500;
  font-size: 16px;
  font-weight: bold;
}

.product-desc {
  margin-bottom: 15px;
  color: #606266;
  font-size: 14px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .page-container {
    padding: 10px;
  }
  
  .content-container {
    grid-template-columns: 1fr;
  }
}
</style>