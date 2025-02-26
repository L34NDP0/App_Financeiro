# backend/config.py
import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///financas.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'sua-chave-secreta-aqui'
    JWT_SECRET_KEY = 'sua-chave-jwt-aqui'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)