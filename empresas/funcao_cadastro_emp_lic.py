from datetime import datetime
from banco.banco import criar_conexao

"""Nestas funções, o úsuario escolhe uma empresa por meio do CNPJ e atribui uma TAG ou licença a mesma."""

def associar_empresa_a_tag_ou_licenca():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    # Mostrar empresas cadastradas
    cursor.execute("SELECT CNPJ, Nome_Empresa FROM Tabela_Empresas")
    empresas = cursor.fetchall()

    if not empresas:
        print("Nenhuma empresa cadastrada.")
        return

    print("\nEmpresas cadastradas:")
    for cnpj, nome in empresas:
        print(f"{cnpj} - {nome}")

    cnpj_escolhido = input("\nDigite o CNPJ da empresa que deseja modificar: ").strip()

    cursor.execute("SELECT Nome_Empresa FROM Tabela_Empresas WHERE CNPJ = ?", (cnpj_escolhido,))
    empresa = cursor.fetchone()

    if not empresa:
        print("Empresa não encontrada.")
        return

    print(f"\nEmpresa selecionada: {empresa[0]}")

    print("\nO que deseja fazer?")
    print("[1] Atribuir uma nova TAG")
    print("[2] Adicionar licenças manualmente")

    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        atribuir_tag_a_empresa(cursor, conexao, cnpj_escolhido, empresa[0])

    elif opcao == "2":
        adicionar_licencas_manual(cursor, conexao, cnpj_escolhido, empresa[0])

    else:
        print("Opção inválida.")

    conexao.close()


def atribuir_tag_a_empresa(cursor, conexao, cnpj, nome_empresa):
    cursor.execute("SELECT DISTINCT Nome_TAG FROM Tabela_TAGs")
    tags = cursor.fetchall()

    if not tags:
        print("Nenhuma TAG cadastrada.")
        return

    print("\nTags disponíveis:")
    for tag in tags:
        print(f"- {tag[0]}")

    tag_escolhida = input("\nDigite o nome da TAG que deseja atribuir: ").strip()

    cursor.execute("SELECT ID_Licenca FROM Tabela_TAGs WHERE Nome_TAG = ?", (tag_escolhida,))
    licencas = cursor.fetchall()

    if not licencas:
        print("TAG não encontrada ou sem licenças associadas.")
        return

    print(f"\nA TAG '{tag_escolhida}' contém as seguintes licenças:")
    for (id_licenca,) in licencas:
        cursor.execute("SELECT Nome_Licenca FROM Tabela_Licencas WHERE ID_Licenca = ?", (id_licenca,))
        nome_licenca = cursor.fetchone()
        print(f"- {nome_licenca[0]}")

    confirmacao = input("\nDeseja realmente associar essa TAG e suas licenças à empresa? (S/N): ").strip().lower()

    if confirmacao != 's':
        print("Ação cancelada pelo usuário.")
        return

    for (id_licenca,) in licencas:
        cursor.execute(
            "SELECT Nome_Licenca, Periodicidade, Antecipacao FROM Tabela_Licencas WHERE ID_Licenca = ?",
            (id_licenca,)
        )
        dados_licenca = cursor.fetchone()

        if dados_licenca:
            nome_licenca, periodicidade, antecipacao = dados_licenca

            data_base = obter_data_base(nome_licenca)

            cursor.execute("""
                INSERT OR IGNORE INTO Relacao_Empresa_Licenca 
                (CNPJ, Nome_Licenca, Data_Base, Periodicidade, Antecipacao) 
                VALUES (?, ?, ?, ?, ?)
            """, (cnpj, nome_licenca, data_base, periodicidade, antecipacao))
            conexao.commit()

    cursor.execute("UPDATE Tabela_Empresas SET TAG = ? WHERE CNPJ = ?", (tag_escolhida, cnpj))
    conexao.commit()

    print(f"\nA TAG '{tag_escolhida}' foi atribuída com sucesso à empresa {nome_empresa}.")


def adicionar_licencas_manual(cursor, conexao, cnpj, nome_empresa):
    cursor.execute("SELECT TAG FROM Tabela_Empresas WHERE CNPJ = ?", (cnpj,))
    tag_atual = cursor.fetchone()

    if not tag_atual or not tag_atual[0]:
        print("Essa empresa ainda não possui uma TAG associada. Atribua uma TAG primeiro.")
        return

    cursor.execute("SELECT Nome_Licenca FROM Relacao_Empresa_Licenca WHERE CNPJ = ?", (cnpj,))
    licencas_existentes = {lic[0] for lic in cursor.fetchall()}

    cursor.execute("SELECT Nome_Licenca, ID_Licenca FROM Tabela_Licencas")
    todas_licencas = cursor.fetchall()

    licencas_disponiveis = [(nome, id_) for nome, id_ in todas_licencas if nome not in licencas_existentes]

    if not licencas_disponiveis:
        print("Todas as licenças já estão atribuídas a esta empresa.")
        return

    print("\nLicenças disponíveis para adicionar:")
    for nome, _ in licencas_disponiveis:
        print(f"- {nome}")

    licencas_input = input("\nDigite os nomes das licenças que deseja adicionar (separados por vírgula): ")
    licencas_escolhidas = [lic.strip() for lic in licencas_input.split(",")]

    licencas_validas = [lic for lic in licencas_disponiveis if lic[0] in licencas_escolhidas]

    if not licencas_validas:
        print("Nenhuma das licenças digitadas é válida.")
        return

    for nome_licenca, id_licenca in licencas_validas:
        cursor.execute("""
            SELECT Nome_Licenca, Periodicidade, Antecipacao 
            FROM Tabela_Licencas 
            WHERE ID_Licenca = ?
        """, (id_licenca,))
        dados_licenca = cursor.fetchone()

        if dados_licenca:
            nome_licenca, periodicidade, antecipacao = dados_licenca
            data_base = obter_data_base(nome_licenca)

            cursor.execute("""
                INSERT OR IGNORE INTO Relacao_Empresa_Licenca 
                (CNPJ, Nome_Licenca, Data_Base, Periodicidade, Antecipacao, Origem_TAG)
                VALUES (?, ?, ?, ?, ?, 1)
            """, (cnpj, nome_licenca, data_base, periodicidade, antecipacao))
            conexao.commit()

    print(f"\nLicenças adicionadas com sucesso à empresa {nome_empresa}.")


def obter_data_base(nome_licenca: str) -> str:
    while True:
        data_base = input(f"Digite a data base para a licença '{nome_licenca}' (AAAA-MM-DD): ").strip()
        try:
            datetime.strptime(data_base, "%Y-%m-%d")
            return data_base
        except ValueError:
            print("Formato inválido. Use AAAA-MM-DD.")