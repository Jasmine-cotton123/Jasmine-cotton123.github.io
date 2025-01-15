<template>
  <div class="auth-page">
    <div class="auth-container">
      <el-card class="auth-card">
        <el-form 
          class="auth-form" 
          :model="formData" 
          :rules="rules" 
          ref="loginForm"
          label-width="0"
        >
          <div class="form-header">
            <h2>欢迎登录</h2>
            <p>请输入您的账号信息</p>
          </div>
          
          <el-form-item prop="username">
            <el-input 
              v-model="formData.username" 
              :prefix-icon="User"
              placeholder="请输入用户名"
            />
          </el-form-item>
          
          <el-form-item prop="password">
            <el-input 
              type="password" 
              v-model="formData.password" 
              :prefix-icon="Lock"
              placeholder="请输入密码"
              show-password
              @keyup.enter="handleLogin"
            />
          </el-form-item>
          
          <el-form-item prop="role">
            <el-select 
              v-model="formData.role" 
              placeholder="请选择角色"
              style="width: 100%"
            >
              <el-option label="用户" value="user"></el-option>
              <el-option label="管理员" value="admin"></el-option>
              <el-option label="经理" value="manager"></el-option>
            </el-select>
          </el-form-item>
          
          <el-button 
            type="primary" 
            @click="handleLogin" 
            :loading="loading"
            class="submit-btn"
          >
            登录
          </el-button>
          
          <div class="form-footer">
            <router-link to="/register" class="register-link">
              还没有账号？立即注册
            </router-link>
          </div>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script>
import { login } from '../utils/request'
import { ElMessage } from 'element-plus'
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { 
  User, 
  Lock,
  UserFilled,
  Management,
  Avatar
} from '@element-plus/icons-vue'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const loginForm = ref(null)
    const loading = ref(false)
    
    const formData = reactive({
      username: '',
      password: '',
      role: ''
    })
    
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度应在3-20个字符之间', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
      ],
      role: [
        { required: true, message: '请选择角色', trigger: 'change' }
      ]
    }
    
    const handleLogin = async () => {
      if (!loginForm.value) return
      
      try {
        await loginForm.value.validate()
        loading.value = true
        
        const response = await login(formData)
        
        if (response.message === "登录成功") {
          ElMessage.success('登录成功')
          localStorage.setItem('user', JSON.stringify({
            username: response.username,
            role: response.role
          }))
          router.push('/Shouye')
        }
      } catch (error) {
        console.error('登录错误:', error)
        ElMessage.error('登录失败，请检查用户名和密码')
      } finally {
        loading.value = false
      }
    }
    
    return {
      loginForm,
      loading,
      rules,
      handleLogin,
      formData,
      User,
      Lock,
      UserFilled,
      Management,
      Avatar
    }
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.auth-container {
  width: 100%;
  max-width: 420px;
  padding: 20px;
}

.auth-card {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.auth-form {
  padding: 20px;
}

.form-header {
  text-align: center;
  margin-bottom: 30px;
}

.form-header h2 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.form-header p {
  margin: 8px 0 0;
  color: #909399;
  font-size: 14px;
}

:deep(.el-input__wrapper) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

:deep(.el-select .el-input__wrapper) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

:deep(.el-select-dropdown__item) {
  display: flex;
  align-items: center;
  gap: 8px;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  margin-top: 16px;
}

.form-footer {
  margin-top: 16px;
  text-align: center;
}

.register-link {
  color: #409EFF;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s;
}

.register-link:hover {
  color: #66b1ff;
}

@media (max-width: 480px) {
  .auth-container {
    padding: 10px;
  }
  
  .auth-form {
    padding: 15px;
  }
}
</style>