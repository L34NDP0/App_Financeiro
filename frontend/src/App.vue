<!-- frontend/src/App.vue -->
<template>
  <div id="app">
    <Toast position="top-right" />
    <ConfirmDialog />
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
          <Button type="button" @click="showAddReceita" class="p-button-success action-button" icon="pi pi-plus">
            <span class="button-text">Receita</span>
          </Button>
          <Button type="button" @click="showAddDespesa" class="p-button-danger action-button" icon="pi pi-minus">
            <span class="button-text">Despesa</span>
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
  margin-bottom: 50px;
  padding: 0 10px;
}

.action-button {
  width: 100%;
  justify-content: flex-start;
  padding: 0.75rem 1rem;
}

.action-button .button-text {
  margin-left: 0.5rem;
}

@media (max-width: 768px) {
  .app-container {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    padding: 10px;
  }

  .actions {
    flex-direction: row;
    margin-bottom: 20px;
  }

  .action-button {
    flex: 1;
    justify-content: center;
  }

  .main-content {
    padding: 10px;
  }
}

@media (max-width: 480px) {
  .actions {
    flex-direction: column;
  }

  .action-button {
    width: 100%;
  }

  .button-text {
    display: inline-block;
  }
}
</style>