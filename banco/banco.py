import os
from sqlalchemy import (
    create_engine, Column, String, Integer, Date, ForeignKey, DateTime
)
from datetime import datetime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Caminho para o banco
CAMINHO_BANCO = os.path.abspath(os.path.join(os.path.dirname(__file__), 'banco.db'))

# Criação do engine com caminho absoluto
db = create_engine(f"sqlite:///{CAMINHO_BANCO}", echo=False)

# Session e Base
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

# Tabela Empresas

class TabelaEmpresa(Base):
    __tablename__ = "tabela_empresas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String, nullable=False)
    cnpj = Column(String, unique=True, nullable=False)
    nome_empresa = Column(String, nullable=False)
    municipio = Column(String, nullable=False)
    tag = Column(String, nullable=False)
    email = Column(String, nullable=False)

    # Uma empresa pode ter várias licenças associadas
    licencas = relationship("RelacaoEmpresaLicenca", back_populates="empresa")

    licencas = relationship(
        "RelacaoEmpresaLicenca",
        back_populates="empresa",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Empresa {self.codigo} - {self.nome_empresa}>"

# -------------------- TABELA LICENÇAS --------------------

class TabelaLicencas(Base):
    __tablename__ = "tabela_licencas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_licenca = Column(String, nullable=False)
    data_base = Column(Date)
    periodicidade = Column(String)
    antecipacao = Column(Integer, nullable=False)

    # Uma licença pode estar relacionada a várias empresas e tags
    empresas = relationship("RelacaoEmpresaLicenca", back_populates="licenca")
    tags = relationship("TabelaTags", back_populates="licenca")

    def __repr__(self):
        return f"<Licença {self.nome_licenca}>"

# -------------------- RELAÇÃO EMPRESA x LICENÇA --------------------

class RelacaoEmpresaLicenca(Base):
    __tablename__ = "relacao_empresa_licenca"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cnpj = Column(String, ForeignKey("tabela_empresas.cnpj", ondelete = "CASCADE"))
    nome_licenca = Column(String, ForeignKey("tabela_licencas.nome_licenca", ondelete = "CASCADE"))
    data_base = Column(Date, nullable=False)
    periodicidade = Column(String, nullable=False)
    antecipacao = Column(Integer, nullable=False)

    empresa = relationship("TabelaEmpresa", back_populates="licencas", passive_deletes = True)
    licenca = relationship("TabelaLicencas", back_populates="empresas", passive_deletes = True)

    def __repr__(self):
        return f"<Relação {self.cnpj} ↔ {self.nome_licenca}>"

# -------------------- TABELA TAGS --------------------

class TabelaTags(Base):
    __tablename__ = "tabela_tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_tag = Column(String, nullable=False)
    id_licenca = Column(Integer, ForeignKey("tabela_licencas.id"))

    licenca = relationship("TabelaLicencas", back_populates="tags")

    def __repr__(self):
        return f"<Tag {self.nome_tag}>"
    
# -------------------- REGISTRO DE E-MAILS ENVIADOS --------------------
class TabelaEnvioEmail(Base):
    __tablename__ = "tabela_envio_email"

    id = Column(Integer, primary_key=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey("tabela_empresas.id"))
    email_destino = Column(String, nullable=False)
    data_envio = Column(DateTime, default=datetime.now)
    licencas_enviadas = Column(String, nullable=False)  # Lista separada por vírgula

    empresa = relationship("TabelaEmpresa")

    def __repr__(self):
        return f"<EnvioEmail {self.email_destino} - {self.data_envio}>"

# -------------------- CRIAÇÃO DAS TABELAS --------------------

Base.metadata.create_all(bind=db)

# -------------------- FUNÇÃO DE DEBUG --------------------

def visualizar_tabelas_orm():
    """Imprime os dados das tabelas usando SQLAlchemy ORM."""
    with Session() as session:
        print("\n=== Empresas ===")
        for empresa in session.query(TabelaEmpresa).all():
            print(empresa)

        print("\n=== Licenças ===")
        for licenca in session.query(TabelaLicencas).all():
            print(licenca)

        print("\n=== Relações Empresa-Licença ===")
        for relacao in session.query(RelacaoEmpresaLicenca).all():
            print(relacao)

        print("\n=== Tags ===")
        for tag in session.query(TabelaTags).all():
            print(tag)

# Executar função se este for o módulo principal
if __name__ == "__main__":
    visualizar_tabelas_orm()