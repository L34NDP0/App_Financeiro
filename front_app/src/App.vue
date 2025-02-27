<!-- frontend/src/App.vue -->
<template>
  <div class="app-container">
    <nav class="sidebar">
      <div class="logo">
        <h1>MyFinance</h1>
      </div>
      <div class="menu">
        <router-link to="/" class="menu-item">
          <i class="pi pi-home"></i>
          <span>Dashboard</span>
        </router-link>
        <router-link to="/extratos" class="menu-item">
          <i class="pi pi-list"></i>
          <span>Extratos</span>
        </router-link>
      </div>
      <div class="actions">
        <Button @click="showAddReceita" class="p-button-success" icon="pi pi-plus">
          Receita
        </Button>
        <Button @click="showAddDespesa" class="p-button-danger" icon="pi pi-minus">
          Despesa
        </Button>
      </div>
    </nav>

    <main class="main-content">
      <router-view></router-view>
    </main>

    <!-- Modais -->
    <Dialog v-model:visible="receitaModal" header="Nova Receita">
      <FormReceita @save="salvarReceita" @cancel="receitaModal = false" />
    </Dialog>

    <Dialog v-model:visible="despesaModal" header="Nova Despesa">
      <FormDespesa @save="salvarDespesa" @cancel="despesaModal = false" />
    </Dialog>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import FormReceita from './components/FormReceita.vue'
import FormDespesa from './components/FormDespesa.vue'

export default {
  name: 'App',
  components: {
    Button,
    Dialog,
    FormReceita,
    FormDespesa
  },
  setup() {
    const store = useStore()
    const receitaModal = ref(false)
    const despesaModal = ref(false)

    const showAddReceita = () => {
      receitaModal.value = true
    }

    const showAddDespesa = () => {
      despesaModal.value = true
    }

    const salvarReceita = async (receita) => {
      try {
        await store.dispatch('adicionarReceita', receita)
        receitaModal.value = false
      } catch (error) {
        // Tratar erro
      }
    }

    const salvarDespesa = async (despesa) => {
      try {
        await store.dispatch('adicionarDespesa', despesa)
        despesaModal.value = false
      } catch (error) {
        // Tratar erro
      }
    }

    return {
      receitaModal,
      despesaModal,
      showAddReceita,
      showAddDespesa,
      salvarReceita,
      salvarDespesa
    }
  }
}
</script>

<style>
.app-container {
  display: flex;
  height: 100vh;
}

.sidebar {
  width: 250px;
  background-color: #f8f9fa;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.logo {
  margin-bottom: 30px;
}

.menu {
  flex-grow: 1;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 10px;
  text-decoration: none;
  color: #495057;
  margin-bottom: 5px;
}

.menu-item i {
  margin-right: 10px;
}

.menu-item.router-link-active {
  background-color: #e9ecef;
  border-radius: 4px;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.main-content {
  flex-grow: 1;
  padding: 20px;
  background-color: #fff;
}
</style>