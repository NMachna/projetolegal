import sqlite3
from banco.banco import criar_conexao

"""Funções para adicionar e excluir licenças da tabela de licenças"""

def adicionar_licenca():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    nome_licenca = input("Digite o nome da licença: ").strip()
    periodicidade = input("Digite a periodicidade da licença (Anual, Semestral, Mensal): ").strip().lower()

    try:
        antecipacao = int(input("Digite a quantidade de dias de antecedência para o alerta: "))
    except ValueError:
        print("Valor inválido para antecedência. Digite um número inteiro.")
        conexao.close()
        return

    cursor.execute("""
        INSERT INTO Tabela_Licencas (Nome_Licenca, Periodicidade, Antecipacao)
        VALUES (?, ?, ?)
    """, (nome_licenca, periodicidade, antecipacao))
    conexao.commit()

    print(f"\nA licença '{nome_licenca}' foi adicionada com sucesso!")

    conexao.close()


def excluir_licenca():
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("SELECT ID_Licenca, Nome_Licenca FROM Tabela_Licencas")
    licencas = cursor.fetchall()

    if not licencas:
        print("Nenhuma licença cadastrada.")
        conexao.close()
        return

    print("\nLicenças cadastradas:")
    for id_licenca, nome_licenca in licencas:
        print(f"{id_licenca} - {nome_licenca}")

    nome_escolhido = input("\nDigite o nome da licença que deseja excluir: ").strip()

    # Verifica se a licença está associada a alguma empresa
    cursor.execute("SELECT COUNT(*) FROM Relacao_Empresa_Licenca WHERE Nome_Licenca = ?", (nome_escolhido,))
    associacoes = cursor.fetchone()[0]

    if associacoes > 0:
        print("Não é possível excluir a licença. Ela está associada a uma ou mais empresas.")
        conexao.close()
        return

    cursor.execute("DELETE FROM Tabela_Licencas WHERE Nome_Licenca = ?", (nome_escolhido,))
    conexao.commit()

    print(f"\nA licença '{nome_escolhido}' foi excluída com sucesso!")

    conexao.close()