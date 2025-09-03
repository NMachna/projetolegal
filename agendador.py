import schedule
import time
from dotenv import load_dotenv
from envios_email.vencimento import disparar_alertas

load_dotenv()

def job():
    print("Iniciando checagem de licenças...")
    enviados = disparar_alertas()
    print(f"{enviados} e-mails enviados.")

# Agendar todo dia às 9h
schedule.every().day.at("10:00").do(job)

# Ou a cada X minutos para testes:
# schedule.every(10).minutes.do(job)

print("Agendador iniciado...")

while True:
    schedule.run_pending()
    time.sleep(1)