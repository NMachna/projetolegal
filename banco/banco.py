import os
import sqlite3

CAMINHO_BANCO = os.path.join(os.path.dirname(__file__), 'banco.db')

def criar_conexao():
    """Cria e retorna uma conexão com o banco de dados SQLite3."""
    return sqlite3.connect(CAMINHO_BANCO)


def criar_tabelas():
    """Cria todas as tabelas do banco de dados, *se* ainda não existirem."""
    conexao = criar_conexao()
    cursor = conexao.cursor()

    # Tabela de empresas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tabela_empresas (
            codigo TEXT,
            cnpj TEXT UNIQUE PRIMARY KEY,
            nome_empresa TEXT NOT NULL,
            municipio TEXT NOT NULL,
            tag TEXT,
            email TEXT NOT NULL
        )
    """)

    # Tabela de licenças
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tabela_licencas (
            id_licenca INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_licenca TEXT NOT NULL,
            data_base DATE,
            periodicidade TEXT,
            antecipacao INTEGER NOT NULL
        )
    """)

    # Relação Empresa <-> Licença
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS relacao_empresa_licenca (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cnpj TEXT,
            nome_licenca TEXT,
            data_base DATE NOT NULL,
            periodicidade TEXT NOT NULL,
            antecipacao INTEGER NOT NULL,
            origem_tag INTEGER DEFAULT 0,
            FOREIGN KEY (cnpj) REFERENCES tabela_empresas(cnpj),
            FOREIGN KEY (nome_licenca) REFERENCES tabela_licencas(nome_licenca),
            UNIQUE (cnpj, nome_licenca)
        )
    """)

    # Tabela de TAGs e Licenças
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tabela_tags (
            id_tag INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_tag TEXT NOT NULL,
            id_licenca TEXT NOT NULL,
            FOREIGN KEY (id_licenca) REFERENCES tabela_licencas(id_licenca)
        )
    """)

    conexao.commit()
    conexao.close()


def visualizar_tabelas():
    """Imprime os dados das tabelas no terminal para debug ou inspeção."""
    conexao = criar_conexao()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM tabela_empresas")
    empresas = cursor.fetchall()
    print("Tabela_Empresas:")
    for empresa in empresas:
        print(empresa)

    cursor.execute("SELECT * FROM tabela_licencas")
    licencas = cursor.fetchall()
    print("\nTabela_Licencas:")
    for licenca in licencas:
        print(licenca)

    cursor.execute("SELECT * FROM relacao_empresa_licenca")
    relacoes = cursor.fetchall()
    print("\nRelacao_Empresa_Licenca:")
    for relacao in relacoes:
        print(relacao)

    cursor.execute("SELECT * FROM tabela_tags")
    tags = cursor.fetchall()
    print("\nTabela_TAGs:")
    for tag in tags:
        print(tag)

    conexao.close()

#criar_tabelas()
visualizar_tabelas()