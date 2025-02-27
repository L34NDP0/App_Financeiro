<template>
    <div class="chart-container">
        <Chart type="line" :data="chartData" :options="chartOptions" />
    </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useStore } from 'vuex'

export default {
    name: 'FluxoCaixaChart',
    setup() {
        const store = useStore()

        // Dados do gráfico
        const chartData = ref({
            labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho'],
            datasets: [
                {
                    label: 'Fluxo de Caixa',
                    data: [0, 0, 0, 0, 0, 0], // Inicialmente vazio
                    fill: false,
                    borderColor: '#2196F3',
                    tension: 0.4
                }
            ]
        })

        // Configurações do gráfico
        const chartOptions = ref({
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        })

        // Buscar dados no Vuex quando o componente for montado
        onMounted(async () => {
            await store.dispatch('fetchResumoDashboard')  // Busca os dados do backend
            atualizarGrafico()  // Atualiza os dados do gráfico
        })

        // Função para atualizar os dados do gráfico
        const atualizarGrafico = () => {
            if (store.state.resumoDashboard) {
                chartData.value.datasets[0].data = store.state.resumoDashboard.fluxoCaixa || [0, 0, 0, 0, 0, 0]
            }
        }

        // Observar mudanças no Vuex e atualizar o gráfico dinamicamente
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
}
</style>
