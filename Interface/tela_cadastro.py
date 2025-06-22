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

class TelaCadastroEmpresa(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(20)

        titulo = QLabel("Cadastro de Empresa")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(titulo)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)

        self.input_cnpj = QLineEdit()
        self.input_nome = QLineEdit()
        self.input_municipio = QLineEdit()
        self.input_email = QLineEdit()
        self.input_tag = QComboBox()
        self.input_tag.addItems([""])  # As TAGs devem aparecer conforme o usuario adiciona novas

        for label, input_widget in [
            ("CNPJ:", self.input_cnpj),
            ("Nome:", self.input_nome),
            ("Município:", self.input_municipio),
            ("E-mail:", self.input_email),
            ("TAG:", self.input_tag),
        ]:
            input_widget.setStyleSheet(ESTILO_INPUT)
            label_widget = QLabel(label)
            label_widget.setStyleSheet(ESTILO_LABEL)
            form_layout.addRow(label_widget, input_widget)

        layout.addLayout(form_layout)

        self.botao_salvar = QPushButton("Salvar")
        self.botao_salvar.setStyleSheet(ESTILO_BOTAO)
        layout.addWidget(self.botao_salvar, alignment=Qt.AlignRight)

        self.setLayout(layout)