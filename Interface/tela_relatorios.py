from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QDialog, QPushButton, QAbstractScrollArea, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from banco.banco import Session, TabelaEmpresa, TabelaEnvioEmail

class TelaRelatorios(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Relatórios de Envio de E-mails")
        self.resize(800, 500)

        layout = QVBoxLayout(self)

        self.tabela_empresas = QTableWidget()
        self.tabela_empresas.setColumnCount(4)
        self.tabela_empresas.setHorizontalHeaderLabels(["Código", "Empresa", "Município", "E-mail"])
        self.tabela_empresas.cellDoubleClicked.connect(self.abrir_detalhes_empresa)
        layout.addWidget(self.tabela_empresas)

        self.setLayout(layout)
        self.carregar_empresas()

    def carregar_empresas(self):
        """Carrega todas as empresas na tabela"""
        try:
            with Session() as session:
                empresas = session.query(TabelaEmpresa).all()
                self.tabela_empresas.setRowCount(len(empresas))

                for i, emp in enumerate(empresas):
                    self.tabela_empresas.setItem(i, 0, QTableWidgetItem(emp.codigo or ""))
                    self.tabela_empresas.setItem(i, 1, QTableWidgetItem(emp.nome_empresa or ""))
                    self.tabela_empresas.setItem(i, 2, QTableWidgetItem(emp.municipio or ""))
                    self.tabela_empresas.setItem(i, 3, QTableWidgetItem(emp.email or ""))

        except Exception as e:
            QMessageBox.critical(self, "Erro ao carregar empresas", str(e))

    def abrir_detalhes_empresa(self, row):
        """Mostra histórico de envios para a empresa clicada"""
        nome_empresa = self.tabela_empresas.item(row, 1).text()  # coluna do nome

        with Session() as session:
            empresa = session.query(TabelaEmpresa).filter_by(nome_empresa=nome_empresa).first()
            if not empresa:
                QMessageBox.warning(self, "Aviso", "Empresa não encontrada.")
                return

            envios = session.query(TabelaEnvioEmail)\
                            .filter_by(empresa_id=empresa.id)\
                            .order_by(TabelaEnvioEmail.data_envio.desc())\
                            .all()

        dialogo = QDialog(self)
        dialogo.setWindowTitle(f"Histórico de envios - {nome_empresa}")

        layout = QVBoxLayout(dialogo)
        tabela = QTableWidget()
        tabela.setColumnCount(3)
        tabela.setHorizontalHeaderLabels(["Data Envio", "E-mail Destino", "Licenças Enviadas"])
        tabela.setRowCount(len(envios))

        for i, envio in enumerate(envios):
            tabela.setItem(i, 0, QTableWidgetItem(envio.data_envio.strftime("%d/%m/%Y %H:%M")))
            tabela.setItem(i, 1, QTableWidgetItem(envio.email_destino))
            tabela.setItem(i, 2, QTableWidgetItem(envio.licencas_enviadas))

        tabela.resizeColumnsToContents()
        tabela.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        layout.addWidget(tabela)

        botao_fechar = QPushButton("Fechar")
        botao_fechar.clicked.connect(dialogo.close)
        layout.addWidget(botao_fechar, alignment=Qt.AlignRight)

        dialogo.resize(800, 400)
        dialogo.exec()