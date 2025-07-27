from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, 
    QTableWidget, QHeaderView, QTableWidgetItem, 
    QDialog, QAbstractScrollArea, QLineEdit,
    QMessageBox, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from sqlalchemy.orm import joinedload

from tags.funcoes_tags import obter_tags
from banco.banco import Session, TabelaTags, TabelaLicencas
from Interface.estilos import ESTILO_BOTAO, ESTILO_TABELA, ESTILO_INPUT, ESTILO_COMBOBOX


class TelaTags(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        titulo = QLabel("TAGS")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(titulo)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.tabela_tags = QTableWidget(0, 1)  # Apenas 1 coluna agora
        self.tabela_tags.setHorizontalHeaderLabels(["Nome TAG"])
        self.tabela_tags.setStyleSheet(ESTILO_TABELA)
        self.tabela_tags.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela_tags.setStyleSheet("font-size: 13px;")
        layout.addWidget(self.tabela_tags)

        self.botao_adicionar_tag = QPushButton("Adicionar TAG")
        self.botao_adicionar_tag.setStyleSheet(ESTILO_BOTAO)
        self.botao_adicionar_tag.clicked.connect(self.abrir_dialogo_cadastro_tag)
        layout.addWidget(self.botao_adicionar_tag, alignment=Qt.AlignRight)

        self.carregar_tags()
        self.setLayout(layout)
        self.tabela_tags.cellDoubleClicked.connect(self.abrir_detalhes_tags)
    
    def carregar_tags(self):
        try:
            self.tags = obter_tags()
            self.tabela_tags.setRowCount(len(self.tags))
            self.tabela_tags.setColumnCount(1)  # Garante pelo menos 1 coluna
            self.tabela_tags.setHorizontalHeaderLabels(["TAG"])

            for i, (nome_tag, _) in enumerate(self.tags):
                item = QTableWidgetItem(nome_tag)
                self.tabela_tags.setItem(i, 0, item)
        except Exception as e:
            QMessageBox.critical(self, "Erro ao carregar TAGs", str(e))

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

    def abrir_dialogo_cadastro_tag(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Cadastrar Nova TAG")

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        label_nome = QLabel("Nome da TAG:")
        input_nome = QLineEdit()
        input_nome.setStyleSheet(ESTILO_INPUT)
        layout.addWidget(label_nome)
        layout.addWidget(input_nome)

        dropdowns = []

        try:
            with Session() as session:
                todas_licencas = session.query(TabelaLicencas.id, TabelaLicencas.nome_licenca).all()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao buscar licenças: {e}")
            return
        
        def adicionar_dropdown():
            licencas_restantes = []
            licencas_selecionadas = []
            
            for dropdown in dropdowns:
                valor = dropdown.currentData()
                if valor:
                    licencas_selecionadas.append(valor)

                    if not licencas_restantes:
                        return
                    
            for id_, nome in todas_licencas:
                if id_ not in licencas_selecionadas:
                    licencas_restantes.append((id_, nome))

            combo = QComboBox()
            combo.setStyleSheet(ESTILO_COMBOBOX)

            for id_, nome in licencas_restantes:
                combo.addItem(nome, id_)
            
            layout.insertWidget(layout.count() - 2, combo)
            dropdowns.append(combo)

            # Botão para adicionar outro campo de licença
        botao_add = QPushButton("Adicionar Licença")
        botao_add.setStyleSheet(ESTILO_BOTAO)
        botao_add.clicked.connect(adicionar_dropdown)
        
        botao_salvar = QPushButton("Salvar")
        botao_salvar.setStyleSheet(ESTILO_BOTAO)

        def salvar():
            nome_tag = input_nome.text().strip()
            if not nome_tag:
                QMessageBox.warning(dialogo, "Erro", "O nome da TAG não pode estar vazio.")
                return
            
            licencas_ids = []
            for combo in dropdowns:
                valor = combo.currentData()
                if valor:
                    licencas_ids.append(valor)
            
            if not licencas_ids:
                QMessageBox.warning(dialogo, "Erro", "Selecione ao menos uma licença.")
                return
            
            try:
                with Session() as session:
                    # Verifica duplicidade
                    existe = session.query(TabelaTags).filter_by(nome_tag=nome_tag).first()
                    if existe:
                        QMessageBox.warning(dialogo, "TAG duplicada", "Essa TAG já existe.")
                        return

                    for id_licenca in licencas_ids:
                        nova_tag = TabelaTags(nome_tag=nome_tag, id_licenca=id_licenca)
                        session.add(nova_tag)

                    session.commit()
                    QMessageBox.information(dialogo, "Sucesso", f"TAG '{nome_tag}' cadastrada com sucesso!")
                    dialogo.accept()
                    self.carregar_tags()

            except Exception as e:
                QMessageBox.critical(dialogo, "Erro", f"Erro ao salvar: {e}")

        botao_salvar.clicked.connect(salvar)
        layout.addWidget(botao_add)
        layout.addWidget(botao_salvar)
        dialogo.setLayout(layout)
        adicionar_dropdown()
        dialogo.exec()