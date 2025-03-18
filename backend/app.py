from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, Receita, Despesa, CategoriaReceita, CategoriaDespesa
import os
from routes import resgistrar_rotas
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)

# Configuração do banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'financas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)


# Inicialização do banco de dados
db.init_app(app)

# rotas
load_dotenv()
base_url = os.getenv("BASE_URL")
resgistrar_rotas(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 10000))    
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )