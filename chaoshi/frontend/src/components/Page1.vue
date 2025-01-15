<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" type="primary" plain class="back-button">
          <el-icon><Back /></el-icon> 返回
        </el-button>
        <h2>商品分类统计</h2>
      </div>
      <el-select 
        v-model="selectedLabel" 
        placeholder="选择标签" 
        class="label-select"
      >
        <el-option
          v-for="label in labels"
          :key="label"
          :label="label"
          :value="label"
        />
      </el-select>
    </div>

    <div class="content-container">
      <el-card class="chart-card">
        <div id="pie-chart" class="pie-chart"></div>
      </el-card>

      <el-card class="table-card">
        <template #header>
          <div class="card-header">
            <span>商品列表</span>
            <span class="total-count">共 {{ filteredProducts.length }} 件商品</span>
          </div>
        </template>
        
        <el-table 
          :data="filteredProducts" 
          style="width: 100%"
          :header-cell-style="{ background: '#f5f7fa' }"
          height="calc(100vh - 500px)"
        >
          <el-table-column prop="name" label="商品名称" min-width="150" show-overflow-tooltip />
          <el-table-column prop="price" label="价格" width="120">
            <template #default="{ row }">
              <span class="price">￥{{ row.price }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="num" label="库存" width="100">
            <template #default="{ row }">
              <el-tag :type="row.num > 0 ? 'success' : 'danger'" size="small">
                {{ row.num }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="produce" label="商品介绍" min-width="200" show-overflow-tooltip />
          <el-table-column prop="label" label="标签" width="120">
            <template #default="{ row }">
              <el-tag>{{ row.label }}</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import * as echarts from 'echarts'
import { ref, onMounted, computed } from 'vue'
import { Back } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

export default {
  name: 'Page1',
  components: {
    Back
  },
  setup() {
    const router = useRouter()
    const products = ref([])
    const labels = ref([])
    const selectedLabel = ref('')
    let pieChart = null

    const filteredProducts = computed(() => {
      if (selectedLabel.value && selectedLabel.value !== '全部') {
        return products.value.filter(product => product.label === selectedLabel.value)
      }
      return products.value
    })

    const initPieChart = () => {
      const pieChartDom = document.getElementById('pie-chart')
      pieChart = echarts.init(pieChartDom)

      const pieOption = {
        title: {
          text: '商品分类占比',
          subtext: '按标签统计',
          left: 'center',
          top: 20,
          textStyle: {
            fontSize: 18,
            fontWeight: 'normal'
          },
          subtextStyle: {
            fontSize: 14,
            color: '#909399'
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c} 件 ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          top: 'middle'
        },
        series: [
          {
            name: '商品分类',
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['60%', '50%'],
            avoidLabelOverlap: true,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: false
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 14,
                fontWeight: 'bold'
              },
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            },
            data: []
          }
        ]
      }

      pieChart.setOption(pieOption)
    }

    const goBack = () => {
      router.go(-1)
    }

    onMounted(async () => {
      initPieChart()

      try {
        const [labelsResponse, productsResponse] = await Promise.all([
          axios.get('http://localhost:11000/api/labels-products'),
          axios.get('http://localhost:11000/api/products')
        ])

        const { labels: labelData } = labelsResponse.data
        products.value = productsResponse.data

        // 更新饼图数据
        const pieData = labelData.map(label => ({
          value: label.count,
          name: label.name
        }))
        pieChart.setOption({
          series: [{
            data: pieData
          }]
        })

        // 设置标签选项
        labels.value = ['全部', ...labelData.map(label => label.name)]
      } catch (error) {
        console.error('获取数据失败:', error)
      }
    })

    return {
      products,
      labels,
      selectedLabel,
      filteredProducts,
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
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 500;
}

.label-select {
  width: 200px;
}

.content-container {
  display: grid;
  gap: 20px;
  grid-template-columns: 1fr;
}

.chart-card {
  margin-bottom: 20px;
}

.pie-chart {
  height: 400px;
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.total-count {
  color: #909399;
  font-size: 14px;
}

.price {
  color: #ff4500;
  font-weight: bold;
}

:deep(.el-table__header) {
  background-color: #f5f7fa;
}

:deep(.el-table) {
  --el-table-border-color: #ebeef5;
  --el-table-header-background-color: #f5f7fa;
}

@media (min-width: 1200px) {
  .content-container {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .chart-card {
    margin-bottom: 0;
  }
}

.header-left {
  display: flex;
  align-items: center;
  gap: 15px;
}

.back-button {
  padding: 8px 15px;
}
</style>