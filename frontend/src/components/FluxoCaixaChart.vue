<template>
    <div class="chart-container">
        <Line :data="chartData" :options="chartOptions" />
    </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useStore } from 'vuex'
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler  // Adicione o import do Filler
} from 'chart.js'
import { Line } from 'vue-chartjs'

// Registre todos os plugins necessários
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler  // Registre o plugin Filler
)

export default {
    name: 'FluxoCaixaChart',
    components: {
        Line
    },
    setup() {
        const store = useStore()

        const chartData = ref({
            labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho'],
            datasets: [
                {
                    label: 'Receitas',
                    data: [],
                    borderColor: '#4CAF50',
                    backgroundColor: 'rgba(76, 175, 80, 0.2)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Despesas',
                    data: [],
                    borderColor: '#F44336',
                    backgroundColor: 'rgba(244, 67, 54, 0.2)',
                    fill: true,
                    tension: 0.4
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
            },
            scales: {
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

        onMounted(async () => {
            await store.dispatch('fetchResumoDashboard')
            atualizarGrafico()
        })

        const atualizarGrafico = () => {
            if (store.state.resumoDashboard?.fluxoCaixa) {
                const { receitas, despesas } = store.state.resumoDashboard.fluxoCaixa
                chartData.value.datasets[0].data = receitas || []
                chartData.value.datasets[1].data = despesas || []
            }
        }

        watch(() => store.state.resumoDashboard, () => {
            atualizarGrafico()
        }, { deep: true })

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