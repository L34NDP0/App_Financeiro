from app import db
from datetime import datetime

class Receita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200))
    data = db.Column(db.Date, nullable=False)
    categoria = db.Column(db.String(50))
    recebido = db.Column(db.Boolean, default=False)
    fixo = db.Column(db.Boolean, default=False)

class Despesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200))
    data = db.Column(db.Date, nullable=False)
    categoria = db.Column(db.String(50))
    pago = db.Column(db.Boolean, default=False)
    fixo = db.Column(db.Boolean, default=False)

class CategoriaReceita(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)

class CategoriaDespesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)