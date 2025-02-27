// frontend/src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import PrimeVue from 'primevue/config'

// Importe os estilos do node_modules
import 'primevue/resources/themes/saga-blue/theme.css'     // theme
import 'primevue/resources/primevue.min.css'             // core css
import 'primeicons/primeicons.css'                      // icons
import '@mdi/font/css/materialdesignicons.css'         // material design icons

const app = createApp(App)
app.use(PrimeVue)
app.use(router)
app.use(store)
app.mount('#app')