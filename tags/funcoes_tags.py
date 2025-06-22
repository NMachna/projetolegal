import sqlite3
from banco.banco import criar_conexao

"""Cadastra uma nova TAG e associa licenças a ela."""

def obter_tags():
    try:
        with criar_conexao() as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome_tag, id_licenca FROM tabela_tags")
            return cursor.fetchall()
        
    except sqlite3.OperationalError as e:
        print(f"Erro ao obter tags: {e}")
        return []

def cadastrar_tag(nova_tag):
    try:
        with criar_conexao() as conexao:

            cursor = conexao.cursor()

            # Verificar se a TAG já existe
            cursor.execute("SELECT COUNT(*) FROM tabela_tags WHERE nome_tag = ?", (nova_tag,))
            if cursor.fetchone()[0] > 0:
                print("Essa TAG já existe no sistema!")
                conexao.close()
                return

            # Mostrar todas as licenças disponíveis
            cursor.execute("SELECT id_licenca, nome_licenca FROM tabela_licencas")
            licencas_disponiveis = cursor.fetchall()

            if not licencas_disponiveis:
                print("Sem licenças cadastradas. Encerrando")
                conexao.close()

            print("\nLicenças disponíveis para associação:")
            for id_licenca, nome_licenca in licencas_disponiveis:
                print(f"[{id_licenca}] {nome_licenca}")

            # Escolher licenças a serem associadas
            licencas_escolhidas = input("\nDigite os IDs das licenças (separados por vírgula): ")
            licencas_escolhidas = [id.strip() for id in licencas_escolhidas.split(",")]

            # Inserir a nova TAG e associar as licenças
            for id_licenca in licencas_escolhidas:
                cursor.execute("INSERT INTO tabela_tags (nome_tag, id_licenca) VALUES (?, ?)", (nova_tag, id_licenca))

            conexao.commit()
            print(f"TAG '{nova_tag}' cadastrada com sucesso!")

    except sqlite3.OperationalError as e:
        print(f"Algo deu errado, erro: {e}")
        conexao.rollback()



"""Exclui uma TAG e remove todas as relações dela com empresas e licenças."""

def excluir_tag(tag):
    try:
        with criar_conexao() as conexao:
            cursor = conexao.cursor()

            cursor.execute("SELECT * FROM tabela_tags WHERE nome_tag = ?", (tag,))
            tag_existente = cursor.fetchone()

            if not tag_existente:
                print(f"A TAG '{tag}' não existe no sistema.")
                conexao.close()
                return

            # Verificar se há empresas associadas à TAG
            cursor.execute("SELECT cnpj FROM tabela_empresas WHERE tag = ?", (tag,))
            empresas_vinculadas = cursor.fetchall()

            if empresas_vinculadas:
                print(f"A TAG '{tag}' está vinculada a {len(empresas_vinculadas)} empresa(s).")
                confirmacao = input("Deseja realmente excluir essa TAG e remover suas associações? (S/N): ").strip().lower()
                if confirmacao == 'n':
                    print("Exclusão cancelada.")
                    conexao.close()
                    return

                # Remover licenças associadas à TAG de cada empresa
                for (cnpj,) in empresas_vinculadas:
                    cursor.execute("""
                        DELETE FROM relacao_empresa_licenca
                        WHERE cnpj = ?
                        AND nome_licenca IN (
                        SELECT nome_licenca FROM tabela_licencas
                        WHERE id_licenca IN (
                        SELECT id_licenca FROM tabela_tags WHERE nome_tag = ?
                                )
                        )
                    """, (cnpj, tag))

                # Remover a TAG das empresas
                cursor.execute("UPDATE tabela_empresas SET tag = NULL WHERE tag = ?", (tag,))

            # Excluir a TAG do banco
            cursor.execute("DELETE FROM tabela_tags WHERE nome_tag = ?", (tag,))
            conexao.commit()

            print(f"A TAG '{tag}' foi excluída com sucesso.")

    except sqlite3.OperationalError as e:
        print(f"Algo deu errado, erro: {e}")
        conexao.rollback()


"""Remove a TAG de uma empresa específica e suas licenças associadas à TAG."""

def remover_tag_de_empresa():
    try:
        with criar_conexao() as conexao:
            cursor = conexao.cursor()

            # Listar empresas e suas TAGs
            cursor.execute("SELECT cnpj, nome_empresa, tag FROM tabela_empresas")
            empresas = cursor.fetchall()

            if not empresas:
                print("Nenhuma empresa cadastrada.")
                conexao.close()
                return

            print("\nEmpresas cadastradas e suas TAGs:")
            for cnpj, nome, tag in empresas:
                tag_info = tag if tag else "Nenhuma"
                print(f"{cnpj} - {nome} | TAG: {tag_info}")

            cnpj_escolhido = input("\nDigite o CNPJ da empresa para remover a TAG: ")

            cursor.execute("SELECT tag FROM tabela_empresas WHERE cnpj = ?", (cnpj_escolhido,))
            tag_atual = cursor.fetchone()

            if not tag_atual or not tag_atual[0]:
                print("Essa empresa não possui uma TAG atribuída.")
                conexao.close()
                return

            confirmacao = input(f"Tem certeza que deseja remover a TAG '{tag_atual[0]}' da empresa? (S/N): ").strip().lower()
            if confirmacao == 'n':
                print("Ação cancelada.")
                conexao.close()
                return

            # Remover TAG da empresa
            cursor.execute("UPDATE tabela_empresas SET tag = NULL WHERE cnpj = ?", (cnpj_escolhido,))

            # Remover licenças associadas à TAG
            cursor.execute("""
                DELETE FROM relacao_empresa_licenca
                WHERE cnpj = ?
                AND nome_licenca IN (
                    SELECT nome_licenca FROM tabela_licencas
                    WHERE id_licenca IN (
                        SELECT id_licenca FROM tabela_tags WHERE nome_tag = ?
                    )
                )
            """, (cnpj_escolhido, tag_atual[0]))

            conexao.commit()
            print(f"A TAG '{tag_atual[0]}' foi removida com sucesso da empresa.")
            
    except sqlite3.OperationalError as e:
        print(f"Algo deu errado, erro: {e}")
        conexao.rollback()