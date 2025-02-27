<!-- frontend/src/views/Dashboard.vue -->
<template>
    <div class="dashboard">
        <div class="cards">
            <div class="card saldo">
                <h3>Saldo</h3>
                <h2>{{ formatCurrency(resumo?.saldo || 0) }}</h2>
            </div>
            <div class="card receitas">
                <h3>Receitas</h3>
                <h2>{{ formatCurrency(resumo?.total_receitas || 0) }}</h2>
            </div>
            <div class="card despesas">
                <h3>Despesas</h3>
                <h2>{{ formatCurrency(resumo?.total_despesas || 0) }}</h2>
            </div>
        </div>

        <div class="charts">
            <div class="chart-container">
                <h3>Fluxo de Caixa</h3>
                <FluxoCaixaChart />
            </div>
            <div class="chart-container">
                <h3>Distribuição de Despesas</h3>
                <PieChart :data="despesasPorCategoria" />
            </div>
        </div>
    </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import FluxoCaixaChart from '../components/FluxoCaixaChart.vue'
import PieChart from '../components/PieChart.vue'

export default {
    name: 'DashboardView',
    components: {
        FluxoCaixaChart,
        PieChart
    },
    setup() {
        const store = useStore()
        const resumo = computed(() => store.state.resumoDashboard)

        const formatCurrency = (value) => {
            return new Intl.NumberFormat('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            }).format(value)
        }

        const despesasPorCategoria = computed(() => {
            if (!resumo.value?.despesas_categoria) return []
            return Object.entries(resumo.value.despesas_categoria).map(([categoria, valor]) => ({
                categoria,
                valor
            }))
        })

        onMounted(() => {
            store.dispatch('fetchResumoDashboard')
        })

        return {
            resumo,
            formatCurrency,
            despesasPorCategoria
        }
    }
}
</script>

<style scoped>
.dashboard {
    padding: 20px;
}

.cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 30px;
}

.card {
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card.saldo {
    background-color: #4CAF50;
    color: white;
}

.card.receitas {
    background-color: #2196F3;
    color: white;
}

.card.despesas {
    background-color: #F44336;
    color: white;
}

.charts {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 20px;
}

.chart-container {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>