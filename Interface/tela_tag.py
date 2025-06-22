from PySide6.QtWidgets import (
    QApplication, QMainWindow, QDockWidget, QListWidget, 
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QStackedWidget, QTableWidget, 
    QHeaderView, QFormLayout, QComboBox, QTableWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from tags.funcoes_tags import obter_tags
from Interface.estilos import ESTILO_BOTAO, ESTILO_INPUT, ESTILO_LABEL

class TelaTags(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        titulo = QLabel("TAGS")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(titulo)

        self.tabela_tags = QTableWidget(0, 2)
        self.tabela_tags.setHorizontalHeaderLabels(["ID", "Nome da TAG", "ID Licença"]) # Descrição seria opcional
        self.tabela_tags.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela_tags.setStyleSheet("font-size: 13px;")
        layout.addWidget(self.tabela_tags)

        self.botao_adicionar_tag = QPushButton("Adicionar TAG")
        self.botao_adicionar_tag.setStyleSheet(ESTILO_BOTAO)
        layout.addWidget(self.botao_adicionar_tag, alignment=Qt.AlignRight)

        self.carregar_tags()
        self.setLayout(layout)
    
    def carregar_tags(self):
        dados = obter_tags()
        print("TAGS CARREGADAS:", dados)
        self.tabela_tags.setRowCount(len(dados))

        for i, linha in enumerate(dados):
            for j, valor in enumerate(linha):
                self.tabela_tags.setItem(i, j, QTableWidgetItem(str(valor)))