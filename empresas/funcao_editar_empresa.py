import sqlite3
from datetime import datetime
from banco.banco import criar_conexao


def editar_empresa():
    try:
        with criar_conexao() as conexao:

            cursor = conexao.cursor()

            cnpj = input("Digite o CNPJ da empresa que deseja editar (apenas números): ").strip()

            cursor.execute("SELECT codigo, nome_empresa, municipio, email FROM tabela_empresas WHERE cnpj = ?", (cnpj,))
            empresa = cursor.fetchone()

            if not empresa:
                print("Empresa não encontrada.")
                conexao.close()
                return

            codigo, nome_empresa, municipio, email = empresa

            print(f"\nEmpresa a ser alterada: {nome_empresa}")
            print("[1] Editar várias informações.")
            print("[2] Editar apenas uma informação.")
            opcao = input("Qual tipo de alteração deseja fazer? (1/2): ").strip()

            if opcao == '1':
                novo_nome = input(f"Novo nome da empresa (atualmente {nome_empresa}): ").strip()
                novo_codigo = input(f"Novo código (atualmente {codigo}): ").strip()
                novo_municipio = input(f"Novo município (atualmente {municipio}): ").strip()
                novo_email = input(f"Novo e-mail (atualmente {email}): ").strip()

                cursor.execute("""
                    UPDATE tabela_empresas 
                    SET nome_empresa = ?, codigo = ?, municipio = ?, email = ? 
                    WHERE cnpj = ?
                """, (novo_nome, novo_codigo, novo_municipio, novo_email, cnpj))
                print("Informações atualizadas com sucesso!")

            elif opcao == '2':
                print("\n[1] Nome da empresa")
                print("[2] Código da empresa")
                print("[3] Município")
                print("[4] E-mail")
                escolha = input("Escolha o que deseja alterar (1/2/3/4): ").strip()

                campos = {
                    '1': ("nome_empresa", "Nome da empresa", nome_empresa),
                    '2': ("codigo", "Código", codigo),
                    '3': ("municipio", "Município", municipio),
                    '4': ("email", "E-mail", email)
                }

                if escolha in campos:
                    campo_sql, descricao, valor_atual = campos[escolha]
                    novo_valor = input(f"Novo {descricao} (atualmente {valor_atual}): ").strip()

                    cursor.execute(f"UPDATE tabela_empresas SET {campo_sql} = ? WHERE cnpj = ?", (novo_valor, cnpj))
                    print(f"{descricao} atualizado com sucesso!")
                else:
                    print("Opção inválida.")

            else:
                print("Opção inválida.")

            conexao.commit()

    except sqlite3.OperationalError as e:
        print(f"Algo deu errado, erro: {e}")
        conexao.rollback()



def editar_datas_licencas_empresa():
    try:
        with criar_conexao() as conexao:

            cursor = conexao.cursor()

            cnpj = input("Digite o CNPJ da empresa para editar as datas das licenças: ").strip()

            cursor.execute("SELECT nome_empresa FROM tabela_empresas WHERE cnpj = ?", (cnpj,))
            empresa = cursor.fetchone()

            if not empresa:
                print("Empresa não encontrada.")
                conexao.close()
                return

            nome_empresa = empresa[0]
            print(f"\nEmpresa encontrada: {nome_empresa}")

            cursor.execute("""
                SELECT l.nome_licenca, rel.data_base
                FROM relacao_empresa_licenca rel
                JOIN tabela_licencas l ON rel.nome_licenca = l.nome_licenca
                WHERE rel.cnpj = ?
            """, (cnpj,))
            licencas = cursor.fetchall()

            if not licencas:
                print("Nenhuma licença associada a essa empresa.")
                conexao.close()
                return

            print("\nLicenças associadas:")
            for i, (nome_licenca, data_base) in enumerate(licencas, 1):
                print(f"[{i}] {nome_licenca} | Data Base: {data_base}")

            escolha = input("\nDigite o número da licença que deseja editar: ").strip()
            if not escolha.isdigit() or not (1 <= int(escolha) <= len(licencas)):
                print("Opção inválida.")
                conexao.close()
                return

            nome_licenca, data_base_atual = licencas[int(escolha) - 1]

            nova_data = input(
                f"Nova data base para '{nome_licenca}' (formato YYYY-MM-DD) ou pressione Enter para manter '{data_base_atual}': "
            ).strip()

            if nova_data:
                try:
                    datetime.strptime(nova_data, "%Y-%m-%d")
                except ValueError:
                    print("Formato inválido. A data não foi alterada.")
                    conexao.close()
                    return
            else:
                nova_data = data_base_atual

            cursor.execute("""
                UPDATE relacao_empresa_licenca 
                SET data_base = ? 
                WHERE cnpj = ? AND nome_licenca = ?
            """, (nova_data, cnpj, nome_licenca))

            conexao.commit()

            print(f"\nA data base da licença '{nome_licenca}' foi atualizada para {nova_data}")

    except sqlite3.OperationalError as e:
        print(f"Algo deu errado, erro: {e}")
        conexao.rollback()