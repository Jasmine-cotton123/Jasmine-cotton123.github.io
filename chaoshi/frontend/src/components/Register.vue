<template>
  <div class="auth-page">
    <div class="auth-container">
      <el-card class="auth-card">
        <el-form 
          class="auth-form" 
          :model="formData" 
          :rules="rules" 
          ref="registerForm"
          label-width="70px"
        >
          <div class="form-header">
            <h2>创建账号</h2>
            <p>请填写注册信息</p>
          </div>
          
          <el-form-item prop="username" label="用户名">
            <el-input 
              v-model="formData.username" 
              :prefix-icon="User"
              placeholder="请输入用户名"
            />
          </el-form-item>
          
          <el-form-item prop="role" label="角色">
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
          
          <el-form-item prop="phone" label="手机号">
            <el-input 
              v-model="formData.phone" 
              :prefix-icon="Iphone"
              placeholder="请输入手机号码"
            />
          </el-form-item>
          
          <el-form-item prop="password" label="密码">
            <el-input 
              type="password" 
              v-model="formData.password" 
              :prefix-icon="Lock"
              placeholder="请输入密码"
              show-password
            />
          </el-form-item>
          
          <el-button 
            type="primary" 
            @click="handleRegister" 
            :loading="loading"
            class="submit-btn"
          >注册
          </el-button>
          
          <div class="form-footer">
            <router-link to="/login" class="login-link">
              已有账号？立即登录
            </router-link>
          </div>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script>
import { register } from '../utils/request'
import { ElMessage } from 'element-plus'
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { 
  User, 
  Lock,
  Iphone,
  UserFilled,
  Management,
  Avatar
} from '@element-plus/icons-vue'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    const registerForm = ref(null)
    const loading = ref(false)
    
    const formData = reactive({
      username: '',
      password: '',
      role: '',
      phone: ''
    })
    
    const validatePhone = (rule, value, callback) => {
      const phoneRegex = /^1[3-9]\d{9}$/
      if (!value) {
        callback(new Error('请输入手机号码'))
      } else if (!phoneRegex.test(value)) {
        callback(new Error('请输入正确的手机号码'))
      } else {
        callback()
      }
    }
    
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
      ],
      phone: [
        { required: true, validator: validatePhone, trigger: 'blur' }
      ]
    }
    
    const handleRegister = async () => {
      if (!registerForm.value) return
      
      try {
        await registerForm.value.validate()
        loading.value = true
        
        const response = await register(formData)
        
        if (response.message === "注册成功") {
          ElMessage.success('注册成功')
          router.push('/login')
        }
      } catch (error) {
        console.error('注册错误:', error)
      } finally {
        loading.value = false
      }
    }
    
    return {
      registerForm,
      loading,
      rules,
      handleRegister,
      formData,
      User,
      Lock,
      Iphone,
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

:deep(.el-form-item__label) {
  padding-bottom: 8px;
  font-weight: 500;
}

:deep(.el-input__wrapper) {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.submit-btn {
  width: 100%;
  padding: 12px;
  font-size: 16px;
}

.form-footer {
  margin-top: 16px;
  text-align: center;
}

.login-link {
  color: #409EFF;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s;
}

.login-link:hover {
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