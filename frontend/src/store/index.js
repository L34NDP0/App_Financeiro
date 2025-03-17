import { createStore } from 'vuex'
import axios from 'axios'

// Configuração da porta e base URL
const port = process.env.PORT || 8080
const API_URL = process.env.VUE_APP_API_URL || `https://app-financeiro-2q7m.onrender.com:${port}`

// Configuração global do Axios
axios.defaults.baseURL = API_URL
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*'
axios.defaults.headers.common['Content-Type'] = 'application/json'
export default createStore({
    state: {
        resumoDashboard: null,
        transacoes: [],
        baseUrl: API_URL // Adicionando baseUrl ao state para referência
    },
    mutations: {
        SET_RESUMO_DASHBOARD(state, resumo) {
            state.resumoDashboard = resumo
        },
        SET_TRANSACOES(state, transacoes) {
            state.transacoes = transacoes
        }
    },
    actions: {
        async fetchResumoDashboard({ commit }) {
            try {
                const response = await axios.get('/api/dashboard/resumo') // Removida a concatenação com API_URL
                commit('SET_RESUMO_DASHBOARD', response.data)
            } catch (error) {
                console.error('Erro ao buscar resumo:', error)
                throw error
            }
        },

        async buscarTransacoes({ commit }, filtros) {
            try {
                let params = {}

                if (filtros.tipo) {
                    params.tipo = filtros.tipo
                }

                if (filtros.categoria && filtros.categoria !== 'Todas') {
                    params.categoria = filtros.categoria
                }

                if (filtros.periodo && filtros.periodo[0] && filtros.periodo[1]) {
                    params.data_inicio = filtros.periodo[0].toISOString().split('T')[0]
                    params.data_fim = filtros.periodo[1].toISOString().split('T')[0]
                }

                const response = await axios.get('/api/transacoes', { params }) // Removida a concatenação com API_URL
                commit('SET_TRANSACOES', response.data)
                return response.data
            } catch (error) {
                console.error('Erro ao buscar transações:', error)
                throw error
            }
        },

        async excluirTransacao({ dispatch }, transacao) {
            try {
                await axios.delete(`/api/transacoes/${transacao.tipo}/${transacao.id}`) // Removida a concatenação com API_URL
                await dispatch('buscarTransacoes', {})
                await dispatch('fetchResumoDashboard')
            } catch (error) {
                console.error('Erro ao excluir transação:', error)
                throw error
            }
        },

        async adicionarReceita({ dispatch }, receita) {
            try {
                await axios.post('/api/receitas', receita) // Removida a concatenação com API_URL
                await dispatch('fetchResumoDashboard')
            } catch (error) {
                console.error('Erro ao adicionar receita:', error)
                throw error
            }
        },

        async adicionarDespesa({ dispatch }, despesa) {
            try {
                await axios.post('/api/despesas', despesa) // Removida a concatenação com API_URL
                await dispatch('fetchResumoDashboard')
            } catch (error) {
                console.error('Erro ao adicionar despesa:', error)
                throw error
            }
        }
    }
})