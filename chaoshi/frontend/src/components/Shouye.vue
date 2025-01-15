<template>
  <div class="full-screen">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <h1>超市购物系统</h1>
          <div class="header-right">
            <el-avatar 
              :size="40" 
              :src="`https://api.dicebear.com/7.x/micah/svg?seed=${user?.username}`"
              class="header-avatar"
            />
            <span class="username">{{ user?.username }}</span>
          </div>
        </div>
      </el-header>
      <el-container class="main-container">
        <el-aside width="220px" class="aside" v-if="user?.role === 'admin' || user?.role === 'manager'">
          <el-menu :default-active="activeMenu" class="el-menu-vertical-demo">
            <template v-if="user?.role === 'admin'">
              <el-menu-item index="1" @click="goToAddProduct">
                <el-icon><Plus /></el-icon>
                <template #title>添加商品</template>
              </el-menu-item>
              <el-menu-item index="2" @click="goToViewStock">
                <el-icon><View /></el-icon>
                <template #title>查看库存 ({{ stockLength }})</template>
              </el-menu-item>
              <el-menu-item index="3" @click="goToSoldOut">
                <el-icon><SoldOut /></el-icon>
                <template #title>售罄商品 ({{ soldOutLength }})</template>
              </el-menu-item>
              <el-menu-item index="4" @click="goToViewComments">
                <el-icon><ChatDotRound /></el-icon>
                <template #title>查看评论({{ commentLength }})</template>
              </el-menu-item>
            </template>
            <template v-if="user?.role === 'manager'">
              <el-menu-item index="2" @click="goToViewStock">
                <el-icon><View /></el-icon>
                <template #title>查看库存 ({{ stockLength }})</template>
              </el-menu-item>
              <el-menu-item index="3" @click="goToSoldOut">
                <el-icon><SoldOut /></el-icon>
                <template #title>售罄商品 ({{ soldOutLength }})</template>
              </el-menu-item>
              <el-menu-item index="5" @click="goToAddAdmin">
                <el-icon><Plus /></el-icon>
                <template #title>添加管理员</template>
              </el-menu-item>
              <el-sub-menu index="6">
                <template #title>
                  <el-icon><PieChart /></el-icon>
                  <span>查看图表</span>
                </template>
                <el-menu-item-group title="Group One">
                  <el-menu-item index="6-1" @click="goToChartOne">图表一</el-menu-item>
                  <el-menu-item index="6-2" @click="goToChartTwo">图表二</el-menu-item>
                </el-menu-item-group>
                <el-menu-item-group title="Group Two">
                  <el-menu-item index="6-3" @click="goToChartThree">图表三</el-menu-item>
                </el-menu-item-group>
                <el-sub-menu index="6-4">
                  <template #title>图表四</template>
                  <el-menu-item index="6-4-1" @click="goToChartFour">图表四</el-menu-item>
                </el-sub-menu>
              </el-sub-menu>
              <el-menu-item index="7" @click="goToAdminInfo">
                <el-icon><User /></el-icon>
                <template #title>查看管理员信息</template>
              </el-menu-item>
            </template>
          </el-menu>
        </el-aside>
        
        <el-container class="content-container">
          <el-main>
            <div class="carousel-container">
              <el-carousel height="400px" motion-blur class="custom-carousel">
                <el-carousel-item v-for="(image, index) in carouselImages" :key="index">
                  <img :src="image" alt="carousel image" class="carousel-image" />
                </el-carousel-item>
              </el-carousel>
            </div>

            <div class="search-section">
              <div class="custom-search-bar">
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="搜索卡片名称"
                  @keyup.enter="searchImages"
                >
                <button class="search-button" @click="searchImages">
                  <el-icon><Search /></el-icon>
                </button>
              </div>
            </div>

            <div class="custom-tabs">
              <div class="tabs-wrapper">
                <button 
                  class="tab-button"
                  :class="{ active: activeTab === 'all' }"
                  @click="activeTab = 'all'"
                >
                  所有
                </button>
                <button 
                  v-for="label in labels" 
                  :key="label"
                  class="tab-button"
                  :class="{ active: activeTab === label }"
                  @click="activeTab = label"
                >
                  {{ label }}
                </button>
              </div>
            </div>

            <div class="cards-section">
              <div class="card-container">
                <el-card v-for="image in paginatedImages" :key="image.id" class="image-card">
                  <div class="card-image-wrapper">
                    <img :src="image.src" class="card-image" />
                    <div class="card-overlay">
                      <div class="card-actions">
                        <el-button 
                          v-if="!isAdminOrManager" 
                          circle
                          :class="{'is-favorite': image.isFavorite}"
                          @click="toggleFavorite(image)"
                        >
                          <el-icon><component :is="image.isFavorite ? 'StarFilled' : 'Star'" /></el-icon>
                        </el-button>
                        <el-button 
                          v-if="!isAdminOrManager" 
                          circle
                          :class="{'in-cart': image.isInCart}"
                          @click="toggleCart(image)"
                        >
                          <el-icon><component :is="image.isInCart ? 'ShoppingCartFull' : 'ShoppingCart'" /></el-icon>
                        </el-button>
                      </div>
                    </div>
                  </div>
                  
                  <div class="card-content">
                    <div class="card-header">
                      <h3 class="card-title">{{ image.name }}</h3>
                      <div class="card-price">¥{{ image.price }}</div>
                    </div>
                    
                    <div class="card-info">
                      <el-tag size="small" :type="image.num > 0 ? 'success' : 'danger'" effect="light">
                        库存: {{ image.num }}
                      </el-tag>
                      
                      <div v-if="isAdminOrManager" class="stats-info">
                        <el-tooltip content="收藏人数" placement="top">
                          <span class="stat-item">
                            <el-icon><Star /></el-icon>
                            {{ image.favorite }}
                          </span>
                        </el-tooltip>
                        <el-tooltip content="购物车人数" placement="top">
                          <span class="stat-item">
                            <el-icon><ShoppingCart /></el-icon>
                            {{ image.cart }}
                          </span>
                        </el-tooltip>
                      </div>
                    </div>
                    
                    <div class="card-description">
                      {{ image.produce }}
                    </div>
                  </div>
                </el-card>
              </div>
              
              <div class="pagination-wrapper">
                <el-pagination
                  background
                  layout="prev, pager, next"
                  :total="filteredImages.length"
                  :page-size="6"
                  @current-change="handlePageChange">
                </el-pagination>
              </div>
            </div>
          </el-main>
          
          <el-aside width="280px" class="right-aside">
            <div class="welcome-card">
              <el-avatar 
                :size="80" 
                :src="`https://api.dicebear.com/7.x/micah/svg?seed=${user?.username}`"
                class="avatar"
              />
              <div class="user-info">
                <h1>欢迎回来</h1>
                <h2>{{ user?.username }}</h2>
                <el-tag :type="getRoleType" class="role-tag" effect="dark">
                  {{ user?.role }}
                </el-tag>
              </div>
              <el-button type="primary" class="logout-btn" @click="handleLogout">
                退出登录
              </el-button>

              <template v-if="!isAdminOrManager">
                <el-button type="text" class="favorites-btn" @click="goToFavorites">
                  <el-icon><StarFilled /></el-icon>
                  收藏 ({{ favoriteImages.length }})
                </el-button>
                <el-button type="text" class="cart-btn" @click="goToCart">
                  <el-icon><ShoppingCart /></el-icon>
                  购物车 ({{ cartImages.length }})
                </el-button>
                <el-button type="text" class="purchase-history-btn" @click="goToPurchaseHistory">
                  <el-icon><Document /></el-icon>
                  购买记录 ({{ purchaseHistoryCount }})
                </el-button>
                <el-button type="text" class="comment-btn" @click="goToComments">
                  <el-icon><ChatDotRound /></el-icon>
                  我的评论 ({{ commentCount }})
                </el-button>
              </template>
            </div>
          </el-aside>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage,ElCarousel } from 'element-plus';
import { Star, StarFilled, ShoppingCart, ShoppingCartFull, Document, ChatDotRound, Plus, View, SoldOut, PieChart ,User} from '@element-plus/icons-vue';
import img1 from '../assets/image1.png';
import img2 from '../assets/image2.png';
import img3 from '../assets/image3.png';
import img4 from '../assets/image4.png';
export default {
  name: 'Shouye',
  components: {
    Star,
    StarFilled,
    ShoppingCart,
    ShoppingCartFull,
    Document,
    ChatDotRound,
    Plus,
    View,
    SoldOut,
    PieChart,
    ElCarousel
  },
  setup() {
    const router = useRouter();
    const user = ref(null);
    const searchQuery = ref('');
    const images = ref([]);
    const filteredImages = ref([]);
    const favoriteImages = ref([]);
    const cartImages = ref([]);
    const purchaseHistoryCount = ref(0);
    const commentCount = ref(0);
    const commentLength = ref(0);
    const currentPage = ref(1);
    const activeTab = ref('all');
    const labels = ref([]);
    
    const carouselImages = ref([
    img2,
    img3,
    img4
    ]);

    const getRoleType = computed(() => {
      switch (user.value?.role) {
        case 'admin':
          return 'danger';
        case 'manager':
          return 'warning';
        default:
          return 'success';
      }
    });

    const isAdminOrManager = computed(() => {
      return user.value?.role === 'admin' || user.value?.role === 'manager';
    });

    const paginatedImages = computed(() => {
      const start = (currentPage.value - 1) * 6;
      const end = start + 6;
      return filteredImages.value.filter(image => image.num > 0).slice(start, end);
    });
    

    const filterImagesByLabel = () => {
      if (activeTab.value === 'all') {
        filteredImages.value = images.value;
      } else {
        filteredImages.value = images.value.filter(image => image.label === activeTab.value);
      }
    };

    const stockLength = computed(() => images.value.length);

    const soldOutLength = computed(() => images.value.filter(image => image.num === 0 || image.num === '0').length);

    onMounted(async () => {
      const userStr = localStorage.getItem('user');
      if (userStr) {
        user.value = JSON.parse(userStr);
        await fetchFavorites();
        await fetchCart();
        await fetchPurchaseHistoryCount();
        await fetchCommentCount();
        await fetchCommentLength();
      } else {
        router.push('/login');
      }
      await fetchImages();
    });

    watch(activeTab, filterImagesByLabel);

    const handleLogout = () => {
      localStorage.removeItem('user');
      ElMessage.success('已退出登录');
      router.push('/login');
    };

    const goToFavorites = () => {
      router.push('/favorites');
    };

    const goToCart = () => {
      router.push('/cart');
    };

    const goToPurchaseHistory = () => {
      router.push('/purchase-history');
    };

    const goToComments = () => {
      router.push('/my-comments');
    };

    const goToAddProduct = () => {
      router.push('/add-product');
    };

    const goToViewStock = () => {
      router.push('/view-stock');
    };

    const goToSoldOut = () => {
      router.push('/sold-out');
    };

    const goToViewComments = () => {
      router.push('/view-comments');
    };

    const goToAddAdmin = () => {
      router.push('/add-admin');
    };

    const goToChartOne = () => {
      router.push('/Page1');
    };

    const goToChartTwo = () => {
      router.push('/Page2');
    };

    const goToChartThree = () => {
      router.push('/Page3');
    };

    const goToChartFour = () => {
      router.push('/Page4');
    };

    const goToAdminInfo = () => {
      router.push('/admin-info')
    };

    const fetchFavorites = async () => {
      try {
        const response = await axios.get(`http://localhost:11000/api/favorites/${user.value.username}`);
        favoriteImages.value = response.data.map(fav => fav.image_id);
        await fetchImages();
      } catch (error) {
        console.error('获取收藏失败:', error);
      }
    };

    const fetchCart = async () => {
      try {
        const response = await axios.get(`http://localhost:11000/api/shopping/${user.value.username}`);
        cartImages.value = response.data.map(item => item.image_id);
        await fetchImages();
      } catch (error) {
        console.error('获取购物车失败:', error);
      }
    };

    const fetchPurchaseHistoryCount = async () => {
      try {
        const response = await axios.get(`http://localhost:11000/api/purchase-history/${user.value.username}`);
        purchaseHistoryCount.value = response.data.length;
      } catch (error) {
        console.error('获取购买记录失败:', error);
      }
    };

    const fetchCommentCount = async () => {
      try {
        const response = await axios.get(`http://localhost:11000/api/my-comments/${user.value.username}`);
        commentCount.value = response.data.length;
      } catch (error) {
        console.error('获取评论数量失败:', error);
      }
    };

    const fetchCommentLength = async () => {
      try {
        const response = await axios.get('http://localhost:11000/api/comments/length');
        commentLength.value = response.data.length;
      } catch (error) {
        console.error('获取评论长度失败:', error);
      }
    };

    const fetchImages = async () => {
      try {
        const response = await axios.get('http://localhost:11000/api/images');
        const { images: imagesData, labels: labelsData } = response.data;

        images.value = imagesData.map(image => ({
          id: image.id,
          name: image.name,
          price: image.price,
          num: image.num,
          produce: image.produce,
          src: `http://localhost:11000/api/image/${image.id}`,
          isFavorite: favoriteImages.value.includes(image.id), // 根据收藏状态设置 isFavorite 属性
          isInCart: cartImages.value.includes(image.id), // 根据购物车状态设置 isInCart 属性
          favorite: image.favorite || 0, // 收藏人数
          cart: image.cart || 0, // 加入购物车人数
          label: image.label // 添加标签属性
        }));
        filteredImages.value = images.value; // 初始化时显示所有图片

        // 获取所有标签
        labels.value = labelsData;
      } catch (error) {
        console.error('获取图片失败:', error);
      }
    };

    const searchImages = () => {
      const query = searchQuery.value.toLowerCase();
      filteredImages.value = images.value.filter(image => {
        const name = image.name.toLowerCase();
        return query.split(' ').every(word => name.includes(word));
      });
    };

    const showAllImages = () => {
      filteredImages.value = images.value;
    };

    const toggleFavorite = async (image) => {
      image.isFavorite = !image.isFavorite;
      if (image.isFavorite) {
        try {
          await axios.post('http://localhost:11000/api/favorite', {
            id: image.id,
            username: user.value.username  // 添加用户名到请求数据中
          });
          ElMessage.success('商品收藏成功');
          favoriteImages.value.push(image.id); // 更新收藏数量
          image.favorite += 1; // 更新收藏人数
        } catch (error) {
          console.error('收藏失败:', error);
          ElMessage.error('收藏失败');
        }
      } else {
        try {
          await axios.delete(`http://localhost:11000/api/favorite/${image.id}`, {
            params: { username: user.value.username }  // 添加用户名到请求参数中
          });
          ElMessage.success('取消收藏成功');
          favoriteImages.value = favoriteImages.value.filter(id => id !== image.id); // 更新收藏数量
          image.favorite -= 1; // 更新收藏人数
        } catch (error) {
          console.error('取消收藏失败:', error);
          ElMessage.error('取消收藏失败');
        }
      }
    };

    const toggleCart = async (image) => {
      image.isInCart = !image.isInCart;
      if (image.isInCart) {
        try {
          await axios.post('http://localhost:11000/api/shopping', {
            id: image.id,
            username: user.value.username  // 添加用户名到请求数据中
          });
          ElMessage.success('商品加入购物车成功');
          cartImages.value.push(image.id); // 更新购物车数量
          image.cart += 1; // 更新购物车人数
        } catch (error) {
          console.error('加入购物车失败:', error);
          ElMessage.error('加入购物车失败');
        }
      } else {
        try {
          await axios.delete(`http://localhost:11000/api/shopping/${image.id}`, {
            params: { username: user.value.username }  // 添加用户名到请求参数中
          });
          ElMessage.success('取消加入购物车成功');
          cartImages.value = cartImages.value.filter(id => id !== image.id); // 更新购物车数量
          image.cart -= 1; // 更新购物车人数
        } catch (error) {
          console.error('取消加入购物车失败:', error);
          ElMessage.error('取消加入购物车失败');
        }
      }
    };

    const handlePageChange = (page) => {
      currentPage.value = page;
    };

    return {
      user,
      getRoleType,
      isAdminOrManager,
      handleLogout,
      goToFavorites,
      goToCart,
      goToPurchaseHistory,
      images,
      filteredImages,
      favoriteImages,
      cartImages,
      purchaseHistoryCount,
      searchQuery,
      carouselImages,
      searchImages,
      showAllImages,
      toggleFavorite,
      toggleCart,
      goToComments,
      commentCount,
      commentLength,
      paginatedImages,
      handlePageChange,
      activeTab,
      labels,
      filterImagesByLabel,
      goToAddProduct,
      goToViewStock,
      goToSoldOut,
      stockLength,
      soldOutLength,
      goToViewComments,
      goToAddAdmin,
      goToChartOne,
      goToChartTwo,
      goToChartThree,
      goToChartFour,
      goToAdminInfo,
      User

    };
  }
};
</script>

<style scoped>
.full-screen {
  height: 100vh;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
}

.header {
  background: linear-gradient(to right, #616fff, #3949ab);
  padding: 0;
  height: 60px;
  line-height: 60px;
  color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.header-content h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 500;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-avatar {
  border: 2px solid rgba(255,255,255,0.8);
}

.username {
  font-size: 1rem;
  color: rgba(255,255,255,0.9);
}

.main-container {
  height: calc(100vh - 60px);
}

.content-container {
  background-color: #f6faff;
  padding: 20px;
}

.carousel-container {
  margin-bottom: 24px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.search-section {
  max-width: 800px;
  margin: 0 auto 24px;
}

.custom-search-bar {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 50px;
  padding: 8px 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.custom-search-bar:focus-within {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
  transform: translateY(-1px);
}

.custom-search-bar input {
  flex: 1;
  border: none;
  outline: none;
  padding: 8px;
  font-size: 16px;
  background: transparent;
}

.search-button {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 8px;
  color: #606266;
  display: flex;
  align-items: center;
  transition: color 0.3s ease;
}

.search-button:hover {
  color: #409EFF;
}

.el-main{
  overflow: hidden;
  position: relative;
}

.cards-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}

.right-aside {
  padding: 0 0 0 20px;
  position: sticky;
  top: 80px;
}

.custom-tabs {
  margin: 0 auto 24px;
  padding: 0 16px;
}

.tabs-wrapper {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  justify-content: center;
  padding: 8px 0;
  scrollbar-width: none; /* Firefox */
  -ms-overflow-style: none; /* IE and Edge */
}

.tabs-wrapper::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

.tab-button {
  background: transparent;
  border: none;
  padding: 8px 20px;
  border-radius: 50px;
  font-size: 14px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.3s ease;
  color: #606266;
  position: relative;
}

.tab-button:hover {
  color: #409EFF;
  background: rgba(64, 158, 255, 0.1);
}

.tab-button.active {
  background: #409EFF;
  color: white;
  font-weight: 500;
}

.tab-button.active::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 50%;
  transform: translateX(-50%);
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: #409EFF;
}

.image-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.image-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
}

.el-container {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.el-container > .el-container {
  flex: 1;
  display: flex;
  flex-direction: row;
}

.aside {
  background-color: #fff;
  padding: 1rem;
  box-shadow: var(--card-shadow);
  height: 100%;
}
:deep(.el-menu){
  border: none;
}
.main {
  background-color: white;
  padding: 1rem;
  box-shadow: var(--card-shadow);
  border-radius: 8px;
  flex: 1;
  margin-left: 1rem;
}

.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  padding: 24px;
}

.image-card {
  border: none;
  transition: all 0.3s ease;
  height: 100%;
}

.image-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

.card-image-wrapper {
  position: relative;
  padding-top: 75%; /* 4:3 宽高比 */
  overflow: hidden;
  border-radius: 8px;
}

.card-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.image-card:hover .card-image {
  transform: scale(1.05);
}

.card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  background: linear-gradient(to bottom, transparent 50%, rgba(0, 0, 0, 0.4));
  opacity: 0;
  transition: opacity 0.3s ease;
  display: flex;
  align-items: flex-end;
  padding: 20px;
}

.image-card:hover .card-overlay {
  opacity: 1;
}

.card-actions {
  display: flex;
  gap: 12px;
  
}

.card-actions .el-button {
  background: rgba(255, 255, 255, 0.9);
  border: none;
}

.card-actions .is-favorite {
  color: #f7ba2a;
}

.card-actions .in-cart {
  color: #409EFF;
}

.card-content {
  padding: 16px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.card-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: #303133;
}

.card-price {
  font-size: 1.2rem;
  font-weight: 600;
  color: #f56c6c;
}

.card-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.stats-info {
  display: flex;
  gap: 12px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #909399;
  font-size: 0.9rem;
}

.card-description {
  font-size: 0.9rem;
  color: #606266;
  line-height: 1.5;
  margin-top: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 32px;
  padding-bottom: 24px;
}

@media (max-width: 768px) {
  .card-container {
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 16px;
    padding: 16px;
  }
  
  .card-title {
    font-size: 1rem;
  }
  
  .card-price {
    font-size: 1.1rem;
  }
}

.welcome-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: var(--card-shadow);
}

.avatar {
  margin-bottom: 1rem;
}

.user-info {
  text-align: center;
}

.role-tag {
  margin-top: 0.5rem;
}

.logout-btn {
  margin-top: 1rem;
  background-color: #f56c6c;
  border-color: #f56c6c;
}

.logout-btn:hover {
  background-color: #f78989;
  border-color: #f78989;
}

.favorites-btn {
  margin-top: 1rem;
  color: #409EFF;
}

.favorites-btn:hover {
  color: #66b1ff;
}

.cart-btn {
  margin-top: 1rem;
  color: #409EFF;
}

.cart-btn:hover {
  color: #66b1ff;
}

.demonstration {
  color: var(--el-text-color-secondary);
}

.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
  text-align: center;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  background-color: #d3dce6;
}

.favorite-container,
.cart-container {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.favorite-container .favorite,
.cart-container .in-cart {
  color: gold;
  margin-right: 0.5rem;
}

.search-bar {
  margin: 1rem;
}

.tabs-container {
  display: flex;
  justify-content: center;
  width: 100%;
}

.add-product-btn {
  margin-top: 1rem;
}

.el-menu-item {
  height: 56px;
  line-height: 56px;
  padding: 0 20px;
  list-style: none;
  cursor: pointer;
  transition: border-color .3s,background-color .3s,color .3s;
}

.el-menu-item:hover {
  background-color: var(--el-menu-hover-bg-color);
}

.el-menu-item .el-icon {
  margin-right: 8px;
  width: 24px;
  text-align: center;
}

.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  padding: 1.5rem;
}

.image-card {
  transition: transform 0.2s, box-shadow 0.2s;
}

.image-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.welcome-card {
  background: #fff;
  padding: 1.5rem;
  border-radius: 12px;
}

.search-bar {
  max-width: 600px;
  margin: 1.5rem auto;
}

.tabs-container {
  margin: 1rem 0 2rem;
}
</style>