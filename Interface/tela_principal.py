from PySide6.QtWidgets import (
    QMessageBox, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, QHeaderView,
    QTableWidgetItem, QAbstractItemView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from banco.banco import Session, TabelaEmpresa, RelacaoEmpresaLicenca
from Interface.estilos import ESTILO_BOTAO, ESTILO_INPUT, ESTILO_TABELA, formatar_cnpj


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
        self.botao_editar = QPushButton("Editar") # Botão para Edição de informações
        self.botao_salvar = QPushButton("Salvar") # Botão para Salvar edições feitas
        self.botao_salvar.setEnabled(False)

        self.botao_pesquisar.clicked.connect(self.pesquisar_empresa)
        self.botao_adicionar.clicked.connect(self.ir_para_cadastro)
        self.botao_excluir.clicked.connect(self.excluir_empresa_selecionada)
        self.botao_editar.clicked.connect(self.habilitar_edicao) 
        self.botao_salvar.clicked.connect(self.salvar_alteracoes)

        for botao in [self.botao_pesquisar, self.botao_adicionar, self.botao_excluir, self.botao_editar, self.botao_salvar]:
            botao.setFixedHeight(30)
            botao.setStyleSheet(ESTILO_BOTAO)
            barra_layout.addWidget(botao)

        layout.addLayout(barra_layout)

        self.tabela = QTableWidget(0, 7)
        self.tabela.setHorizontalHeaderLabels(["ID", "Código", "CNPJ", "Empresa", "Município", "TAG", "E-mail"])
        self.tabela.setStyleSheet(ESTILO_TABELA)
        self.tabela.setStyleSheet("font-size: 13px;")
        self.tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Por padrão bloqueia edição

        self.tabela.setStyleSheet("""
            QTableWidget::item:hover {
                background-color: #f0f0f0;
            }
        """)

        self.tabela.setColumnWidth(0, 50)   # ID
        self.tabela.setColumnWidth(1, 100)  # Código
        self.tabela.setColumnWidth(2, 150)  # CNPJ
        self.tabela.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch) # Nome
        self.tabela.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch) # Municipio
        self.tabela.setColumnWidth(5, 150)  # TAG
        self.tabela.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)  # E-mail
        self.tabela.setAlternatingRowColors(True)
        
        layout.addWidget(self.tabela)
        self.setLayout(layout)

    def habilitar_edicao(self): # Ativa o modo de edição
        self.tabela.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked)
        self.botao_salvar.setEnabled(True)

    def salvar_alteracoes(self): # Confirmação de alterações e mudanças no Banco de Dados
        resposta = QMessageBox.question(self, "Confirmar", "Deseja salvar as alterações feitas?", QMessageBox.Yes | QMessageBox.No)
        if resposta == QMessageBox.No:
            return
        
        try:
            with Session() as session:
                for row in range(self.tabela.rowCount()):
                    id_empresa = int(self.tabela.item(row, 0).text())
                    empresa = session.query(TabelaEmpresa).get(id_empresa)
                    if empresa:
                        empresa.codigo = self.tabela.item(row, 1).text()
                        empresa.cnpj = self.tabela.item(row, 2).text().replace(".", "").replace("-", "").replace("/", "")
                        empresa.nome_empresa = self.tabela.item(row, 3).text()
                        empresa.municipio = self.tabela.item(row, 4).text()
                        empresa.tag = self.tabela.item(row, 5).text()
                        empresa.email = self.tabela.item(row, 6).text()

                session.commit()
            QMessageBox.information(self, "Sucesso", "Alterações salvas com sucesso!")
            self.carregar_dados()

        except Exception as e:
            QMessageBox.critical(self, "Erro ao salvar", str(e))

        self.tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.botao_salvar.setEnabled(False)

    def exibir_dados(self, dados):
        colunas = ["ID", "Código", "CNPJ", "Empresa", "Município", "TAG", "E-mail"]
        self.tabela.setRowCount(len(dados))
        self.tabela.setColumnCount(len(colunas))
        self.tabela.setHorizontalHeaderLabels(colunas)

        colunas_centralizadas = {0, 1, 2, 4, 5}

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
                if j == 2: #CNPJ
                    valor = formatar_cnpj(valor)
                item = QTableWidgetItem(str(valor))
                if j in colunas_centralizadas:
                    item.setTextAlignment(Qt.AlignCenter)
                self.tabela.setItem(i, j, item)

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
                if not termo:
                    empresas = session.query(TabelaEmpresa).all()

                elif termo.isdigit() and len(termo) <= 4:
                    # Busca por código
                    empresas = session.query(TabelaEmpresa).filter(TabelaEmpresa.codigo == termo).all()

                elif termo.isdigit() and len(termo) >= 11:
                    # Remove pontuação se tiver e busca por CNPJ
                    cnpj_limpo = termo.zfill(14)
                    empresas = session.query(TabelaEmpresa).filter(TabelaEmpresa.cnpj.like(f"%{cnpj_limpo}%")).all()

                else:
                    # Busca por nome (case insensitive)
                    empresas = session.query(TabelaEmpresa).filter(TabelaEmpresa.nome_empresa.ilike(f"%{termo}%")).all()

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