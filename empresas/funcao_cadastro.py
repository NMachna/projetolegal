import sqlite3
from datetime import datetime
from tags.funcoes_tags import cadastrar_tag
from banco.banco import criar_conexao


"""Cadastra uma nova empresa e, se precisar, uma nova TAG"""

def cadastrar_empresa():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    # Coletar dados da empresa
    codigo = input("Digite o código da Empresa: ").strip()
    cnpj = input("Digite o CNPJ da Empresa (Apenas números): ").strip()
    nome_empresa = input("Digite o Nome da Empresa: ").strip()
    municipio = input("Informe o Município da Empresa: ").strip()
    tag_escolhida = input("Adicione o Nome da TAG (CND) que deseja cadastrar a Empresa: ").strip()
    email = input("Informe o(s) e-mail(s) de notificação: ").strip()

    nova_empresa = (codigo, cnpj, nome_empresa, municipio, tag_escolhida, email)

    # Verificar duplicidade por CNPJ ou Código
    cursor.execute("SELECT * FROM Tabela_Empresas WHERE CNPJ = ? OR Codigo = ?", (cnpj, codigo))
    if cursor.fetchone():
        print("Já existe uma empresa cadastrada com esse CNPJ ou código.")
        conexao.close()
        return

    # Inserir empresa no banco
    cursor.execute("""
        INSERT INTO Tabela_Empresas (Codigo, CNPJ, Nome_Empresa, Municipio, TAG, Email)
        VALUES (?, ?, ?, ?, ?, ?)
    """, nova_empresa)
    conexao.commit()

    # Verificar se a TAG existe
    cursor.execute("SELECT * FROM Tabela_TAGs WHERE Nome_TAG = ?", (tag_escolhida,))
    if not cursor.fetchone():
        print(f"A TAG '{tag_escolhida}' não existe. Vamos cadastrá-la.")
        cadastrar_tag(tag_escolhida)

    # Buscar licenças associadas à TAG
    cursor.execute("SELECT ID_Licenca FROM Tabela_TAGs WHERE Nome_TAG = ?", (tag_escolhida,))
    licencas = cursor.fetchall()

    for (id_licenca,) in licencas:
        # Buscar os dados da licença
        cursor.execute("""
            SELECT Nome_Licenca, Periodicidade, Antecipacao 
            FROM Tabela_Licencas 
            WHERE ID_Licenca = ?
        """, (id_licenca,))
        dados_licenca = cursor.fetchone()

        if dados_licenca:
            nome_licenca, periodicidade, antecipacao = dados_licenca

            # Solicita a Data Base com validação
            while True:
                data_base = input(
                    f"Digite a data base da licença '{nome_licenca}' (Formato: YYYY-MM-DD): ").strip()
                try:
                    datetime.strptime(data_base, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Formato inválido. Use YYYY-MM-DD.")

            # Inserir relação Empresa <-> Licença
            cursor.execute("""
                INSERT INTO Relacao_Empresa_Licenca (CNPJ, Nome_Licenca, Data_Base, Periodicidade, Antecipacao)
                VALUES (?, ?, ?, ?, ?)
            """, (cnpj, nome_licenca, data_base, periodicidade, antecipacao))
            conexao.commit()

    print(f"\nA empresa '{nome_empresa}' foi cadastrada com sucesso!")
    conexao.close()