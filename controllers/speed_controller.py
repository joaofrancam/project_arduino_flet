
from models import speed_model

def registrar_velocidade(speed, user_id):
    speed_model.insert_speed(speed, user_id)

def obter_velocidades(login):
    return speed_model.get_user_speeds(login)
