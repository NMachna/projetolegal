from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,QPushButton, 
    QTableWidget, QHeaderView, QTableWidgetItem, 
    QDialog, QAbstractScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from tags.funcoes_tags import obter_tags
from Interface.estilos import ESTILO_BOTAO, ESTILO_TABELA

class TelaTags(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        titulo = QLabel("TAGS")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(titulo)

        self.tabela_tags = QTableWidget(0, 1)  # Apenas 1 coluna agora
        self.tabela_tags.setHorizontalHeaderLabels(["Nome TAG"])
        self.tabela_tags.setStyleSheet(ESTILO_TABELA)
        self.tabela_tags.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela_tags.setStyleSheet("font-size: 13px;")
        layout.addWidget(self.tabela_tags)

        self.botao_adicionar_tag = QPushButton("Adicionar TAG")
        self.botao_adicionar_tag.setStyleSheet(ESTILO_BOTAO)
        layout.addWidget(self.botao_adicionar_tag, alignment=Qt.AlignRight)

        self.carregar_tags()
        self.setLayout(layout)
        self.tabela_tags.cellDoubleClicked.connect(self.abrir_detalhes_tags)
    
    def carregar_tags(self):
        self.tags = obter_tags()
        self.tabela_tags.setRowCount(len(self.tags))

        for i, (nome_tag, _) in enumerate(self.tags):
            self.tabela_tags.setItem(i, 0, QTableWidgetItem(nome_tag))

    def abrir_detalhes_tags(self, row):
        nome_tag, licencas = self.tags[row]

        dialogo = QDialog(self)
        dialogo.setWindowTitle(f"Licenças vinculadas à TAG '{nome_tag}'")

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        tabela = QTableWidget()
        tabela.setColumnCount(3)
        tabela.setHorizontalHeaderLabels(["Nome da Licença", "Periodicidade", "Antecipação"])
        tabela.setRowCount(len(licencas))

        for i, (_, nome_licenca, periodicidade, antecipacao) in enumerate(licencas):
            tabela.setItem(i, 0, QTableWidgetItem(nome_licenca))
            tabela.setItem(i, 1, QTableWidgetItem(periodicidade))
            tabela.setItem(i, 2, QTableWidgetItem(str(antecipacao)))

        tabela.resizeColumnsToContents()
        tabela.resizeRowsToContents()
        tabela.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        layout.addWidget(tabela)

        botao_fechar = QPushButton("Fechar")
        botao_fechar.setStyleSheet(ESTILO_BOTAO)
        botao_fechar.clicked.connect(dialogo.close)
        layout.addWidget(botao_fechar, alignment=Qt.AlignRight)

        dialogo.setLayout(layout)
        dialogo.setFont(QFont("Segoe UI", 12))

        # Ajusta tamanho com base na tabela
        largura = tabela.verticalHeader().width()
        for i in range(tabela.columnCount()):
            largura += tabela.columnWidth(i)

        altura = tabela.horizontalHeader().height()
        for i in range(tabela.rowCount()):
            altura += tabela.rowHeight(i)

        largura += 50
        altura += 100

        dialogo.resize(largura, altura)
        dialogo.exec()