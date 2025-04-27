from PySide6.QtWidgets import (
    QApplication, QMainWindow, QDockWidget, QListWidget, 
    QTableWidget, QVBoxLayout, QHBoxLayout, QWidget, 
    QLineEdit, QPushButton, QStackedWidget, QHeaderView, QTextEdit, QLabel, QComboBox
)
from PySide6.QtCore import Qt

# PEP8
# Arrumar
# <UML> para banco de Dados


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Esqueleto da Tabela de Controle")
        self.setGeometry(100, 100, 800, 600)
        self.showMaximized() # Para aparecer de forma Maximizada, mas com bordas de minimizar, fechar etc
        
        # Criar o Gerenciados das telas
        self.stack = QStackedWidget()

        # Criar as Telas
        self.tela_principal = TelaPrincipal()
        self.tela_cadastro = TelaCadastro()
        self.tela_licencas = TelaLicencas()

        # Adicionando telas ao Stack
        self.stack.addWidget(self.tela_principal) # Indice 0
        self.stack.addWidget(self.tela_cadastro) # Indice 1
        self.stack.addWidget(self.tela_licencas)  # Indice 2

        # Definindo a tela principal como Inicial
        self.setCentralWidget(self.stack)

        # Criando um menu lateral
        self.menu_lateral = QDockWidget("Menu", self)
        self.lista_menu = QListWidget()
        self.lista_menu.addItems(["Menu Principal", "Cadastro de Empresas", "Licenças", "TAGS", "Relatórios", "Alertas"])
        self.menu_lateral.setFixedWidth(150) # Largura do menu

        self.menu_lateral.setWidget(self.lista_menu)

        # Adicionando o menu lateral na esquerda
        self.addDockWidget(Qt.LeftDockWidgetArea, self.menu_lateral)

        # Conectar cliques do menu à troca de telas
        self.lista_menu.itemClicked.connect(self.mudar_tela)


        
    # Controle para mudar as Telas
    def mudar_tela(self, item):
        if item.text() == "Menu Principal":
            self.stack.setCurrentIndex(0)
        elif item.text() == "Cadastro de Empresas":
            self.stack.setCurrentIndex(1)
        elif item.text() == "Licenças":
            self.stack.setCurrentIndex(2)

# -------------------------------------------- Telas Individuais --------------------------------------------

class TelaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        # Criando um layout vertical principal
        layout = QVBoxLayout()

        # Criando o layout horizontal para os elementos acima da tabela
        barra_layout = QHBoxLayout()

        # Criando o texto "Consultar Empresa"
        self.texto_consultar = QTextEdit("Consultar Empresa")
        self.texto_consultar.setReadOnly(True)  # Impede a edição
        self.texto_consultar.setFixedHeight(30)  # Ajustando a altura
        barra_layout.addWidget(self.texto_consultar)

        # Criando a barra de pesquisa (input)
        self.barra_pesquisa = QLineEdit()
        self.barra_pesquisa.setPlaceholderText("Digite o CNPJ da empresa")
        barra_layout.addWidget(self.barra_pesquisa)

        # Criando o botões
        self.botao_pesquisar = QPushButton("Pesquisar")
        barra_layout.addWidget(self.botao_pesquisar)

        self.botao_adicionar = QPushButton("Adicionar Empresa")
        barra_layout.addWidget(self.botao_adicionar)

        self.botao_excluir = QPushButton("Excluir Empresa")
        barra_layout.addWidget(self.botao_excluir)

        # Adicionando a barra de elementos ao layout principal
        layout.addLayout(barra_layout)

        # Criando a tabela
        self.tabela = QTableWidget(30, 6)  # 20 linhas e 6 colunas
        self.tabela.setHorizontalHeaderLabels(["Código", "CNPJ", "Nome Empresa", "Município", "TAG", "E-mail"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.tabela.setColumnWidth(0, 75)  # Código
        self.tabela.setColumnWidth(1, 130)  # CNPJ
        self.tabela.setColumnWidth(2, 400)  # Nome Empresa
        self.tabela.setColumnWidth(3, 200)  # Município
        self.tabela.setColumnWidth(4, 100)  # TAG

        layout.addWidget(self.tabela)  # Adicionando a tabela ao layout

        # Definir layout direto na Tela
        self.setLayout(layout)

        

class TelaCadastro(QWidget):
    def __init__(self):
        super().__init__()
        layout_principal = QVBoxLayout()
        layout_principal.setAlignment(Qt.AlignCenter)  # Centraliza o layout na tela

        # ------------------------ Linha 1 (Código - CNPJ - Nome Empresa) ------------------------
        linha1 = QHBoxLayout()

        coluna1 = QVBoxLayout()
        label_codigo = QLabel("Código:")
        self.input_codigo = QLineEdit()
        self.input_codigo.setFixedWidth(120)
        coluna1.addWidget(label_codigo)
        coluna1.addWidget(self.input_codigo)

        coluna2 = QVBoxLayout()
        label_cnpj = QLabel("CNPJ:")
        self.input_cnpj = QLineEdit()
        self.input_cnpj.setFixedWidth(180)
        coluna2.addWidget(label_cnpj)
        coluna2.addWidget(self.input_cnpj)

        coluna3 = QVBoxLayout()
        label_nome_empresa = QLabel("Nome Empresa:")
        self.input_nome_empresa = QLineEdit()
        self.input_nome_empresa.setFixedWidth(280)
        coluna3.addWidget(label_nome_empresa)
        coluna3.addWidget(self.input_nome_empresa)

        linha1.addLayout(coluna1)
        linha1.addLayout(coluna2)
        linha1.addLayout(coluna3)

        # ------------------------ Linha 2 (Município - TAG - E-mail) ------------------------
        linha2 = QHBoxLayout()

        coluna4 = QVBoxLayout()
        label_municipio = QLabel("Município:")
        self.input_municipio = QLineEdit()
        self.input_municipio.setFixedWidth(200)
        coluna4.addWidget(label_municipio)
        coluna4.addWidget(self.input_municipio)

        coluna5 = QVBoxLayout()
        label_tag = QLabel("TAG:")
        self.input_tag = QLineEdit()
        self.input_tag.setFixedWidth(120)
        coluna5.addWidget(label_tag)
        coluna5.addWidget(self.input_tag)

        coluna6 = QVBoxLayout()
        label_email = QLabel("E-mail:")
        self.input_email = QLineEdit()
        self.input_email.setFixedWidth(280)
        coluna6.addWidget(label_email)
        coluna6.addWidget(self.input_email)

        linha2.addLayout(coluna4)
        linha2.addLayout(coluna5)
        linha2.addLayout(coluna6)

        # ------------------------ Botão Cadastrar ------------------------
        botao_layout = QHBoxLayout()
        botao_layout.setAlignment(Qt.AlignCenter)  # Centralizar o botão
        self.btn_cadastrar = QPushButton("Cadastrar")
        self.btn_cadastrar.setFixedSize(200, 40)  # Botão maior para destaque
        botao_layout.addWidget(self.btn_cadastrar)

        # ------------------------ Adicionar elementos ao Layout Principal ------------------------
        layout_principal.addLayout(linha1)
        layout_principal.addSpacing(10)  # Espaço entre as linhas
        layout_principal.addLayout(linha2)
        layout_principal.addSpacing(20)  # Espaço antes do botão
        layout_principal.addLayout(botao_layout)

        # Definir layout final
        self.setLayout(layout_principal) # Juntando todo o layout

# -------------------------------------------- Tela Licenças --------------------------------------------

class TelaLicencas(QWidget):
    def __init__(self):
        super().__init__()

        # Layout Principal
        layout_horizontal = QHBoxLayout()

        # ---------------------- Menu de Botões (lado esquerdo) ----------------------

        menu_botoes = QVBoxLayout()
        
        self.botao_adicionar = QPushButton("Adicionar Licença")
        self.botao_adicionar.setFixedSize(150, 50)

        self.botao_excluir = QPushButton("Excluir Licença")
        self.botao_excluir.setFixedSize(150, 50)

        menu_botoes.addStretch()
        menu_botoes.addWidget(self.botao_adicionar, alignment=Qt.AlignCenter)
        menu_botoes.addSpacing(10)
        menu_botoes.addWidget(self.botao_excluir, alignment=Qt.AlignCenter)
        menu_botoes.addStretch()

        menu_botoes.addWidget(self.botao_adicionar)
        menu_botoes.addWidget(self.botao_excluir)

        layout_horizontal.addLayout(menu_botoes)

        # ---------------------- Área da Tabela + Filtros ----------------------

        area_tabela_layout = QVBoxLayout()

        # Layout dos filtros
        filtros_layout = QHBoxLayout()

        self.input_pesquisa = QLineEdit()
        self.input_pesquisa.setPlaceholderText("Digite o Nome da Licença")

        self.dropdown_filtro = QComboBox()
        self.dropdown_filtro.addItems(["Todas", "Anual", "Semestral", "Trimestral", "Mensal"]) # Tipos de Periodicidade
        
        filtros_layout.addWidget(QLabel("Pesquisar Licença:"))
        filtros_layout.addWidget(self.input_pesquisa)
        filtros_layout.addWidget(QLabel("Filtro:"))
        filtros_layout.addWidget(self.dropdown_filtro)


        area_tabela_layout.addLayout(filtros_layout)

        # Tabela de Licenças
        self.tabela_licencas = QTableWidget(10, 5)
        self.tabela_licencas.setHorizontalHeaderLabels(["ID", "Nome", "Data Base", "Periodicidade", "Antecipação"])

        self.tabela_licencas.setColumnWidth(0, 50)    # ID
        self.tabela_licencas.setColumnWidth(1, 250)   # Nome
        self.tabela_licencas.setColumnHidden(2, True) # Oculta a coluna "Data Base"
        self.tabela_licencas.setColumnWidth(3, 120)   # Periodicidade
        self.tabela_licencas.setColumnWidth(4, 120)   # Antecipação

        self.tabela_licencas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        area_tabela_layout.addWidget(self.tabela_licencas)

        # Adiciona a parte da tabela ao layout principal
        layout_horizontal.addLayout(area_tabela_layout)

        self.setLayout(layout_horizontal)

app = QApplication([])
janela = MainWindow()
janela.show()
app.exec()