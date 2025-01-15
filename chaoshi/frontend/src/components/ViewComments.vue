<template>
  <div class="view-stock-container">
    <div class="page-header">
      <el-button @click="goBack" type="primary" plain class="back-button">
        <el-icon><Back /></el-icon> 返回
      </el-button>
      <h2>评论信息</h2>
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
          <el-option label="评论人数（从小到大）" value="commentCountAsc" />
          <el-option label="评论人数（从大到小）" value="commentCountDesc" />
        </el-select>
      </div>

      <el-table
        :data="filteredComments"
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

        <el-table-column 
          v-for="i in maxCommentCount" 
          :key="i" 
          :label="`评论${i}`" 
          min-width="200"
          show-overflow-tooltip
        >
          <template #default="{ row }">
            <div v-if="row['comment' + i]" class="comment-content">
              <el-avatar 
                :size="24" 
                :src="`https://api.dicebear.com/7.x/micah/svg?seed=${row['username' + i]}`"
                class="comment-avatar"
              />
              <div class="comment-text">
                <span class="username">{{ row['username' + i] }}</span>
                <p class="comment">{{ row['comment' + i] }}</p>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button 
              type="primary" 
              size="small" 
              @click="viewDetails(row.name)"
            >
              <el-icon><View /></el-icon>
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { 
  Back, 
  Search, 
  Picture,
  View 
} from '@element-plus/icons-vue'

export default {
  name: 'ViewComments',
  components: {
    Back,
    Search,
    Picture,
    View
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const comments = ref([]);
    const sortKey = ref('name');
    const sortOrder = ref('ascending');
    const searchQuery = ref('');
    const maxCommentCount = ref(0);

    const fetchComments = async () => {
      try {
        const response = await axios.get('http://localhost:11000/api/comments');
        const formattedComments = response.data.map(comment => {
          const formattedComment = { name: comment.name, src: comment.src, commentCount: 0 };
          let i = 1;
          while (comment[`username${i}`] && comment[`comment${i}`]) {
            formattedComment[`username${i}`] = comment[`username${i}`];
            formattedComment[`comment${i}`] = comment[`comment${i}`];
            formattedComment.commentCount++;
            i++;
          }
          maxCommentCount.value = Math.max(maxCommentCount.value, i - 1);
          return formattedComment;
        });
        comments.value = formattedComments;
      } catch (error) {
        console.error('获取评论信息失败:', error);
      }
    };

    onMounted(() => {
      fetchComments();
    });

    watch(route, (to, from) => {
      if (to.query.refresh) {
        fetchComments();
      }
    });

    const goBack = () => {
      router.push('/Shouye');
    };

    const handleSortChange = ({ prop, order }) => {
      sortKey.value = prop;
      sortOrder.value = order === 'ascending' ? 'asc' : 'desc';
    };

    const sortedComments = computed(() => {
      return [...comments.value].sort((a, b) => {
        if (sortKey.value === 'commentCountAsc') {
          return a.commentCount - b.commentCount;
        } else if (sortKey.value === 'commentCountDesc') {
          return b.commentCount - a.commentCount;
        } else {
          return sortOrder.value === 'asc' ? a[sortKey.value].localeCompare(b[sortKey.value]) : b[sortKey.value].localeCompare(a[sortKey.value]);
        }
      });
    });

    const filteredComments = computed(() => {
      return sortedComments.value.filter(comment =>
        comment.name.toLowerCase().includes(searchQuery.value.toLowerCase())
      );
    });

    const viewDetails = (name) => {
      router.push({ path: '/comment-details', query: { name } });
    };

    return {
      comments,
      goBack,
      sortKey,
      sortOrder,
      searchQuery,
      sortedComments,
      filteredComments,
      handleSortChange,
      maxCommentCount,
      viewDetails
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

.comment-content {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 8px;
  background: #f8f9fa;
  border-radius: 4px;
}

.comment-avatar {
  flex-shrink: 0;
}

.comment-text {
  flex: 1;
  min-width: 0;
}

.username {
  font-weight: bold;
  color: #409EFF;
  font-size: 0.9rem;
}

.comment {
  margin: 4px 0 0;
  font-size: 0.9rem;
  color: #606266;
  word-break: break-word;
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