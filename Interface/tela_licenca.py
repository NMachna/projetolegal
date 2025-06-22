from PySide6.QtWidgets import (
    QApplication, QMainWindow, QDockWidget, QListWidget, 
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QStackedWidget, QTableWidget, 
    QHeaderView, QFormLayout, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys
from Interface.estilos import ESTILO_BOTAO, ESTILO_INPUT, ESTILO_LABEL


class TelaLicencas(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        titulo = QLabel("Licenças")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(titulo)

        self.tabela_licencas = QTableWidget(0, 3)
        self.tabela_licencas.setHorizontalHeaderLabels([
            "Licença", "Periodicidade do Vencimento", "Dias de Antecipação"
        ])
        self.tabela_licencas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela_licencas.setStyleSheet("font-size: 13px;")
        layout.addWidget(self.tabela_licencas)

        self.botao_adicionar_licenca = QPushButton("Adicionar Licença")
        self.botao_adicionar_licenca.setStyleSheet(ESTILO_BOTAO)

        self.botao_excluir_licenca = QPushButton("Excluir Licença")
        self.botao_excluir_licenca.setStyleSheet(ESTILO_BOTAO)
        
        for botao in [self.botao_adicionar_licenca, self.botao_excluir_licenca]:
            botao.setFixedHeight(30)
            botao.setStyleSheet(ESTILO_BOTAO)
            layout.addWidget(botao)

        self.setLayout(layout)