<template>
    <div class="chart-container">
        <Pie v-if="chartReady" :data="chartData" :options="chartOptions" />
        <div v-else>Carregando...</div>
    </div>
</template>

<script>
import { ref, watch, onMounted } from 'vue'
import { useStore } from 'vuex'
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
        const store = useStore()
        const chartReady = ref(false)

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

        const atualizarGrafico = () => {
            if (props.data && props.data.length > 0) {
                chartData.value.labels = props.data.map(item => item.categoria)
                chartData.value.datasets[0].data = props.data.map(item => item.valor)
                chartReady.value = true
            }
        }

        onMounted(async () => {
            console.log('Componente PieChart montado')
            try {
                await store.dispatch('fetchResumoDashboard')
                atualizarGrafico()
            } catch (error) {
                console.error('Erro ao carregar dados:', error)
            }
        })

        // Watch para props.data
        watch(() => props.data, (newData) => {
            if (newData && newData.length > 0) {
                atualizarGrafico()
            }
        }, { immediate: true })

        // Watch para store
        watch(() => store.state.resumoDashboard, () => {
            atualizarGrafico()
        }, { deep: true })

        return {
            chartData,
            chartOptions,
            chartReady
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