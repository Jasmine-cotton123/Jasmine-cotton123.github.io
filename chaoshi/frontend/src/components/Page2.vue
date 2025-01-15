<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" type="primary" plain class="back-button">
          <el-icon><Back /></el-icon> 返回
        </el-button>
        <h2>商品销售统计</h2>
      </div>
    </div>

    <div class="content-container">
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>商品销售明细</span>
            <el-tooltip content="展示每个商品的库存数量和销售数量对比">
              <el-icon><InfoFilled /></el-icon>
            </el-tooltip>
          </div>
        </template>
        <div ref="chart1" class="chart"></div>
      </el-card>

      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>分类销售统计</span>
            <el-tooltip content="按商品分类统计库存和销售情况">
              <el-icon><InfoFilled /></el-icon>
            </el-tooltip>
          </div>
        </template>
        <div ref="chart2" class="chart"></div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'
import { Back, InfoFilled } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

export default {
  name: 'Page2',
  components: {
    Back,
    InfoFilled
  },
  setup() {
    const router = useRouter()
    const chart1 = ref(null)
    const chart2 = ref(null)
    let chartInstance1 = null
    let chartInstance2 = null

    const initChart1 = (data) => {
      const labels = data.map(item => item.name)
      const numData = data.map(item => item.num)
      const purchasedData = data.map(item => item.purchased)

      chartInstance1.setOption({
        title: {
          text: '商品库存与销量对比',
          textStyle: {
            fontSize: 16,
            fontWeight: 'normal'
          },
          top: 20
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['库存', '已售'],
          top: 20,
          right: 20
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: labels,
          axisLabel: {
            interval: 0,
            rotate: 30
          }
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '库存',
            type: 'bar',
            data: numData,
            itemStyle: {
              color: '#409EFF'
            }
          },
          {
            name: '已售',
            type: 'bar',
            data: purchasedData,
            itemStyle: {
              color: '#67C23A'
            }
          }
        ]
      })
    }

    const initChart2 = (labelProductMap) => {
      const labels = Object.keys(labelProductMap)
      const numData = labels.map(label => 
        labelProductMap[label].reduce((sum, product) => sum + product.num, 0)
      )
      const purchasedData = labels.map(label => 
        labelProductMap[label].reduce((sum, product) => sum + product.purchased, 0)
      )

      chartInstance2.setOption({
        title: {
          text: '分类销售统计',
          textStyle: {
            fontSize: 16,
            fontWeight: 'normal'
          },
          top: 20
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['库存', '已售'],
          top: 20,
          right: 20
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: labels
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '库存',
            type: 'bar',
            data: numData,
            itemStyle: {
              color: '#409EFF'
            }
          },
          {
            name: '已售',
            type: 'bar',
            data: purchasedData,
            itemStyle: {
              color: '#67C23A'
            }
          }
        ]
      })
    }

    const fetchData = async () => {
      try {
        const [productsRes, labelsRes] = await Promise.all([
          axios.get('http://localhost:11000/api/products'),
          axios.get('http://localhost:11000/api/labels-products')
        ])

        initChart1(productsRes.data)
        initChart2(labelsRes.data.label_product_map)
      } catch (error) {
        console.error('获取数据失败:', error)
      }
    }

    const goBack = () => {
      router.go(-1)
    }

    onMounted(() => {
      chartInstance1 = echarts.init(chart1.value)
      chartInstance2 = echarts.init(chart2.value)
      fetchData()

      window.addEventListener('resize', () => {
        chartInstance1?.resize()
        chartInstance2?.resize()
      })
    })

    return {
      chart1,
      chart2,
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
  margin-bottom: 20px;
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
  font-weight: 500;
}

.content-container {
  display: grid;
  gap: 20px;
  grid-template-columns: 1fr;
}

.chart-card {
  background: #fff;
  border-radius: 8px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-header .el-icon {
  color: #909399;
  cursor: help;
}

.chart {
  height: 400px;
  width: 100%;
}

@media (min-width: 1200px) {
  .content-container {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>