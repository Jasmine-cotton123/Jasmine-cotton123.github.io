<template>
  <div class="add-admin">
    <el-container>
      <el-header class="header">
        <el-button type="text" class="back-btn" @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回
        </el-button>
        添加管理员
      </el-header>
      <el-main>
        <el-form :model="form" :rules="rules" ref="form" label-width="100px">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="form.username"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input type="password" v-model="form.password"></el-input>
          </el-form-item>
          <el-form-item label="电话" prop="phone">
            <el-input v-model="form.phone"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm('form')">添加管理员</el-button>
          </el-form-item>
        </el-form>
        <p v-if="message">{{ message }}</p>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus';
import { ArrowLeft } from '@element-plus/icons-vue';
import { useRouter } from 'vue-router';

export default {
  data() {
    const validatePhone = (rule, value, callback) => {
      const phoneRegex = /^[1][3-9]\d{9}$/;
      if (!value) {
        callback(new Error('请输入电话'));
      } else if (!phoneRegex.test(value)) {
        callback(new Error('请输入有效的电话号码'));
      } else {
        callback();
      }
    };

    return {
      form: {
        username: '',
        password: '',
        phone: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 20, message: '用户名长度应在3-20个字符之间', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
        ],
        phone: [
          { required: true, validator: validatePhone, trigger: 'blur' }
        ]
      },
      message: ''
    };
  },
  methods: {
    async submitForm(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          try {
            const response = await fetch('http://localhost:11000/api/add-admin', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify(this.form)
            });
            const data = await response.json();
            if (response.ok) {
              this.message = '管理员添加成功';
              ElMessage.success('管理员添加成功');
            } else {
              this.message = data.message || '添加管理员失败';
              ElMessage.error(this.message);
            }
          } catch (error) {
            this.message = '添加管理员失败';
            console.error('添加管理员错误:', error);
            ElMessage.error('添加管理员失败');
          }
        } else {
          console.log('表单验证失败');
          return false;
        }
      });
    },
    goBack() {
      this.$router.push('/Shouye');
    }
  },
  components: {
    ArrowLeft
  }
};
</script>

<style scoped>
.add-admin {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.add-admin h2 {
  text-align: center;
}
.header {
  background-color: var(--primary-color);
  color: white;
  text-align: center;
  font-size: 1.5rem;
  padding: 1rem;
  display: flex;
  align-items: center;
}
.back-btn {
  margin-right: 1rem;
}
</style>