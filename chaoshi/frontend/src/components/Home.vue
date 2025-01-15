<template>
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const user = ref(null)

const getRoleType = computed(() => {
  switch (user.value?.role) {
    case 'admin':
      return 'danger'
    case 'manager':
      return 'warning'
    default:
      return 'success'
  }
})

onMounted(() => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    user.value = JSON.parse(userStr)
  } else {
    router.push('/login')
  }
})

const handleLogout = () => {
  localStorage.removeItem('user')
  ElMessage.success('已退出登录')
  router.push('/login')
}
</script>

<style scoped>
.welcome-card {
  width: 90%;
  max-width: 360px;
  margin: 2rem auto;
  padding: 2rem;
  text-align: center;
  animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.avatar {
  border: 4px solid #eef2ff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 1.5rem;
  transition: transform 0.3s ease;
}

.avatar:hover {
  transform: scale(1.05);
}

.user-info {
  margin-bottom: 1.5rem;
}

.user-info h1 {
  color: #4b5563;
  font-size: 1.2rem;
  margin: 0;
  font-weight: 500;
}

.user-info h2 {
  color: #1f2937;
  font-size: 1.5rem;
  margin: 0.5rem 0 1rem;
  font-weight: 600;
}

.role-tag {
  font-size: 0.9rem;
  padding: 0.4rem 1.2rem;
  border-radius: 20px;
  font-weight: 500;
}

.logout-btn {
  width: 100%;
  padding: 0.8rem;
  font-size: 1rem;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

@media (max-width: 480px) {
  .welcome-card {
    padding: 1.5rem;
  }

  .avatar {
    margin-bottom: 1rem;
  }

  .user-info h1 {
    font-size: 1.1rem;
  }

  .user-info h2 {
    font-size: 1.3rem;
  }
}
</style> 