from PySide6.QtWidgets import QWidget, QVBoxLayout, QHeaderView, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
from envios_email.vencimento import disparar_alertas, obter_licencas_proximas_vencimento

class TelaAlertas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alertas de Licenças")
        self.resize(800, 500)

        layout = QVBoxLayout(self)

        # Tabela para mostrar licenças a vencer
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(3)
        self.tabela.setHorizontalHeaderLabels(["Empresa", "Licença", "Data de Vencimento"])
        
        # Ajuste automático para ocupar o espaço disponível
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.tabela)

        # Botão para disparar e-mails
        self.botao_disparar = QPushButton("Disparar alertas por e-mail")
        self.botao_disparar.clicked.connect(self.enviar_alertas)
        layout.addWidget(self.botao_disparar)

        # Carregar dados ao abrir
        self.carregar_dados()

    def carregar_dados(self):
        """Carrega as licenças próximas ao vencimento na tabela"""
        licencas = obter_licencas_proximas_vencimento()
        total_linhas = sum(len(emp["licencas"]) for emp in licencas)
        self.tabela.setRowCount(total_linhas)

        linha = 0
        for empresa in licencas:
            for licenca in empresa["licencas"]:
                self.tabela.setItem(linha, 0, QTableWidgetItem(empresa["empresa"]))
                self.tabela.setItem(linha, 1, QTableWidgetItem(licenca["nome"]))
                self.tabela.setItem(linha, 2, QTableWidgetItem(licenca["vencimento"]))
                linha += 1

    def enviar_alertas(self):
        enviados = disparar_alertas()
        QMessageBox.information(
            self, "Envio Concluído", f"{enviados} e-mails enviados com sucesso."
        )
        # Atualizar tabela depois do envio
        self.carregar_dados()