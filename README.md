# Sistema de Controle Financeiro

Um sistema web completo para gerenciamento de finanças pessoais, desenvolvido com Vue.js no frontend e Python Flask no backend.

## 🚀 Funcionalidades

- ✅ Cadastro de receitas e despesas
- 📊 Dashboard com resumo financeiro
- 📈 Gráficos de acompanhamento
- 📅 Controle por período
- 🏷️ Categorização de transações
- 💰 Acompanhamento de receitas fixas e variáveis
- 📱 Interface responsiva

## 🛠️ Tecnologias Utilizadas

### Backend
- Python 3.x
- Flask
- SQLAlchemy
- SQLite
- Flask-CORS

### Frontend
- Vue.js 3
- Vuex
- Vue Router
- PrimeVue
- Chart.js
- Axios

## 📋 Pré-requisitos

- Python 3.x
- Node.js
- npm ou yarn

## ⚙️ Configuração do Ambiente

### Backend

1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd <nome-do-repositorio>
```

2. Crie e ative o ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências
```bash
cd backend
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Inicie o servidor
```bash
python app.py
```

### Frontend

1. Instale as dependências
```bash
cd frontend
npm install
```

2. Inicie o servidor de desenvolvimento
```bash
npm run serve
```

3. Para build de produção
```bash
npm run build
```

## 🗄️ Estrutura do Banco de Dados

### Tabelas Principais

- **Receitas**
  - id (PK)
  - valor
  - descrição
  - data
  - categoria
  - recebido (boolean)
  - fixo (boolean)

- **Despesas**
  - id (PK)
  - valor
  - descrição
  - data
  - categoria
  - pago (boolean)
  - fixo (boolean)

- **Categorias**
  - id (PK)
  - nome
  - tipo (receita/despesa)

## 📱 Endpoints da API

### Receitas
- `GET /receitas` - Lista todas as receitas
- `POST /receitas` - Cria nova receita
- `PUT /receitas/<id>` - Atualiza uma receita
- `DELETE /receitas/<id>` - Remove uma receita

### Despesas
- `GET /despesas` - Lista todas as despesas
- `POST /despesas` - Cria nova despesa
- `PUT /despesas/<id>` - Atualiza uma despesa
- `DELETE /despesas/<id>` - Remove uma despesa

### Dashboard
- `GET /dashboard/resumo` - Obtém resumo financeiro
- `GET /relatorios/mensal/<ano>/<mes>` - Relatório mensal

## 🔧 Configuração de Desenvolvimento

### Variáveis de Ambiente

```env
BASE_URL=http://localhost:10000
```

### Portas padrão
- Backend: 10000
- Frontend: 8080

## 📦 Deploy

### Backend
1. Configure as variáveis de ambiente de produção
2. Instale as dependências de produção
3. Execute com um servidor WSGI (ex: Gunicorn)

### Frontend
1. Gere o build de produção
```bash
npm run build
```
2. Deploy os arquivos estáticos gerados na pasta `dist`

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## ✒️ Autores

* **Leandro Barros** - *Aplicativo financeiro* - [Leandro](https://github.com/L34NDP0)

## 📄 Versão

1.0.0
