import requests
import os
from APITempoV2 import verificar_clima


TOKEN = os.environ["TELEGRAM_TOKEN"]
URL = f"https://api.telegram.org/bot{TOKEN}"

def send_Message(text):
    params = {"chat_id" : 8998652969, "text": text}
    resposta = requests.get(f"{URL}/sendMessage",params=params)
    resposta.raise_for_status()

def mandar_mensagem():
    try:
        clima = verificar_clima("São Paulo")
    except Exception as e:
        print(f"Erro ao verificar o clima: {e}")
        return

    if clima["vai_chover"] == True and clima["vai_fazer_frio"] == False:
        send_Message("🚨 Hoje vai chover, LEVE GUARDA-CHUVA! 🌧️")
    elif clima["vai_fazer_frio"] == True and clima["vai_chover"] == False:
        send_Message("🚨 Hoje vai fazer frio, LEVE UM AGASALHO! ❄️🥶")
    elif clima["vai_chover"] == True and clima["vai_fazer_frio"] == True:
        send_Message("🚨 Hoje vai fazer frio e chover, LEVE UM AGASALHO E UM GUARDA-CHUVA 🌧️❄️")

mandar_mensagem()
