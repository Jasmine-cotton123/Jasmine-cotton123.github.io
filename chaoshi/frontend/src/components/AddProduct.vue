<template>
  <div class="add-product-container">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" type="primary" plain class="back-button">
          <el-icon><Back /></el-icon> 返回
        </el-button>
        <h2>添加商品</h2>
      </div>
    </div>

    <el-card class="box-card">
      <el-form 
        :model="formData" 
        :rules="rules" 
        ref="productForm" 
        label-width="80px"
        @submit.prevent
      >
        <el-form-item label="商品名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入商品名称"></el-input>
        </el-form-item>

        <el-form-item label="数量" prop="num">
          <el-input-number 
            v-model="formData.num" 
            :min="1" 
            controls-position="right"
          ></el-input-number>
        </el-form-item>

        <el-form-item label="价格" prop="price">
          <el-input-number 
            v-model="formData.price" 
            :min="0" 
            :precision="2" 
            :step="0.1" 
            controls-position="right"
          ></el-input-number>
        </el-form-item>

        <el-form-item label="商品介绍" prop="produce">
          <el-input v-model="formData.produce" placeholder="请输入商品介绍"></el-input>
        </el-form-item>

        <el-form-item label="标签" prop="label">
          <el-input v-model="formData.label" placeholder="请输入标签"></el-input>
        </el-form-item>

        <el-form-item label="图片" prop="image">
          <el-upload
            ref="uploadRef"
            class="upload-demo"
            action="#"
            :auto-upload="false"
            :on-change="onFileChange"
            :on-remove="handleRemove"
            :before-upload="beforeUpload"
            :limit="1"
            drag
            :show-file-list="false"
          >
            <template v-if="imageUrl">
              <div class="image-preview-container">
                <img :src="imageUrl" class="preview-image" />
                <div class="image-preview-mask" @click.stop="handleRemove">
                  <el-icon><Delete /></el-icon>
                  <span>点击更换图片</span>
                </div>
              </div>
            </template>
            <template v-else>
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                将文件拖到此处，或<em>点击上传</em>
              </div>
            </template>
            <template #tip>
              <div class="el-upload__tip">
                只能上传 jpg/png 文件，且不超过 2MB
              </div>
            </template>
          </el-upload>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm">添加商品</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { ElMessage } from 'element-plus'
import { Back, UploadFilled, Delete } from '@element-plus/icons-vue'

export default {
  components: {
    Back,
    UploadFilled,
    Delete
  },
  data() {
    return {
      formData: {
        name: '',
        num: 1,
        price: 0,
        produce: '',
        label: '',
        image: null,
      },
      imageUrl: '',
      rules: {
        name: [
          { required: true, message: '请输入商品名称', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        num: [
          { required: true, message: '请输入数量', trigger: 'blur' }
        ],
        price: [
          { required: true, message: '请输入价格', trigger: 'blur' }
        ],
        produce: [
          { required: true, message: '请输入生产地', trigger: 'blur' }
        ],
        label: [
          { required: true, message: '请输入标签', trigger: 'blur' }
        ],
        image: [
          { required: true, message: '请上传图片', trigger: 'change' }
        ]
      }
    };
  },
  methods: {
    goBack() {
      this.$router.back()
    },
    beforeUpload(file) {
      const isImage = file.type.startsWith('image/')
      if (!isImage) {
        ElMessage.error('只能上传图片文件！')
        return false
      }
      
      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isLt2M) {
        ElMessage.error('图片大小不能超过 2MB!')
        return false
      }
      
      return true
    },
    onFileChange(file) {
      if (this.beforeUpload(file.raw)) {
        // 清理旧的预览
        this.handleRemove()
        
        this.formData.image = file.raw
        this.imageUrl = URL.createObjectURL(file.raw)
      }
    },
    handleRemove() {
      if (this.imageUrl) {
        URL.revokeObjectURL(this.imageUrl)
        this.imageUrl = ''
      }
      this.formData.image = null
      if (this.$refs.uploadRef) {
        this.$refs.uploadRef.clearFiles()
      }
    },
    submitForm() {
      if (!this.$refs.productForm) return;
      
      this.$refs.productForm.validate((valid) => {
        if (valid) {
          this.handleSubmit();
        } else {
          return false;
        }
      });
    },
    async handleSubmit() {
      try {
        const formData = new FormData();
        Object.keys(this.formData).forEach(key => {
          formData.append(key, this.formData[key]);
        });

        const response = await fetch('http://localhost:11000/api/add-product', {
          method: 'POST',
          body: formData,
        });
        
        const result = await response.json();
        if (response.ok) {
          ElMessage.success('商品添加成功');
          setTimeout(() => {
            this.$router.back();
          }, 1000);
        } else {
          ElMessage.error(`添加商品失败: ${result.message}`);
        }
      } catch (error) {
        console.error('添加商品错误:', error);
        ElMessage.error('添加商品失败');
      }
    },
    resetForm() {
      if (this.$refs.productForm) {
        this.$refs.productForm.resetFields()
        this.handleRemove()
      }
    }
  }
};
</script>

<style scoped>
.add-product-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 20px;
  width: 100%;
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
}

.box-card {
  margin-top: 20px;
}

.el-form-item {
  margin-bottom: 20px;
}

.upload-demo {
  width: 100%;
  margin-top: 10px;
}

.preview-image {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
}

.el-upload {
  width: 100%;
}

.el-upload-dragger {
  width: 100%;
  height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.el-icon--upload {
  margin: 20px 0 16px;
  font-size: 48px;
  color: #409EFF;
}

.el-upload__text {
  margin: 0 0 16px;
  color: #606266;
  font-size: 14px;
}

.el-upload__text em {
  color: #409EFF;
  font-style: normal;
}

.el-upload__tip {
  color: #909399;
  font-size: 12px;
  margin-top: 5px;
}

@media (max-width: 768px) {
  .add-product-container {
    padding: 10px;
  }
  
  .box-card {
    margin-top: 10px;
  }
}

.image-preview-container {
  position: relative;
  width: 200px;
  height: 200px;
  margin: 0 auto;
}

.image-preview-mask {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #fff;
  opacity: 0;
  transition: opacity 0.3s;
  cursor: pointer;
  border-radius: 4px;
}

.image-preview-mask:hover {
  opacity: 1;
}

.image-preview-mask .el-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}
</style>