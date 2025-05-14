
from models import user_model

def cadastrar_usuario(login, senha):
    return user_model.insert_user(login, senha)

def autenticar_usuario(login, senha):
    return user_model.authenticate_user(login, senha)

def buscar_id_usuario(login):
    return user_model.get_user_id(login)
