import sqlite3
from datetime import datetime, timedelta
from banco.banco import criar_conexao



def calcular_data_vencimento_avisos(periodicidade, data_base, antecipacao):
    # Define o intervalo da periodicidade
    periodicidade = periodicidade.lower()
    dias_periodicidade = {
        "anual": 365,
        "semestral": 182,
        "mensal": 30
    }.get(periodicidade, 0)

    # Converte a data base para datetime
    data_base = datetime.strptime(data_base, "%Y-%m-%d")
    data_vencimento = data_base + timedelta(days=dias_periodicidade)
    data_envio = data_vencimento - timedelta(days=antecipacao)

    return data_vencimento.strftime("%Y-%m-%d"), data_envio.strftime("%Y-%m-%d")

def obter_empresas():
    try:
        with criar_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, codigo, cnpj, nome_empresa, municipio, tag, email FROM tabela_empresas")
            dados = cursor.fetchall()
            return dados
        
    except sqlite3.OperationalError as e:
        print(f"Algo deu errado, erro: {e}")
        conexao.rollback()

def consultar_empresa():
    try:
        with criar_conexao() as conexao:
            
            cursor = conexao.cursor()

            cnpj = input("Digite o CNPJ da empresa para consulta: ").strip()

            cursor.execute("""
                SELECT 
                    e.codigo,
                    e.cnpj,
                    e.nome_empresa,
                    l.nome_licenca,
                    l.periodicidade,
                    rel.data_base,
                    rel.antecipacao,
                    e.email
                FROM tabela_empresas e
                JOIN relacao_empresa_licenca rel ON e.cnpj = rel.cnpj
                JOIN tabela_licencas l ON rel.nome_licenca = l.nome_licenca
                WHERE e.cnpj = ?
            """, (cnpj,))

            registros = cursor.fetchall()

            if not registros:
                print("Nenhuma empresa encontrada com esse CNPJ.")
                conexao.close()
                return

            # Cabeçalho (pegamos os dados da primeira linha)
            codigo, cnpj, nome_empresa, _, _, _, _, email = registros[0]
            print(f"\nDados da Empresa:")
            print(f"Código: {codigo}")
            print(f"CNPJ: {cnpj}")
            print(f"Nome: {nome_empresa}")
            print(f"E-mail de Notificação: {email}\n")

            print(f"Licenças Vinculadas:\n")

            for _, _, _, nome_licenca, periodicidade, data_base, antecipacao, _ in registros:
                vencimento, envio = calcular_data_vencimento_avisos(periodicidade, data_base, antecipacao)

                print(f"Licença: {nome_licenca}")
                print(f"- Periodicidade: {periodicidade}")
                print(f"- Data Base: {data_base}")
                print(f"- Vencimento: {vencimento}")
                print(f"- Enviar aviso em: {envio}\n")

    except sqlite3.OperationalError as e:
        print(f"Algo deu errado, erro: {e}")
        conexao.rollback()