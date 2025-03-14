<!-- frontend/src/App.vue -->
<template>
  <div id="app">
    <Toast position="top-right" />
    <ConfirmDialog />
    <div class="app-container">
      <nav class="sidebar">
        <div class="logo">
          <img src="@/assets/logo.png" width="100" height="90" />
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
      <Dialog v-model:visible="receitaModal" header="Nova Receita" :modal="true" :closable="true" :closeOnEscape="true"
        :dismissableMask="true">
        <FormReceita @save="handleSaveReceita" @cancel="closeReceitaModal" />
      </Dialog>

      <Dialog v-model:visible="despesaModal" header="Nova Despesa" :modal="true" :closable="true" :closeOnEscape="true"
        :dismissableMask="true">
        <FormDespesa @save="handleSaveDespesa" @cancel="closeDespesaModal" />
      </Dialog>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useToast } from 'primevue/usetoast'
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
    const toast = useToast()
    const receitaModal = ref(false)
    const despesaModal = ref(false)

    const showAddReceita = () => {
      receitaModal.value = true
    }

    const showAddDespesa = () => {
      despesaModal.value = true
    }

    const closeReceitaModal = () => {
      receitaModal.value = false
    }

    const closeDespesaModal = () => {
      despesaModal.value = false
    }

    const handleSaveReceita = async (success) => {
      if (success) {
        closeReceitaModal()
        toast.add({
          severity: 'success',
          summary: 'Sucesso',
          detail: 'Receita adicionada com sucesso!',
          life: 3000
        })
      } else {
        toast.add({
          severity: 'error',
          summary: 'Erro',
          detail: 'Erro ao adicionar receita',
          life: 3000
        })
      }
    }

    const handleSaveDespesa = async (success) => {
      if (success) {
        closeDespesaModal()
        toast.add({
          severity: 'success',
          summary: 'Sucesso',
          detail: 'Despesa adicionada com sucesso!',
          life: 3000
        })
      } else {
        toast.add({
          severity: 'error',
          summary: 'Erro',
          detail: 'Erro ao adicionar despesa',
          life: 3000
        })
      }
    }

    return {
      receitaModal,
      despesaModal,
      showAddReceita,
      showAddDespesa,
      closeReceitaModal,
      closeDespesaModal,
      handleSaveReceita,
      handleSaveDespesa
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

/* Estilos para o modal */
:deep(.p-dialog) {
  max-width: 90vw;
  width: 500px;
}

:deep(.p-dialog-header) {
  padding: 1.5rem;
}

:deep(.p-dialog-content) {
  padding: 0;
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

  :deep(.p-dialog) {
    width: 95vw;
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