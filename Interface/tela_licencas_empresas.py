from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QComboBox, 
    QMessageBox, QTableWidget, QTableWidgetItem, 
    QDateEdit, QCompleter
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont
from banco.banco import Session, TabelaEmpresa, RelacaoEmpresaLicenca
from Interface.estilos import ESTILO_BOTAO, ESTILO_DATEEDIT, ESTILO_LABEL

class TelaRenovacaoLicencas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Renovação de Licenças")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        titulo = QLabel("Renovação de Licenças")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        self.layout.addWidget(titulo)

        # ComboBox para selecionar empresa
        empresa_layout = QHBoxLayout()
        empresa_label = QLabel("Selecione a Empresa:")
        empresa_label.setStyleSheet(ESTILO_LABEL)
        self.combo_empresa = QComboBox()
        empresa_layout.addWidget(empresa_label)
        empresa_layout.addWidget(self.combo_empresa)
        self.layout.addLayout(empresa_layout)

        self.combo_empresa.currentIndexChanged.connect(self.carregar_licencas_empresa)

        # Tabela de licenças
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(4)
        self.tabela.setHorizontalHeaderLabels(["Licença", "Data Base", "Periodicidade", "Status"])
        self.layout.addWidget(self.tabela)

        # Botão para salvar alterações
        self.botao_salvar = QPushButton("Atualizar Datas")
        self.botao_salvar.setStyleSheet(ESTILO_BOTAO)
        self.botao_salvar.clicked.connect(self.atualizar_datas)
        self.layout.addWidget(self.botao_salvar, alignment=Qt.AlignRight)

        self.carregar_empresas()

    def carregar_empresas(self):
        try:
            with Session() as session:
                empresas = session.query(TabelaEmpresa).all()
                self.combo_empresa.clear()
                nomes_empresas = [empresa.nome_empresa for empresa in empresas]
                self.combo_empresa.addItems(nomes_empresas)
                self.combo_empresa.setEditable(True)  # Permite digitar

                # Configura o completer para filtrar conforme digita
                completer = QCompleter(nomes_empresas, self.combo_empresa)
                completer.setCaseSensitivity(Qt.CaseInsensitive)
                completer.setFilterMode(Qt.MatchContains)  # Permite buscar em qualquer parte do nome
                self.combo_empresa.setCompleter(completer)

                # Guarda o mapping nome -> id para uso posterior
                self.empresa_map = {empresa.nome_empresa: empresa.id for empresa in empresas}

        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))

    def carregar_licencas_empresa(self):
        """Carrega licenças da empresa selecionada na tabela"""
        empresa_nome = self.combo_empresa.currentText()
        empresa_id = self.empresa_map.get(empresa_nome)
        if not empresa_nome or empresa_id is None:
            return

        with Session() as session:
            relacoes = session.query(RelacaoEmpresaLicenca).filter_by(cnpj=session.query(TabelaEmpresa.cnpj).filter_by(id=empresa_id).scalar()).all()
        
        self.tabela.setRowCount(len(relacoes))

        for i, rel in enumerate(relacoes):
            # Coluna Licença
            self.tabela.setItem(i, 0, QTableWidgetItem(rel.nome_licenca))
            
            # Coluna Data Base (editable)
            date_edit = QDateEdit()
            date_edit.setCalendarPopup(True)
            date_edit.setDate(QDate(rel.data_base.year, rel.data_base.month, rel.data_base.day))
            date_edit.setStyleSheet(ESTILO_DATEEDIT)
            self.tabela.setCellWidget(i, 1, date_edit)
            
            # Coluna Periodicidade
            self.tabela.setItem(i, 2, QTableWidgetItem(rel.periodicidade))
            
            # Coluna Status
            status = self.calcular_status(rel)
            self.tabela.setItem(i, 3, QTableWidgetItem(status))

    def calcular_status(self, rel):
        """Calcula se a licença está vencida ou a vencer"""
        from datetime import date, timedelta
        MAPEAMENTO_PERIODICIDADE = {
            "mensal": 30,
            "bimestral": 60,
            "trimestral": 90,
            "semestral": 180,
            "anual": 365
        }
        dias = MAPEAMENTO_PERIODICIDADE.get(rel.periodicidade.lower(), 0)
        data_venc = rel.data_base + timedelta(days=dias)
        dias_restantes = (data_venc - date.today()).days
        if dias_restantes < 0:
            return "VENCIDA"
        else:
            return "A VENCER"

    def atualizar_datas(self):
        empresa_nome = self.combo_empresa.currentText()
        empresa_id = self.empresa_map.get(empresa_nome)
        if not empresa_nome or empresa_id is None:
            return
        try:
            with Session() as session:
                empresa_cnpj = session.query(TabelaEmpresa.cnpj).filter_by(id=empresa_id).scalar()
                relacoes = session.query(RelacaoEmpresaLicenca).filter_by(cnpj=empresa_cnpj).all()

                for i, rel in enumerate(relacoes):
                    date_edit = self.tabela.cellWidget(i, 1)
                    nova_data = date_edit.date().toPython()
                    rel.data_base = nova_data

                session.commit()
                QMessageBox.information(self, "Sucesso", "Datas de licenças atualizadas com sucesso!")
                self.carregar_licencas_empresa()

        except Exception as e:
            QMessageBox.critical(self, "Erro", str(e))