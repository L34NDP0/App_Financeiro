// frontend/src/store/index.js
import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
    state: {
        receitas: [],
        despesas: [],
        categoriasReceitas: [],
        categoriasDespesas: [],
        resumoDashboard: null
    },

    mutations: {
        SET_RECEITAS(state, receitas) {
            state.receitas = receitas
        },
        SET_DESPESAS(state, despesas) {
            state.despesas = despesas
        },
        SET_CATEGORIAS_RECEITAS(state, categorias) {
            state.categoriasReceitas = categorias
        },
        SET_CATEGORIAS_DESPESAS(state, categorias) {
            state.categoriasDespesas = categorias
        },
        SET_RESUMO_DASHBOARD(state, resumo) {
            state.resumoDashboard = resumo
        }
    },

    actions: {
        async fetchReceitas({ commit }) {
            try {
                const response = await axios.get(`${API_URL}/receitas`)
                commit('SET_RECEITAS', response.data)
            } catch (error) {
                console.error('Erro ao buscar receitas:', error)
            }
        },

        async fetchDespesas({ commit }) {
            try {
                const response = await axios.get(`${API_URL}/despesas`)
                commit('SET_DESPESAS', response.data)
            } catch (error) {
                console.error('Erro ao buscar despesas:', error)
            }
        },

        async fetchResumoDashboard({ commit }) {
            try {
                const response = await axios.get(`${API_URL}/dashboard/resumo`)
                commit('SET_RESUMO_DASHBOARD', response.data)
            } catch (error) {
                console.error('Erro ao buscar resumo:', error)
            }
        },

        async adicionarReceita({ dispatch }, receita) {
            try {
                await axios.post(`${API_URL}/receitas`, receita)
                dispatch('fetchReceitas')
                dispatch('fetchResumoDashboard')
            } catch (error) {
                console.error('Erro ao adicionar receita:', error)
                throw error
            }
        },

        async adicionarDespesa({ dispatch }, despesa) {
            try {
                await axios.post(`${API_URL}/despesas`, despesa)
                dispatch('fetchDespesas')
                dispatch('fetchResumoDashboard')
            } catch (error) {
                console.error('Erro ao adicionar despesa:', error)
                throw error
            }
        }
    }
})