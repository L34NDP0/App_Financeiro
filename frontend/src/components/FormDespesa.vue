<!-- frontend/src/components/FormDespesa.vue -->
<template>
    <form @submit.prevent="handleSubmit" class="form-container">
        <div class="form-group">
            <label for="descricao">Descrição</label>
            <InputText id="descricao" v-model="form.descricao" :class="{ 'p-invalid': errors.descricao }"
                placeholder="Ex: Aluguel" />
            <small class="p-error" v-if="errors.descricao">{{ errors.descricao }}</small>
        </div>

        <div class="form-group">
            <label for="valor">Valor</label>
            <InputNumber id="valor" v-model="form.valor" :class="{ 'p-invalid': errors.valor }" mode="currency"
                currency="BRL" locale="pt-BR" :minFractionDigits="2" :maxFractionDigits="2" :step="0.01" :pt="{
                    input: {
                        inputmode: 'decimal',
                        autocomplete: 'off'
                    }
                }" />
            <small class="p-error" v-if="errors.valor">{{ errors.valor }}</small>
        </div>

        <div class="form-group">
            <label for="categoria">Categoria</label>
            <Dropdown id="categoria" v-model="form.categoria" :options="categorias" optionLabel="nome"
                optionValue="nome" :class="{ 'p-invalid': errors.categoria }" placeholder="Selecione uma categoria" />
            <small class="p-error" v-if="errors.categoria">{{ errors.categoria }}</small>
        </div>

        <div class="form-group">
            <label for="data">Data</label>
            <Calendar id="data" v-model="form.data" :class="{ 'p-invalid': errors.data }" dateFormat="dd/mm/yy"
                :showIcon="true" />
            <small class="p-error" v-if="errors.data">{{ errors.data }}</small>
        </div>

        <div class="form-group switches">
            <div class="switch-item">
                <label>
                    <Checkbox v-model="form.pago" binary />
                    Pago
                </label>
            </div>
            <div class="switch-item">
                <label>
                    <Checkbox v-model="form.fixo" binary />
                    Despesa Fixa
                </label>
            </div>
        </div>

        <div class="form-actions">
            <Button type="button" label="Cancelar" class="p-button-text" @click="$emit('cancel')" />
            <Button type="submit" label="Salvar" class="p-button-danger" :loading="loading" />
        </div>
    </form>
</template>

<script>
import { ref, reactive } from 'vue'
import { useStore } from 'vuex'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Dropdown from 'primevue/dropdown'
import Calendar from 'primevue/calendar'
import Checkbox from 'primevue/checkbox'
import Button from 'primevue/button'

export default {
    name: 'FormDespesa',
    components: {
        InputText,
        InputNumber,
        Dropdown,
        Calendar,
        Checkbox,
        Button
    },
    emits: ['save', 'cancel'],
    setup(props, { emit }) {
        const store = useStore()
        const loading = ref(false)

        const form = reactive({
            descricao: '',
            valor: null,
            categoria: null,
            data: new Date(),
            pago: false,
            fixo: false
        })

        const errors = reactive({
            descricao: '',
            valor: '',
            categoria: '',
            data: ''
        })

        const categorias = ref([
            { nome: 'Alimentação' },
            { nome: 'Moradia' },
            { nome: 'Lazer' },
            { nome: 'Investimentos' },
            { nome: 'Educação' },
            { nome: 'Transporte' },
            { nome: 'Saúde' },
            { nome: 'Outros' }
        ])

        const validateForm = () => {
            let isValid = true

            // Limpa erros anteriores
            Object.keys(errors).forEach(key => errors[key] = '')

            if (!form.descricao) {
                errors.descricao = 'Descrição é obrigatória'
                isValid = false
            }

            if (!form.valor || form.valor <= 0) {
                errors.valor = 'Valor deve ser maior que zero'
                isValid = false
            }

            if (!form.categoria) {
                errors.categoria = 'Categoria é obrigatória'
                isValid = false
            }

            if (!form.data) {
                errors.data = 'Data é obrigatória'
                isValid = false
            }

            return isValid
        }

        const handleSubmit = async () => {
            if (!validateForm()) return

            loading.value = true
            try {
                const despesaData = {
                    ...form,
                    data: form.data.toISOString().split('T')[0]
                }

                await store.dispatch('adicionarDespesa', despesaData)
                // Limpa o formulário
                Object.keys(form).forEach(key => {
                    if (key === 'data') {
                        form[key] = new Date()
                    } else if (typeof form[key] === 'boolean') {
                        form[key] = false
                    } else {
                        form[key] = null
                    }
                })
                // Emite o evento de sucesso
                emit('save', true)
            } catch (error) {
                console.error('Erro ao salvar despesa:', error)
                emit('save', false)
            } finally {
                loading.value = false
            }
        }

        return {
            form,
            errors,
            loading,
            categorias,
            handleSubmit
        }
    }
}
</script>

<style scoped>
.form-container {
    padding: 1rem;
}

.form-group {
    margin-bottom: 1rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
}

/* Inputs responsivos */
.form-group :deep(.p-inputtext),
.form-group :deep(.p-dropdown),
.form-group :deep(.p-calendar),
.form-group :deep(.p-inputnumber) {
    width: 100%;
}

/* Ajustes para dropdown e calendar em mobile */
:deep(.p-dropdown-panel),
:deep(.p-datepicker) {
    position: fixed !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    width: calc(100vw - 2rem) !important;
    max-height: 80vh;
    overflow-y: auto;
}

/* Checkboxes responsivos */
.switches {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

/* Botões responsivos */
.form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 1rem;
}

/* Media query para mobile */
@media (max-width: 480px) {
    .form-actions {
        flex-direction: column;
    }

    .form-actions button {
        width: 100%;
    }

    .switches {
        flex-direction: column;
    }
}
</style>