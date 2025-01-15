import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const request = axios.create({
    baseURL: 'http://localhost:11000',  // API基础URL
    timeout: 5000,  // 请求超时时间
    headers: {
        'Content-Type': 'multipart/form-data'
    }
})

// 将对象转换为FormData
const objectToFormData = (obj) => {
    const formData = new FormData()
    Object.keys(obj).forEach(key => {
        formData.append(key, obj[key])
    })
    return formData
}

// 请求拦截器
request.interceptors.request.use(
    config => {
        // 如果是POST请求，将数据转换为FormData
        if (config.method === 'post' && config.data) {
            config.data = objectToFormData(config.data)
        }
        console.log('发送请求:', config)
        return config
    },
    error => {
        console.error('请求错误:', error)
        return Promise.reject(error)
    }
)

// 响应拦截器
request.interceptors.response.use(
    response => {
        const res = response.data
        
        // 如果响应成功但业务状态不成功
        if (response.status !== 200 && response.status !== 201) {
            ElMessage.error(res.message || '请求失败')
            return Promise.reject(new Error(res.message || '请求失败'))
        }
        
        return res
    },
    error => {
        console.error('响应错误:', error)
        const message = error.response?.data?.message || '请求失败，请稍后重试'
        ElMessage.error(message)
        return Promise.reject(error)
    }
)

// API请求函数
export const login = (data) => {
    return request({
        url: '/api/login',
        method: 'post',
        data
    })
}

export const register = (data) => {
    return request({
        url: '/api/register',
        method: 'post',
        data
    })
}

export default request 