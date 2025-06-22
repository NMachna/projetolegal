from PySide6.QtWidgets import (
    QApplication, QMainWindow, QDockWidget, QListWidget, 
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QStackedWidget, QTableWidget, 
    QHeaderView, QFormLayout, QComboBox, QTableWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from empresas.funcao_consulta_empresa import obter_empresas
from Interface.estilos import ESTILO_BOTAO, ESTILO_INPUT

class TelaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(15)

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
        self.botao_adicionar = QPushButton("Adicionar")
        self.botao_excluir = QPushButton("Excluir")

        for botao in [self.botao_pesquisar, self.botao_adicionar, self.botao_excluir]:
            botao.setFixedHeight(30)
            botao.setStyleSheet(ESTILO_BOTAO)
            barra_layout.addWidget(botao)

        layout.addLayout(barra_layout)

        self.tabela = QTableWidget(0, 6)
        self.tabela.setHorizontalHeaderLabels(["ID", "Código", "CNPJ", "Nome", "Município", "TAG", "E-mail"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setStyleSheet("font-size: 13px;")
        layout.addWidget(self.tabela)

        self.setLayout(layout)

    def exibir_dados(self, dados):
        colunas = ["ID", "Código", "CNPJ", "Nome", "Município", "TAG", "E-mail"]
        self.tabela.setRowCount(len(dados))
        self.tabela.setColumnCount(len(colunas))
        self.tabela.setHorizontalHeaderLabels(colunas)

        for i, linha in enumerate(dados):
            for j, valor in enumerate(linha):
                item = QTableWidgetItem(str(valor))
                self.tabela.setItem(i, j, item)

        self.tabela.resizeColumnsToContents()

    def carregar_dados(self):
        self.barra_pesquisa.clear()
        dados = obter_empresas()
        self.exibir_dados(dados)
        self.tabela.clearSelection()