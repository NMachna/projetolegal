from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox
from envios_email.vencimento import disparar_alertas

class TelaAlertas(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alertas")

        layout = QVBoxLayout(self)

        self.botao_disparar = QPushButton("Disparar alertas por e-mail")
        self.botao_disparar.clicked.connect(self.enviar_alertas)

        layout.addWidget(self.botao_disparar)

    def enviar_alertas(self):
        enviados = disparar_alertas()
        QMessageBox.information(
            self, "Envio Concluído", f"{enviados} e-mails enviados com sucesso."
        )