// frontend/src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import PrimeVue from 'primevue/config'






const app = createApp(App)

// Use o PrimeVue
app.use(PrimeVue)



app.use(router)
app.use(store)

app.mount('#app')