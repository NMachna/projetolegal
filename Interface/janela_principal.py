from PySide6.QtWidgets import QMainWindow, QDockWidget, QListWidget, QStackedWidget
from PySide6.QtCore import Qt

from Interface.tela_principal import TelaPrincipal
from Interface.tela_cadastro import TelaCadastroEmpresa
from Interface.tela_licenca import TelaLicencas
from Interface.tela_tag import TelaTags
from Interface.tela_alerta import TelaAlertas
from Interface.tela_relatorios import TelaRelatorios
from Interface.tela_licencas_empresas import TelaRenovacaoLicencas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Controle de Empresas")
        self.showMaximized()
        self.setStyleSheet("background-color: #f0f2f5;")

        self.stack = QStackedWidget()

        # Telas
        self.tela_principal = TelaPrincipal(self)
        self.tela_cadastro = TelaCadastroEmpresa()
        self.tela_licencas = TelaLicencas()
        self.tela_tags = TelaTags()
        self.tela_alertas = TelaAlertas()
        self.tela_relatorios = TelaRelatorios(self)
        self.tela_licencas_empresas = TelaRenovacaoLicencas()

        # Adicionando ao stack
        self.stack.addWidget(self.tela_principal)  # índice 0
        self.stack.addWidget(self.tela_cadastro)   # índice 1
        self.stack.addWidget(self.tela_licencas)   # índice 2
        self.stack.addWidget(self.tela_tags)       # índice 3
        self.stack.addWidget(self.tela_licencas_empresas) # Indice 4
        self.stack.addWidget(self.tela_alertas)    # Indice 5
        self.stack.addWidget(self.tela_relatorios) # Indice 6
        

        self.setCentralWidget(self.stack)

        # Carrega o banco de dados na interface
        self.tela_principal.carregar_dados()

        # Menu lateral
        self.menu_lateral = QDockWidget("Menu", self)
        self.lista_menu = QListWidget()
        self.lista_menu.addItems([
            "Menu Principal", "Cadastro de Empresas", 
            "Licenças", "TAGS", "Licenças Empresas", "Relatórios", "Alertas"
        ])
        self.lista_menu.setStyleSheet("padding: 10px; font-size: 14px;")
        self.menu_lateral.setFixedWidth(180)
        self.menu_lateral.setWidget(self.lista_menu)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.menu_lateral)

        self.lista_menu.itemClicked.connect(self.mudar_tela)

    def mudar_tela(self, item):
        mapa = {
            "Menu Principal": 0,
            "Cadastro de Empresas": 1,
            "Licenças": 2,
            "TAGS": 3,
            "Licenças Empresas" : 4,
            "Alertas" : 5,
            "Relatórios" : 6
        }
        index = mapa.get(item.text(), 0)
        self.stack.setCurrentIndex(index)

        if item.text() == "Menu Principal":
            self.tela_principal.carregar_dados()

        elif item.text() == "Cadastro de Empresas":
            self.tela_cadastro.carregar_tags()
            
        elif item.text() == "TAGS":
            self.tela_tags.carregar_tags()