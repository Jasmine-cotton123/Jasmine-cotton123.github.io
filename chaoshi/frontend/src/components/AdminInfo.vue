<template>
    <div class="page-container">
      <div class="page-header">
        <el-button @click="goBack" type="primary" plain class="back-button">
          <el-icon><Back /></el-icon> 返回
        </el-button>
        <h2 class="header-title">管理员信息</h2>
      </div>
      <div class="table-container">
        <el-table :data="adminList" style="width: 50%; margin: 0 auto;">
          <el-table-column prop="username" label="用户名" width="180"></el-table-column>
          <el-table-column prop="phone" label="电话" width="180"></el-table-column>
          <el-table-column prop="role" label="角色" width="180"></el-table-column>
          <el-table-column prop="password" label="密码" width="180"></el-table-column>
          <el-table-column label="操作" width="180">
            <template #default="scope">
              <el-button @click="goToEditAdmin(scope.row)" type="primary" size="small">修改</el-button>
              <el-button @click="deleteAdmin(scope.row)" type="danger" size="small">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  import { ElMessage, ElMessageBox } from 'element-plus'
  import { useRouter } from 'vue-router'
  import { Back } from '@element-plus/icons-vue'
  
  export default {
    name: 'AdminInfo',
    components: {
      Back
    },
    setup() {
      const router = useRouter()
      const adminList = ref([])
  
      const fetchAdminInfo = async () => {
        try {
          const response = await axios.get('http://localhost:11000/api/admins')
          adminList.value = response.data
        } catch (error) {
          console.error('获取管理员信息失败:', error)
          ElMessage.error('获取管理员信息失败')
        }
      }
  
      const goToEditAdmin = (admin) => {
        router.push({ name: 'EditAdmin', params: { username: admin.username } })
      }
  
      const deleteAdmin = (admin) => {
        ElMessageBox.confirm('确定要删除这个管理员吗?', '删除管理员', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          axios.delete(`http://localhost:11000/api/admin/${admin.username}`)
            .then(() => {
              ElMessage.success('管理员删除成功')
              fetchAdminInfo()
            })
            .catch(error => {
              console.error('删除管理员失败:', error)
              ElMessage.error('删除管理员失败')
            })
        }).catch(() => {
          ElMessage.info('取消删除')
        })
      }
  
      const goBack = () => {
        router.push('/Shouye')
      }
  
      onMounted(fetchAdminInfo)
  
      return {
        adminList,
        goToEditAdmin,
        deleteAdmin,
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
  
  .table-container {
    display: flex;
    justify-content: center;
  }
  
  .el-table {
    width: 80%;
    margin: 0 auto;
  }
  </style>