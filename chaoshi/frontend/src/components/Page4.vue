<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" type="primary" plain class="back-button">
          <el-icon><Back /></el-icon> 返回
        </el-button>
        <h2>销售趋势分析</h2>
      </div>
    </div>

    <div class="content-container">
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <div class="header-with-select">
              <span>商品销售趋势</span>
              <el-select 
                v-model="selectedName" 
                placeholder="选择商品" 
                class="product-select"
              >
                <el-option
                  v-for="item in productNames"
                  :key="item"
                  :label="item"
                  :value="item"
                />
              </el-select>
            </div>
            <el-tooltip content="展示选定商品的销售数量和金额变化趋势">
              <el-icon><InfoFilled /></el-icon>
            </el-tooltip>
          </div>
        </template>
        <div ref="dynamicChart" class="chart"></div>
      </el-card>

      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>商品销售排行</span>
            <el-tooltip content="所有商品的累计销售金额排名">
              <el-icon><InfoFilled /></el-icon>
            </el-tooltip>
          </div>
        </template>
        <div ref="barChart" class="chart"></div>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'
import { Back, InfoFilled } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

export default {
  name: 'Page4',
  components: {
    Back,
    InfoFilled
  },
  setup() {
    const router = useRouter()
    const selectedName = ref('矿泉水')
    const productNames = ref([])
    const dynamicChart = ref(null)
    const barChart = ref(null)
    let dynamicChartInstance = null
    let barChartInstance = null

    const initDynamicChart = (purchaseData) => {
      const categories = purchaseData.map(item => item.purchase_time)
      const priceData = purchaseData.map(item => item.total_price)
      const quantityData = purchaseData.map(item => item.quantity)

      dynamicChartInstance.setOption({
        title: {
          text: '销售趋势',
          textStyle: {
            fontSize: 16,
            fontWeight: 'normal'
          },
          top: 20
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          }
        },
        legend: {
          data: ['销售金额', '销售数量'],
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
          data: categories,
          axisLabel: {
            interval: 0,
            rotate: 30
          }
        },
        yAxis: [
          {
            type: 'value',
            name: '销售金额',
            position: 'left',
            axisLabel: {
              formatter: '￥{value}'
            }
          },
          {
            type: 'value',
            name: '销售数量',
            position: 'right'
          }
        ],
        series: [
          {
            name: '销售金额',
            type: 'bar',
            data: priceData,
            itemStyle: {
              color: '#FF9800'
            }
          },
          {
            name: '销售数量',
            type: 'line',
            yAxisIndex: 1,
            data: quantityData,
            itemStyle: {
              color: '#2196F3'
            }
          }
        ]
      })
    }

    const initBarChart = (data) => {
      const sortedData = [...data].sort((a, b) => b.total_price - a.total_price)

      barChartInstance.setOption({
        title: {
          text: '销售金额排行',
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
          },
          formatter: '{b}: ￥{c}'
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          axisLabel: {
            formatter: '￥{value}'
          }
        },
        yAxis: {
          type: 'category',
          data: sortedData.map(item => item.name)
        },
        series: [
          {
            type: 'bar',
            data: sortedData.map(item => ({
              value: item.total_price,
              itemStyle: {
                color: `rgba(64, 158, 255, ${item.total_price / Math.max(...sortedData.map(d => d.total_price))})`
              }
            })),
            label: {
              show: true,
              position: 'right',
              formatter: '￥{c}'
            }
          }
        ]
      })
    }

    const fetchData = async () => {
      try {
        const [namesRes, totalPriceRes] = await Promise.all([
          axios.get('http://localhost:11000/api/product-names'),
          axios.get('http://localhost:11000/api/product-total-price')
        ])
        productNames.value = namesRes.data
        initBarChart(totalPriceRes.data)
      } catch (error) {
        console.error('获取数据失败:', error)
      }
    }

    const fetchDynamicData = async (name) => {
      try {
        const response = await axios.get('http://localhost:11000/api/product-dynamic-data', {
          params: { name }
        })
        initDynamicChart(response.data)
      } catch (error) {
        console.error('获取动态数据失败:', error)
      }
    }

    const goBack = () => {
      router.go(-1)
    }

    watch(selectedName, (newName) => {
      if (newName) {
        fetchDynamicData(newName)
      }
    })

    onMounted(() => {
      dynamicChartInstance = echarts.init(dynamicChart.value)
      barChartInstance = echarts.init(barChart.value)
      fetchData()
      fetchDynamicData(selectedName.value)

      window.addEventListener('resize', () => {
        dynamicChartInstance?.resize()
        barChartInstance?.resize()
      })
    })

    return {
      selectedName,
      productNames,
      dynamicChart,
      barChart,
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

.header-with-select {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
}

.product-select {
  width: 200px;
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