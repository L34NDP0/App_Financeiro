import { createStore } from 'vuex'
import axios from 'axios'


const API_URL = process.env.VUE_APP_API_URL || 'https://app-financeiro-2q7m.onrender.com'
export default createStore({
    state: {
        resumoDashboard: null,
        transacoes: []
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
                const response = await axios.get(`${API_URL}/dashboard/resumo`)
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

                const response = await axios.get(`${API_URL}/transacoes`, { params })
                commit('SET_TRANSACOES', response.data)
                return response.data
            } catch (error) {
                console.error('Erro ao buscar transações:', error)
                throw error
            }
        },

        async excluirTransacao({ dispatch }, transacao) {
            try {
                await axios.delete(`${API_URL}/transacoes/${transacao.tipo}/${transacao.id}`)
                await dispatch('buscarTransacoes', {})
                await dispatch('fetchResumoDashboard')
            } catch (error) {
                console.error('Erro ao excluir transação:', error)
                throw error
            }
        },

        async adicionarReceita({ dispatch }, receita) {
            try {
                await axios.post(`${API_URL}/receitas`, receita)
                await dispatch('fetchResumoDashboard')
            } catch (error) {
                console.error('Erro ao adicionar receita:', error)
                throw error
            }
        },

        async adicionarDespesa({ dispatch }, despesa) {
            try {
                await axios.post(`${API_URL}/despesas`, despesa)
                await dispatch('fetchResumoDashboard')
            } catch (error) {
                console.error('Erro ao adicionar despesa:', error)
                throw error
            }
        }
    }
})