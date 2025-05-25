from PySide6.QtWidgets import (
    QApplication, QMainWindow, QDockWidget, QListWidget, 
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QStackedWidget, QTableWidget, 
    QHeaderView, QFormLayout, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys

# ---------- Estilo global ----------
ESTILO_BOTAO = """
    QPushButton {
        background-color: #3498db;
        color: white;
        border-radius: 4px;
        padding: 6px 12px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #2980b9;
    }
"""

ESTILO_INPUT = "QLineEdit { padding: 6px; font-size: 14px; }"
ESTILO_LABEL = "QLabel { font-size: 14px; }"

# ---------- Janela Principal da Interface ----------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Controle de Empresas")
        self.showMaximized()

        self.stack = QStackedWidget()

        self.tela_principal = TelaPrincipal()
        self.tela_cadastro = TelaCadastroEmpresa()
        self.tela_licencas = TelaLicencas()
        self.tela_tags = TelaTags()


        """Indices das Telas/Janelas"""
        self.stack.addWidget(self.tela_principal)   # índice 0
        self.stack.addWidget(self.tela_cadastro)    # índice 1
        self.stack.addWidget(self.tela_licencas)    # índice 2
        self.stack.addWidget(self.tela_tags)        # índice 3

        self.setCentralWidget(self.stack)

        """Definindo o Menu"""
        self.menu_lateral = QDockWidget("Menu", self)
        self.lista_menu = QListWidget()
        self.lista_menu.addItems([
            "Menu Principal", "Cadastro de Empresas", 
            "Licenças", "TAGS", "Relatórios", "Alertas"
        ])
        self.lista_menu.setStyleSheet("padding: 10px; font-size: 14px;")
        self.menu_lateral.setFixedWidth(180)
        self.menu_lateral.setWidget(self.lista_menu)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.menu_lateral)

        self.lista_menu.itemClicked.connect(self.mudar_tela)


    """Função para mudanças de Telas"""
    def mudar_tela(self, item):
        texto = item.text()
        if texto == "Menu Principal":
            self.stack.setCurrentIndex(0)
        elif texto == "Cadastro de Empresas":
            self.stack.setCurrentIndex(1)
        elif texto == "Licenças":
            self.stack.setCurrentIndex(2)
        elif texto == "TAGS":
            self.stack.setCurrentIndex(3)

# ---------- Menu Principal ----------
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

        # Setando a tabeela
        self.tabela = QTableWidget(0, 6)
        self.tabela.setHorizontalHeaderLabels(["Código", "CNPJ", "Nome", "Município", "TAG", "E-mail"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setStyleSheet("font-size: 13px;")
        layout.addWidget(self.tabela)

        self.setLayout(layout)

# ---------- Tela de Cadastro ----------
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

# ---------- Tela de Licenças ----------
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

# ---------- Tela de TAGs ----------
class TelaTags(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        titulo = QLabel("TAGS")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(titulo)

        self.tabela_tags = QTableWidget(0, 2)
        self.tabela_tags.setHorizontalHeaderLabels(["Nome da TAG", "Descrição"]) # Descrição seria opcional
        self.tabela_tags.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela_tags.setStyleSheet("font-size: 13px;")
        layout.addWidget(self.tabela_tags)

        self.botao_adicionar_tag = QPushButton("Adicionar TAG")
        self.botao_adicionar_tag.setStyleSheet(ESTILO_BOTAO)
        layout.addWidget(self.botao_adicionar_tag, alignment=Qt.AlignRight)

        self.setLayout(layout)

# ---------- Execução ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    screen_geometry = app.primaryScreen().availableGeometry()
    window.setGeometry(screen_geometry)
    window.show()
    sys.exit(app.exec())