from datetime import date, timedelta
from collections import defaultdict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import certifi

from banco.banco import Session, RelacaoEmpresaLicenca, TabelaEmpresa, TabelaEnvioEmail

# Mapeamento de Periodicidade
MAPEAMENTO_PERIODICIDADE = {
    "mensal": 30,
    "bimestral": 60,
    "trimestral": 90,
    "semestral": 180,
    "anual": 365
}

# Estrutura de Dicionario
def nova_empresa_dict():
    return {"empresa": None, "email": None, "licencas": []}

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

            # Verifica se está dentro do período de antecipação
            if 0 <= (data_vencimento - data_hoje).days <= relacao.antecipacao:
                empresas_dict[empresa.id]["empresa"] = empresa.nome_empresa
                empresas_dict[empresa.id]["email"] = empresa.email
                empresas_dict[empresa.id]["licencas"].append({
                    "nome": licenca.nome_licenca,
                    "vencimento": data_vencimento.strftime("%d/%m/%Y")
                })

        # Somente empresas que realmente têm licenças
        for dados_empresa in empresas_dict.values():
            if dados_empresa["licencas"]:
                resultado.append(dados_empresa)

    return resultado

# Parte de e-mail -> Alterar para um arquivo separado depois
SMTP_SERVER = "email-ssl.com.br"
SMTP_PORT = 465
SENDER_EMAIL = "contato@eocp.com.br"
SENDER_PASSWORD = "Wocp016@nw#y05"

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
    corpo = f"""
    <html>
        <body>
            <h2>Relatório de Licenças Próximas do Vencimento</h2>
            <p>Prezado(a) <strong>{empresa['empresa']}</strong>,</p>
            <p>Segue a lista de licenças próximas do vencimento:</p>
            <ul>
    """
    for lic in empresa["licencas"]:
        corpo += f"<li>{lic['nome']} - Vencimento: {lic['vencimento']}</li>"
    
    corpo += """
            </ul>
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
            html_email = montar_corpo_email(dados_empresa)

            try:
                send_locaweb_email(
                    SENDER_EMAIL,
                    SENDER_PASSWORD,
                    dados_empresa["email"],
                    f"Licenças próximas do vencimento - {dados_empresa['empresa']}",
                    html_email
                )

                # Guardar no banco o histórico do envio
                licencas_str = ", ".join(
                    f"{lic['nome']} (venc: {lic['vencimento']})"
                    for lic in dados_empresa["licencas"]
                )

                empresa_obj = session.query(TabelaEmpresa).filter_by(email=dados_empresa["email"]).first()

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