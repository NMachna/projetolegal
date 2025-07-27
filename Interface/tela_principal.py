from PySide6.QtWidgets import (
    QMessageBox, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QHeaderView,
    QTableWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from banco.banco import Session, TabelaEmpresa, RelacaoEmpresaLicenca
from Interface.estilos import ESTILO_BOTAO, ESTILO_INPUT, ESTILO_TABELA


class TelaPrincipal(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()
        layout.setSpacing(15)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        titulo = QLabel("Consulta de Empresas")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignLeft)
        layout.addWidget(titulo)

        barra_layout = QHBoxLayout()
        barra_layout.setSpacing(10)

        self.barra_pesquisa = QLineEdit()
        self.barra_pesquisa.setPlaceholderText("Digite o CNPJ da empresa")
        self.barra_pesquisa.setFixedHeight(30)
        self.barra_pesquisa.setStyleSheet(ESTILO_INPUT)
        barra_layout.addWidget(self.barra_pesquisa)

        self.botao_pesquisar = QPushButton("Pesquisar")
        self.botao_adicionar = QPushButton("Cadastrar")
        self.botao_excluir = QPushButton("Excluir")

        self.botao_adicionar.clicked.connect(self.ir_para_cadastro)
        self.botao_excluir.clicked.connect(self.excluir_empresa_selecionada)

        for botao in [self.botao_pesquisar, self.botao_adicionar, self.botao_excluir]:
            botao.setFixedHeight(30)
            botao.setStyleSheet(ESTILO_BOTAO)
            barra_layout.addWidget(botao)

        layout.addLayout(barra_layout)

        self.tabela = QTableWidget(0, 7)
        self.tabela.setHorizontalHeaderLabels(["ID", "Código", "CNPJ", "Nome", "Município", "TAG", "E-mail"])
        self.tabela.setStyleSheet(ESTILO_TABELA)
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setStyleSheet("font-size: 13px;")
        layout.addWidget(self.tabela)

        self.setLayout(layout)

    def exibir_dados(self, dados):
        colunas = ["ID", "Código", "CNPJ", "Nome", "Município", "TAG", "E-mail"]
        self.tabela.setRowCount(len(dados))
        self.tabela.setColumnCount(len(colunas))
        self.tabela.setHorizontalHeaderLabels(colunas)

        for i, empresa in enumerate(dados):
            valores = [
                empresa.id,
                empresa.codigo,
                empresa.cnpj,
                empresa.nome_empresa,
                empresa.municipio,
                empresa.tag,
                empresa.email
            ]
            for j, valor in enumerate(valores):
                item = QTableWidgetItem(str(valor))
                self.tabela.setItem(i, j, item)

        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def carregar_dados(self):
        self.barra_pesquisa.clear()
        try:
            with Session() as session:
                empresas = session.query(TabelaEmpresa).all()
                self.exibir_dados(empresas)

        except Exception as e:
            QMessageBox.critical(self, "Erro ao carregar", str(e))

    def pesquisar_empresa(self):
        termo = self.barra_pesquisa.text().strip()
        try:
            with Session() as session:
                if termo:
                    empresas = session.query(TabelaEmpresa).filter(TabelaEmpresa.cnpj.like(f"%{termo}%")).all()
                else:
                    empresas = session.query(TabelaEmpresa).all()
                self.exibir_dados(empresas)
        except Exception as e:
            QMessageBox.critical(self, "Erro na pesquisa", str(e))


    def ir_para_cadastro(self):
        self.main_window.stack.setCurrentWidget(self.main_window.tela_cadastro)

    def excluir_empresa_selecionada(self):
        linha_selecionada = self.tabela.currentRow()
        if linha_selecionada == -1:
            QMessageBox.warning(self, "Nenhuma seleção", "Selecione uma empresa para excluir.")
            return

        cnpj = self.tabela.item(linha_selecionada, 2).text() # Coluna CNPJ
        nome_empresa = self.tabela.item(linha_selecionada, 3).text() # Coluna Nome

        resposta = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir a empresa '{nome_empresa}' com CNPJ {cnpj}",
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta == QMessageBox.No:
            return # Ação cancelada
        
        try:
            with Session() as session:
                session.query(RelacaoEmpresaLicenca).filter_by(cnpj = cnpj).delete()

                empresa = session.query(TabelaEmpresa).filter_by(cnpj=cnpj).first()
                if empresa:
                    session.delete(empresa)
                    session.commit()
                    QMessageBox.information(self, "Sucesso", f"Empresa '{nome_empresa}' excluída com sucesso.")
                    self.carregar_dados()
                else:
                    QMessageBox.warning(self, "Não encontrada", "Empresa não encontrada.")
        except Exception as e:
            QMessageBox.critical(self, "Erro ao excluir", str(e))