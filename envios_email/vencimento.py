from datetime import date, timedelta
from collections import defaultdict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import certifi
from dotenv import load_dotenv
import os

from banco.banco import Session, RelacaoEmpresaLicenca, TabelaEmpresa, TabelaEnvioEmail

load_dotenv()

# Mapeamento de Periodicidade
MAPEAMENTO_PERIODICIDADE = {
    "mensal": 30,
    "bimestral": 60,
    "trimestral": 90,
    "semestral": 180,
    "anual": 365
}
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# Estrutura de Dicionario
def nova_empresa_dict():
    return {"empresa": None, "email": None, "licencas": []}

def filtrar_licencas_ja_enviadas(empresa_obj, licencas_proximas):
    # Retorna as licenças que ainda não foram enviadas.
    with Session() as session:
        # Consulta todos os envios anteriores para essa empresa
        envios_anteriores = session.query(TabelaEnvioEmail)\
            .filter_by(empresa_id=empresa_obj.id)\
            .all()

        # Cria uma lista com nomes de licenças já enviadas
        licencas_enviadas = []
        for envio in envios_anteriores:
            for lic in envio.licencas_enviadas.split(","):
                nome_licenca = lic.split(" (venc:")[0].strip()
                licencas_enviadas.append(nome_licenca)

        # Filtra as licenças que ainda não foram enviadas
        licencas_para_enviar = [lic for lic in licencas_proximas if lic["nome"] not in licencas_enviadas]

    return licencas_para_enviar

# Busca de licenças a expirar
def obter_licencas_proximas_vencimento():
    data_hoje = date.today()
    resultado = []

    with Session() as session:
        relacoes = session.query(RelacaoEmpresaLicenca).all()
        empresas_dict = defaultdict(nova_empresa_dict)

        for relacao in relacoes:
            empresa = relacao.empresa
            licenca = relacao.licenca

            # Garante que não existe relação orfã
            if not empresa or not licenca:
                print(f"[AVISO] Relação órfã encontrada (id={relacao.id}). Ignorando.")
                continue

            # Garantir que periodicidade existe
            if not relacao.periodicidade:
                continue

            dias_periodicidade = MAPEAMENTO_PERIODICIDADE.get(relacao.periodicidade.lower())
            if dias_periodicidade is None or relacao.data_base is None:
                continue

            data_vencimento = relacao.data_base + timedelta(days=dias_periodicidade)
            dias_restantes = (data_vencimento - data_hoje).days

            # Status
            if dias_restantes < 0:
                status = "VENCIDA"
            elif dias_restantes <= relacao.antecipacao:
                status = "A VENCER"
            else:
                continue

            empresas_dict[empresa.id]["empresa"] = empresa.nome_empresa
            empresas_dict[empresa.id]["email"] = empresa.email
            empresas_dict[empresa.id]["licencas"].append({
                "nome": licenca.nome_licenca,
                "vencimento": data_vencimento.strftime("%d/%m/%Y"),
                "status": status
            })

        # Somente empresas que realmente têm licenças
        for dados_empresa in empresas_dict.values():
            if dados_empresa["licencas"]:
                resultado.append(dados_empresa)

    return resultado

def send_locaweb_email(sender_email, sender_password, recipient_email, subject, body_html):
    

    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject

        # Versão texto simples (evita spam)
        body_text = "Segue a lista de licenças próximas do vencimento. Veja detalhes no formato HTML."
        msg.attach(MIMEText(body_text, "plain"))
        msg.attach(MIMEText(body_html, "html"))

        context = ssl.create_default_context(cafile=certifi.where())

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)

    except Exception as e:
        print(f"Erro ao enviar e-mail para {recipient_email}: {e}")

# Prototipo do Corpo em HTML -> Ver com o Guido um modelo melhor e mais complexo
def montar_corpo_email(empresa):
    vencidas = [lic for lic in empresa["licencas"] if lic["status"] == "VENCIDA"]
    a_vencer = [lic for lic in empresa["licencas"] if lic["status"] == "A VENCER"]

    corpo = f"""
    <html>
        <body>
            <h2>Relatório de Licenças</h2>
            <p>Prezado(a) <strong>{empresa['empresa']}</strong>,</p>
    """

    # Seção de vencidas
    if vencidas:
        corpo += "<h3 style='color:red;'>Licenças Vencidas:</h3><ul>"
        for lic in vencidas:
            corpo += f"<li><b>{lic['nome']}</b> - Vencimento em: {lic['vencimento']}</li>"
        corpo += "</ul>"

    # Seção de a vencer
    if a_vencer:
        corpo += "<h3 style='color:orange;'>Licenças Próximas do Vencimento:</h3><ul>"
        for lic in a_vencer:
            corpo += f"<li><b>{lic['nome']}</b> - Vencimento em: {lic['vencimento']}</li>"
        corpo += "</ul>"

    corpo += """
            <p>Atenciosamente,<br>Equipe de Controle</p>
        </body>
    </html>
    """
    return corpo

# Função para ser utilizada na Tela_Alerta
def disparar_alertas():
    empresas_vencendo = obter_licencas_proximas_vencimento()
    enviados = 0
    
    with Session() as session:
        for dados_empresa in empresas_vencendo:
            empresa_obj = session.query(TabelaEmpresa).filter_by(nome_empresa=dados_empresa["empresa"]).first()
            
            if not empresa_obj:
                print(f"[AVISO] Empresa não encontrada no banco: {dados_empresa['empresa']}")
                continue

            # Filtra apenas licenças que ainda não foram enviadas
            licencas_para_enviar = filtrar_licencas_ja_enviadas(empresa_obj, dados_empresa["licencas"])
            if not licencas_para_enviar:
                print(f"Todas as licenças já enviadas para {empresa_obj.nome_empresa}. Pulando...")
                continue

            # Monta corpo do e-mail apenas com as licenças restantes
            html_email = montar_corpo_email({
                "empresa": empresa_obj.nome_empresa,
                "email": empresa_obj.email,
                "licencas": licencas_para_enviar
            })
            try:
                send_locaweb_email(
                    SENDER_EMAIL,
                    SENDER_PASSWORD,
                    dados_empresa["email"],
                    f"Licenças próximas do vencimento/vencidas - {dados_empresa['empresa']}",
                    html_email
                )

                # Guardar no banco o histórico do envio
                licencas_str = ", ".join(
                    f"{lic['nome']} (venc: {lic['vencimento']})"
                    for lic in licencas_para_enviar
                )

                registro = TabelaEnvioEmail(
                    empresa_id=empresa_obj.id if empresa_obj else None,
                    email_destino=dados_empresa["email"],
                    licencas_enviadas=licencas_str
                )
                session.add(registro)
                session.commit()

                enviados += 1
                print(f"E-mail enviado para {dados_empresa['empresa']} ({dados_empresa['email']})")

            except Exception as e:
                print(f"Erro ao enviar e-mail para {dados_empresa['email']}: {e}")

    return enviados