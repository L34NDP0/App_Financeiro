<template>
    <div class="chart-container">
        <Bar v-if="chartReady" :data="chartData" :options="chartOptions" />
        <div v-else>Carregando...</div>
    </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useStore } from 'vuex'
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js'
import { Bar } from 'vue-chartjs'

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
)

export default {
    name: 'FluxoCaixaChart',
    components: {
        Bar
    },
    setup() {
        const store = useStore()
        const chartReady = ref(false)

        const chartData = ref({
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
            datasets: [
                {
                    label: 'Receitas',
                    data: [0, 0, 0, 0, 0, 0],
                    backgroundColor: 'rgba(76, 175, 80, 0.8)',
                    borderColor: '#4CAF50',
                    borderWidth: 1,
                    borderRadius: 5,
                    barPercentage: 0.8,
                    categoryPercentage: 0.9
                },
                {
                    label: 'Despesas',
                    data: [0, 0, 0, 0, 0, 0],
                    backgroundColor: 'rgba(244, 67, 54, 0.8)',
                    borderColor: '#F44336',
                    borderWidth: 1,
                    borderRadius: 5,
                    barPercentage: 0.8,
                    categoryPercentage: 0.9
                }
            ]
        })

        const chartOptions = ref({
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        padding: 20,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: (context) => {
                            const value = context.raw || 0;
                            return `${context.dataset.label}: R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: (value) => {
                            return `R$ ${value.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`;
                        }
                    }
                }
            }
        })

        const mesesAbreviados = {
            'January': 'Jan',
            'February': 'Fev',
            'March': 'Mar',
            'April': 'Abr',
            'May': 'Mai',
            'June': 'Jun',
            'July': 'Jul',
            'August': 'Ago',
            'September': 'Set',
            'October': 'Out',
            'November': 'Nov',
            'December': 'Dez'
        }

        const atualizarGrafico = () => {
            console.log('Atualizando gráfico...')
            console.log('Estado do dashboard:', store.state.resumoDashboard)

            const fluxoCaixa = store.state.resumoDashboard?.fluxoCaixa
            console.log('Dados do fluxo de caixa:', fluxoCaixa)

            if (fluxoCaixa) {
                const labels = fluxoCaixa.labels.map(mes =>
                    mesesAbreviados[mes] || mes.substring(0, 3)
                )
                console.log('Labels processados:', labels)
                console.log('Receitas:', fluxoCaixa.receitas)
                console.log('Despesas:', fluxoCaixa.despesas)

                chartData.value = {
                    labels,
                    datasets: [
                        {
                            ...chartData.value.datasets[0],
                            data: fluxoCaixa.receitas || []
                        },
                        {
                            ...chartData.value.datasets[1],
                            data: fluxoCaixa.despesas || []
                        }
                    ]
                }
                chartReady.value = true
            }
        }

        onMounted(async () => {
            console.log('Componente montado')
            try {
                await store.dispatch('fetchResumoDashboard')
                atualizarGrafico()
            } catch (error) {
                console.error('Erro ao carregar dados:', error)
            }
        })

        watch(() => store.state.resumoDashboard, (newVal) => {
            console.log('Dashboard atualizado:', newVal)
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
    padding: 10px;
}
</style>