import schedule
import time
from dotenv import load_dotenv
from envios_email.vencimento import disparar_alertas

load_dotenv()

def job():
    print("Iniciando checagem de licenças...")
    enviados = disparar_alertas()
    print(f"{enviados} e-mails enviados.")

schedule.every().day.at("10:00").do(job)

print("Iniciando agendador")

while True:
    schedule.run_pending()
    time.sleep(1)