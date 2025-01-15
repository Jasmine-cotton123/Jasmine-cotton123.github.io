<template>
  <div class="page-container">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" type="primary" plain class="back-button">
          <el-icon><Back /></el-icon> 返回
        </el-button>
        <h2>商品收藏分析</h2>
      </div>
    </div>

    <div class="content-container">
      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>收藏与购物车对比</span>
            <el-tooltip content="展示每个商品的收藏数和购物车数量对比">
              <el-icon><InfoFilled /></el-icon>
            </el-tooltip>
          </div>
        </template>
        <div ref="chart1" class="chart"></div>
      </el-card>

      <el-card class="chart-card">
        <template #header>
          <div class="card-header">
            <span>转化率排行</span>
            <el-tooltip content="商品从收藏到加入购物车的转化率">
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
  name: 'Page3',
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
      const favoriteData = data.map(item => item.favorite)
      const cartData = data.map(item => item.cart)

      chartInstance1.setOption({
        title: {
          text: '商品收藏与购物车数据',
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
          data: ['收藏数', '购物车数'],
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
            name: '收藏数',
            type: 'bar',
            data: favoriteData,
            itemStyle: {
              color: '#FF9800'
            }
          },
          {
            name: '购物车数',
            type: 'bar',
            data: cartData,
            itemStyle: {
              color: '#2196F3'
            }
          }
        ]
      })
    }

    const initChart2 = (data) => {
      const labels = data.map(item => item.name)
      const ratioData = data.map(item => ({
        value: (item.cart / item.favorite * 100).toFixed(2),
        itemStyle: {
          color: `rgba(64, 158, 255, ${item.cart / item.favorite})`
        }
      }))

      // 按转化率排序
      const sortedData = labels.map((label, index) => ({
        label,
        ratio: ratioData[index]
      })).sort((a, b) => b.ratio.value - a.ratio.value)

      chartInstance2.setOption({
        title: {
          text: '收藏转化率排行',
          textStyle: {
            fontSize: 16,
            fontWeight: 'normal'
          },
          top: 20
        },
        tooltip: {
          formatter: '{b}: {c}%'
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
            formatter: '{value}%'
          }
        },
        yAxis: {
          type: 'category',
          data: sortedData.map(item => item.label)
        },
        series: [
          {
            type: 'bar',
            data: sortedData.map(item => item.ratio),
            label: {
              show: true,
              position: 'right',
              formatter: '{c}%'
            }
          }
        ]
      })
    }

    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:11000/api/products')
        initChart1(response.data)
        initChart2(response.data)
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