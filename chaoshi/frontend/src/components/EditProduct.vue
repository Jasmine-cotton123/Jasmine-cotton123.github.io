<template>
  <div class="add-product-container">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" type="primary" plain class="back-button">
          <el-icon><Back /></el-icon> 返回
        </el-button>
        <h2>修改商品</h2>
      </div>
    </div>

    <el-card class="box-card">
      <el-form 
        ref="productForm"
        :model="product" 
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="商品名称" prop="name">
          <el-input v-model="product.name" placeholder="请输入商品名称"></el-input>
        </el-form-item>

        <el-form-item label="数量" prop="num">
          <el-input-number 
            v-model="product.num" 
            :min="1" 
            controls-position="right"
          ></el-input-number>
        </el-form-item>

        <el-form-item label="价格" prop="price">
          <el-input-number 
            v-model="product.price" 
            :min="0" 
            :precision="2" 
            :step="0.1" 
            controls-position="right"
          ></el-input-number>
        </el-form-item>

        <el-form-item label="生产地" prop="produce">
          <el-input v-model="product.produce" placeholder="请输入生产地"></el-input>
        </el-form-item>

        <el-form-item label="标签" prop="label">
          <el-input v-model="product.label" placeholder="请输入标签"></el-input>
        </el-form-item>

        <el-form-item label="图片" prop="image">
          <el-upload
            ref="uploadRef"
            class="upload-demo"
            action="#"
            :auto-upload="false"
            :on-change="onFileChange"
            :show-file-list="false"
            drag
          >
            <template v-if="newImageUrl || product.src">
              <div class="image-preview-container">
                <img 
                  :src="newImageUrl || product.src" 
                  class="preview-image"
                />
                <div class="image-preview-mask" @click.stop="handleRemoveImage">
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
          <el-button 
            type="primary" 
            :loading="loading"
            @click="submitForm"
          >
            <el-icon><Check /></el-icon>保存修改
          </el-button>
          <el-button @click="goBack">
            <el-icon><Close /></el-icon>取消修改
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { 
  Back, 
  UploadFilled, 
  Delete,
  Check,
  Close 
} from '@element-plus/icons-vue'

export default {
  name: 'EditProduct',
  components: {
    Back,
    UploadFilled,
    Delete,
    Check,
    Close
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const productForm = ref(null)
    const loading = ref(false)
    const product = ref({})
    const originalProduct = ref({})
    const newImage = ref(null)
    const newImageUrl = ref(null)

    const rules = {
      name: [
        { required: true, message: '请输入商品名称', trigger: 'blur' },
        { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
      ],
      price: [
        { required: true, message: '请输入价格', trigger: 'blur' }
      ],
      num: [
        { required: true, message: '请输入数量', trigger: 'blur' }
      ],
      label: [
        { required: true, message: '请输入标签', trigger: 'blur' }
      ],
      produce: [
        { required: true, message: '请输入商品介绍', trigger: 'blur' }
      ]
    }

    const fetchProduct = async () => {
      try {
        const response = await axios.get(`http://localhost:11000/api/product/${route.params.name}`)
        product.value = response.data
        originalProduct.value = { ...response.data }
      } catch (error) {
        console.error('获取商品信息失败:', error)
        ElMessage.error('获取商品信息失败')
      }
    }

    const onFileChange = (file) => {
      const isImage = file.raw.type.startsWith('image/')
      if (!isImage) {
        ElMessage.error('只能上传图片文件！')
        return false
      }
      
      const isLt2M = file.raw.size / 1024 / 1024 < 2
      if (!isLt2M) {
        ElMessage.error('图片大小不能超过 2MB!')
        return false
      }

      newImage.value = file.raw
      newImageUrl.value = URL.createObjectURL(file.raw)
    }

    const handleRemoveImage = () => {
      if (newImageUrl.value) {
        URL.revokeObjectURL(newImageUrl.value)
      }
      newImage.value = null
      newImageUrl.value = null
    }

    const submitForm = async () => {
      if (!productForm.value) return
      
      try {
        await productForm.value.validate()
        await updateProduct()
      } catch (error) {
        console.error('表单验证失败:', error)
      }
    }

    const updateProduct = async () => {
      // 检查是否有修改
      if (
        product.value.name === originalProduct.value.name &&
        product.value.price === originalProduct.value.price &&
        product.value.num === originalProduct.value.num &&
        product.value.produce === originalProduct.value.produce &&
        product.value.label === originalProduct.value.label &&
        !newImage.value
      ) {
        ElMessage.warning('信息未修改')
        return
      }

      loading.value = true
      try {
        const formData = new FormData()
        formData.append('name', product.value.name)
        formData.append('price', product.value.price)
        formData.append('num', product.value.num)
        formData.append('produce', product.value.produce)
        formData.append('label', product.value.label)
        if (newImage.value) {
          formData.append('image', newImage.value)
        }

        const response = await axios.put(
          `http://localhost:11000/api/product/${route.params.name}`,
          formData,
          {
            headers: { 'Content-Type': 'multipart/form-data' }
          }
        )

        if (response.data.message === '修改成功') {
          ElMessage.success('修改成功')
          setTimeout(() => {
            router.push({ 
              name: 'ViewStock', 
              query: { refresh: new Date().getTime() } 
            })
          }, 1000)
        } else {
          ElMessage.error('修改失败')
        }
      } catch (error) {
        console.error('修改商品信息失败:', error)
        ElMessage.error('修改失败')
      } finally {
        loading.value = false
      }
    }

    const goBack = () => {
      ElMessage.info('已取消修改')
      setTimeout(() => {
        router.go(-1)
      }, 500)
    }

    onMounted(() => {
      fetchProduct()
    })

    return {
      productForm,
      product,
      rules,
      loading,
      newImageUrl,
      onFileChange,
      handleRemoveImage,
      submitForm,
      goBack
    }
  }
}
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

.image-preview-container {
  position: relative;
  width: 200px;
  height: 200px;
  margin: 0 auto;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
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
</style>