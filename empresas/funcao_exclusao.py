import sqlite3
from banco.banco import criar_conexao


def excluir_empresa():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cnpj = input("Digite o CNPJ da empresa que deseja excluir (apenas números): ")

    cursor.execute("SELECT nome_empresa FROM tabela_empresas WHERE cnpj = ?", (cnpj,))
    empresa = cursor.fetchone()

    if not empresa:
        print("Empresa não encontrada.")
        return

    nome_empresa = empresa[0]

    confirmacao = input(
        f"Tem certeza que deseja excluir a empresa '{nome_empresa}' e todas as suas licenças? (S/N): "
    ).strip().lower()

    if confirmacao == 'n':
        print("Exclusão cancelada.")
    else:
        cursor.execute("DELETE FROM relacao_empresa_licenca WHERE cnpj = ?", (cnpj,))
        cursor.execute("DELETE FROM tabela_empresas WHERE cnpj = ?", (cnpj,))
        conexao.commit()
        print(f"Empresa '{nome_empresa}' e todas as suas licenças foram excluídas com sucesso!")

    conexao.close()

def desassociar_licenca_empresa():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("SELECT cnpj, nome_empresa FROM tabela_empresas")
    empresas = cursor.fetchall()

    if not empresas:
        print("Nenhuma empresa cadastrada.")
        return

    print("\nEmpresas cadastradas:")
    for cnpj, nome in empresas:
        print(f"{cnpj} - {nome}")

    cnpj_escolhido = input("\nDigite o CNPJ da empresa para remover uma licença: ")

    cursor.execute("SELECT nome_licenca FROM relacao_empresa_licenca WHERE cnpj = ?", (cnpj_escolhido,))
    licencas = cursor.fetchall()

    if not licencas:
        print("Esta empresa não possui licenças cadastradas.")
        return

    print("\nLicenças atribuídas à empresa:")
    for licenca in licencas:
        print(f"- {licenca[0]}")

    licenca_escolhida = input("\nDigite o nome da licença que deseja remover: ")

    if licenca_escolhida not in [l[0] for l in licencas]:
        print("Licença não cadastrada para a empresa.")
        return

    confirmacao = input(
        f"Tem certeza que deseja remover a licença '{licenca_escolhida}' da empresa? (S/N): "
    ).strip().lower()

    if confirmacao == 'n':
        print("Ação cancelada pelo usuário.")
        return

    cursor.execute(
        "DELETE FROM relacao_empresa_licenca WHERE cnpj = ? AND nome_licenca = ?",
        (cnpj_escolhido, licenca_escolhida)
    )
    conexao.commit()

    print(f"\nA licença '{licenca_escolhida}' foi removida com sucesso da empresa!")
    conexao.close()