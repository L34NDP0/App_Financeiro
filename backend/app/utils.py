# backend/app/utils.py
from datetime import datetime

def validar_data(data_str):
    try:
        return datetime.strptime(data_str, '%Y-%m-%d').date()
    except ValueError:
        return None

def validar_valor(valor):
    try:
        valor_float = float(valor)
        if valor_float <= 0:
            raise ValueError("O valor deve ser maior que zero")
        return valor_float
    except ValueError as e:
        raise ValueError("Valor inválido")