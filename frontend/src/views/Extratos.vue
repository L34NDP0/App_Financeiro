<template>
    <div class="extratos-view">
        <div class="header">
            <h2>Extratos</h2>
            <div class="filters">
                <div class="filter-group">
                    <span class="p-float-label">
                        <Calendar v-model="filters.periodo" selectionMode="range" :showIcon="true"
                            dateFormat="dd/mm/yy" />
                        <label>Período</label>
                    </span>
                </div>
                <div class="filter-group">
                    <span class="p-float-label">
                        <Dropdown v-model="filters.tipo" :options="tiposTransacao" optionLabel="label"
                            optionValue="value" placeholder="Selecione" />
                        <label>Tipo</label>
                    </span>
                </div>
                <div class="filter-group">
                    <span class="p-float-label">
                        <Dropdown v-model="filters.categoria" :options="categorias" optionLabel="nome"
                            optionValue="nome" placeholder="Selecione" />
                        <label>Categoria</label>
                    </span>
                </div>
                <Button icon="pi pi-search" @click="buscarTransacoes" />
                <Button icon="pi pi-filter-slash" class="p-button-outlined" @click="limparFiltros" />
            </div>
        </div>

        <DataTable :value="transacoes" :paginator="true" :rows="10" :loading="loading"
            paginatorTemplate="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
            :rowsPerPageOptions="[10, 20, 50]" responsiveLayout="scroll"
            currentPageReportTemplate="Mostrando {first} a {last} de {totalRecords}">

            <Column field="data" header="Data" :sortable="true">
                <template #body="slotProps">
                    {{ formatarData(slotProps.data.data) }}
                </template>
            </Column>

            <Column field="descricao" header="Descrição" :sortable="true" />

            <Column field="categoria" header="Categoria" :sortable="true" />

            <Column field="valor" header="Valor" :sortable="true">
                <template #body="slotProps">
                    <span
                        :class="{ 'valor-receita': slotProps.data.tipo === 'receita', 'valor-despesa': slotProps.data.tipo === 'despesa' }">
                        {{ formatarMoeda(slotProps.data.valor) }}
                    </span>
                </template>
            </Column>

            <Column field="status" header="Status" :sortable="true">
                <template #body="slotProps">
                    <Tag :value="slotProps.data.status" :severity="getStatusSeverity(slotProps.data)" />
                </template>
            </Column>

            <Column header="Ações">
                <template #body="slotProps">
                    <Button icon="pi pi-pencil" class="p-button-text p-button-sm"
                        @click="editarTransacao(slotProps.data)" />
                    <Button icon="pi pi-trash" class="p-button-text p-button-danger p-button-sm"
                        @click="confirmarExclusao(slotProps.data)" />
                </template>
            </Column>
        </DataTable>
    </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useStore } from 'vuex'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Calendar from 'primevue/calendar'
import Dropdown from 'primevue/dropdown'
import Tag from 'primevue/tag'
import { useConfirm } from 'primevue/useconfirm'
import { useToast } from 'primevue/usetoast'

export default {
    name: 'ExtratosView',
    components: {
        DataTable,
        Column,
        Button,
        Calendar,
        Dropdown,
        Tag
    },
    setup() {
        const store = useStore()
        const confirm = useConfirm()
        const toast = useToast()
        const loading = ref(false)
        const transacoes = ref([])

        const filters = reactive({
            periodo: null,
            tipo: null,
            categoria: null
        })

        const tiposTransacao = [
            { label: 'Todos', value: null },
            { label: 'Receitas', value: 'receita' },
            { label: 'Despesas', value: 'despesa' }
        ]

        const categorias = ref([
            { nome: 'Todas' },
            { nome: 'Alimentação' },
            { nome: 'Moradia' },
            { nome: 'Transporte' },
            { nome: 'Saúde' },
            { nome: 'Educação' },
            { nome: 'Lazer' },
            { nome: 'Salário' },
            { nome: 'Investimentos' },
            { nome: 'Freelance' },
            { nome: 'Outros' }
        ])

        const formatarData = (data) => {
            return new Date(data).toLocaleDateString('pt-BR')
        }

        const formatarMoeda = (valor) => {
            return valor.toLocaleString('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            })
        }

        const getStatusSeverity = (transacao) => {
            if (transacao.tipo === 'receita') {
                return transacao.recebido ? 'success' : 'warning'
            } else {
                return transacao.pago ? 'success' : 'warning'
            }
        }

        const buscarTransacoes = async () => {
            loading.value = true
            try {
                // Implemente a lógica de busca com filtros
                const response = await store.dispatch('buscarTransacoes', filters)
                transacoes.value = response
            } catch (error) {
                toast.add({
                    severity: 'error',
                    summary: 'Erro',
                    detail: 'Erro ao buscar transações',
                    life: 3000
                })
            } finally {
                loading.value = false
            }
        }

        const limparFiltros = () => {
            filters.periodo = null
            filters.tipo = null
            filters.categoria = null
            buscarTransacoes()
        }

        const editarTransacao = (transacao) => {
            // Implementar lógica de edição
            console.log('Editar transação:', transacao)
        }

        const confirmarExclusao = (transacao) => {
            confirm.require({
                message: 'Tem certeza que deseja excluir esta transação?',
                header: 'Confirmar Exclusão',
                icon: 'pi pi-exclamation-triangle',
                accept: () => excluirTransacao(transacao),
                reject: () => { }
            })
        }

        const excluirTransacao = async (transacao) => {
            try {
                await store.dispatch('excluirTransacao', transacao)
                toast.add({
                    severity: 'success',
                    summary: 'Sucesso',
                    detail: 'Transação excluída com sucesso',
                    life: 3000
                })
                buscarTransacoes()
            } catch (error) {
                toast.add({
                    severity: 'error',
                    summary: 'Erro',
                    detail: 'Erro ao excluir transação',
                    life: 3000
                })
            }
        }

        onMounted(() => {
            buscarTransacoes()
        })

        return {
            loading,
            transacoes,
            filters,
            tiposTransacao,
            categorias,
            formatarData,
            formatarMoeda,
            getStatusSeverity,
            buscarTransacoes,
            limparFiltros,
            editarTransacao,
            confirmarExclusao
        }
    }
}
</script>

<style scoped>
.extratos-view {
    padding: 20px;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.filters {
    display: flex;
    gap: 1rem;
    align-items: flex-end;
}

.filter-group {
    min-width: 200px;
}

:deep(.p-calendar),
:deep(.p-dropdown) {
    width: 100%;
}

.valor-receita {
    color: #4CAF50;
    font-weight: 600;
}

.valor-despesa {
    color: #F44336;
    font-weight: 600;
}

@media (max-width: 768px) {
    .header {
        flex-direction: column;
        align-items: stretch;
        gap: 1rem;
    }

    .filters {
        flex-direction: column;
        gap: 1rem;
    }

    .filter-group {
        min-width: 100%;
    }
}
</style>