<template>
    <div class="page-container">
      <div class="page-header">
        <el-button @click="goBack" type="primary" plain class="back-button">
          <el-icon><Back /></el-icon> 返回
        </el-button>
        <h2 class="header-title">修改管理员信息</h2>
      </div>
      <el-form :model="editForm" class="form-container">
        <el-form-item label="用户名">
          <el-input v-model="editForm.username"></el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="editForm.password" type="password"></el-input>
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="editForm.phone"></el-input>
        </el-form-item>
      </el-form>
      <div class="form-footer">
        <el-button @click="goBack">取消</el-button>
        <el-button type="primary" @click="editAdmin">确定</el-button>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  import { ElMessage } from 'element-plus'
  import { useRoute, useRouter } from 'vue-router'
  import { Back } from '@element-plus/icons-vue'
  
  export default {
    name: 'EditAdmin',
    components: {
      Back
    },
    setup() {
      const route = useRoute()
      const router = useRouter()
      const editForm = ref({
        username: '',
        password: '',
        phone: ''
      })
  
      const fetchAdminInfo = async () => {
        try {
          const response = await axios.get(`http://localhost:11000/api/admin/${route.params.username}`)
          editForm.value = response.data
        } catch (error) {
          console.error('获取管理员信息失败:', error)
          ElMessage.error('获取管理员信息失败')
        }
      }
  
      const editAdmin = async () => {
        try {
          await axios.put(`http://localhost:11000/api/admin/${route.params.username}`, editForm.value)
          ElMessage.success('管理员信息修改成功')
          router.push({ name: 'AdminInfo' })
        } catch (error) {
          console.error('修改管理员信息失败:', error)
          ElMessage.error('修改管理员信息失败')
        }
      }
  
      const goBack = () => {
        router.push({ name: 'AdminInfo' })
      }
  
      onMounted(fetchAdminInfo)
  
      return {
        editForm,
        editAdmin,
        goBack
      }
    }
  }
  </script>
  
  <style scoped>
  .page-container {
    padding: 20px;
  }
  
  .page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
  }
  
  .back-button {
    padding: 8px 15px;
  }
  
  .header-title {
    margin: 0;
    font-size: 20px;
    font-weight: 500;
    text-align: center;
    flex-grow: 1;
  }
  
  .form-container {
    width: 50%;
    margin: 0 auto;
  }
  
  .form-footer {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 20px;
  }
  </style>