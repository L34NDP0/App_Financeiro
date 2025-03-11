import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// Chart.js
import { Chart } from 'chart.js'
import { registerables } from 'chart.js'
Chart.register(...registerables)

// PrimeVue
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'
import ConfirmationService from 'primevue/confirmationservice'
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Calendar from 'primevue/calendar'
import Dropdown from 'primevue/dropdown'
import Tag from 'primevue/tag'


// Estilos do PrimeVue
import 'primevue/resources/themes/saga-blue/theme.css'
import 'primevue/resources/primevue.min.css'
import 'primeicons/primeicons.css'

const app = createApp(App)

// Use PrimeVue e seus serviços
app.use(PrimeVue)
app.use(ToastService)
app.use(ConfirmationService)
app.use(router)
app.use(store)
app.component('DataTable', DataTable)
app.component('Column', Column)
app.component('Calendar', Calendar)
app.component('Dropdown', Dropdown)
app.component('Tag', Tag)

// Registre os componentes globalmente
app.component('Toast', Toast)
app.component('ConfirmDialog', ConfirmDialog)
app.component('Button', Button)
app.component('Dialog', Dialog)

app.mount('#app')