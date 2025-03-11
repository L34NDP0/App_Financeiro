<template>
    <div class="chart-container">
        <Pie :data="chartData" :options="chartOptions" />
    </div>
</template>

<script>
import { ref, watch } from 'vue'
import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
    Colors
} from 'chart.js'
import { Pie } from 'vue-chartjs'

// Registre todos os plugins necessários
ChartJS.register(
    ArcElement,
    Tooltip,
    Legend,
    Colors
)

export default {
    name: 'PieChart',
    components: {
        Pie
    },
    props: {
        data: {
            type: Array,
            required: true
        }
    },
    setup(props) {
        const chartData = ref({
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF',
                    '#FF9F40',
                    '#808080'
                ],
                hoverBackgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF',
                    '#FF9F40',
                    '#808080'
                ]
            }]
        })

        const chartOptions = ref({
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        usePointStyle: true
                    }
                },
                tooltip: {
                    callbacks: {
                        label: (context) => {
                            const value = context.raw;
                            return `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`;
                        }
                    }
                }
            }
        })

        watch(() => props.data, (newData) => {
            if (newData && newData.length > 0) {
                chartData.value.labels = newData.map(item => item.categoria)
                chartData.value.datasets[0].data = newData.map(item => item.valor)
            }
        }, { immediate: true })

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
    position: relative;
}
</style>
