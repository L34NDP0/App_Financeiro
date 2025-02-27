// frontend/src/components/PieChart.vue
<template>
    <div class="chart-container">
        <Chart type="pie" :data="chartData" :options="chartOptions" />
    </div>
</template>

<script>
export default {
    name: 'PieChart',
    props: {
        data: {
            type: Array,
            required: true
        }
    },
    setup(props) {
        const chartData = {
            labels: props.data.map(item => item.categoria),
            datasets: [
                {
                    data: props.data.map(item => item.valor),
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0',
                        '#9966FF',
                        '#FF9F40'
                    ]
                }
            ]
        }

        const chartOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }

        return {
            chartData,
            chartOptions
        }
    }
}
</script>

<style scoped>
.chart-container {
    height: 300px;
    width: 100%;
}
</style>