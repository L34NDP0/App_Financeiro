/* eslint-disable */
import { createStore } from 'vuex';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

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
            state.receitas = receitas;
        },
        SET_DESPESAS(state, despesas) {
            state.despesas = despesas;
        },
        SET_CATEGORIAS_RECEITAS(state, categorias) {
            state.categoriasReceitas = categorias;
        },
        SET_CATEGORIAS_DESPESAS(state, categorias) {
            state.categoriasDespesas = categorias;
        },
        SET_RESUMO_DASHBOARD(state, resumo) {
            state.resumoDashboard = resumo;
        }
    },

    actions: {
        async fetchData({ commit }, { mutation, endpoint }) {
            try {
                const response = await axios.get(`${API_URL}${endpoint}`);
                commit(mutation, response.data);
            } catch (error) {
                console.error(`Erro ao buscar ${endpoint}:`, error.response?.data || error.message);
            }
        },

        fetchReceitas({ dispatch }) {
            return dispatch('fetchData', { mutation: 'SET_RECEITAS', endpoint: '/receitas' });
        },

        fetchDespesas({ dispatch }) {
            return dispatch('fetchData', { mutation: 'SET_DESPESAS', endpoint: '/despesas' });
        },

        fetchResumoDashboard({ dispatch }) {
            return dispatch('fetchData', { mutation: 'SET_RESUMO_DASHBOARD', endpoint: '/dashboard/resumo' });
        },

        async adicionarItem({ dispatch }, { endpoint, data, fetchActions }) {
            try {
                await axios.post(`${API_URL}${endpoint}`, data);
                fetchActions.forEach(action => dispatch(action));
            } catch (error) {
                console.error(`Erro ao adicionar em ${endpoint}:`, error.response?.data || error.message);
                throw error;
            }
        },

        adicionarReceita({ dispatch }, receita) {
            return dispatch('adicionarItem', { endpoint: '/receitas', data: receita, fetchActions: ['fetchReceitas', 'fetchResumoDashboard'] });
        },

        adicionarDespesa({ dispatch }, despesa) {
            return dispatch('adicionarItem', { endpoint: '/despesas', data: despesa, fetchActions: ['fetchDespesas', 'fetchResumoDashboard'] });
        }
    }
});
