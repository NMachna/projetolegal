from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTableWidget, 
    QHeaderView, QComboBox,QTableWidgetItem,
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, 
    QSpinBox, QDialogButtonBox, QMessageBox
)
from PySide6.QtGui import QFont
from banco.banco import criar_conexao
from Interface.estilos import ESTILO_BOTAO, ESTILO_INPUT, ESTILO_LABEL


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
        self.carregar_licencas()
        self.botao_adicionar_licenca.clicked.connect(self.abrir_dialogo_adicionar_licenca)
        self.botao_excluir_licenca.clicked.connect(self.excluir_licenca_selecionada)

    def carregar_licencas(self):
        self.tabela_licencas.setRowCount(0)

        try:
            with criar_conexao() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT nome_licenca, periodicidade, antecipacao
                    FROM tabela_licencas
                """)
                licencas = cursor.fetchall()

                for row_index, (nome, periodicidade, antecipacao) in enumerate(licencas):
                    self.tabela_licencas.insertRow(row_index)
                    self.tabela_licencas.setItem(row_index, 0, QTableWidgetItem(nome))
                    self.tabela_licencas.setItem(row_index, 1, QTableWidgetItem(periodicidade.capitalize()))
                    self.tabela_licencas.setItem(row_index, 2, QTableWidgetItem(str(antecipacao)))

        except Exception as e:
            QMessageBox.critical(self, "Erro ao carregar", str(e))

    def abrir_dialogo_adicionar_licenca(self):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Adicionar Nova Licença")

        layout = QVBoxLayout()
        form = QFormLayout()

        input_nome = QLineEdit()
        input_periodicidade = QComboBox()
        input_periodicidade.addItems(["anual", "semestral", "mensal"])

        input_antecipacao = QSpinBox()
        input_antecipacao.setMinimum(1)
        input_antecipacao.setMaximum(365)
        input_antecipacao.setValue(30)

        form.addRow("Nome da Licença:", input_nome)
        form.addRow("Periodicidade:", input_periodicidade)
        form.addRow("Dias de Antecipação:", input_antecipacao)

        layout.addLayout(form)

        botoes = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botoes.accepted.connect(dialogo.accept)
        botoes.rejected.connect(dialogo.reject)
        layout.addWidget(botoes)

        dialogo.setLayout(layout)

        if dialogo.exec():
            nome = input_nome.text().strip()
            periodicidade = input_periodicidade.currentText()
            antecipacao = input_antecipacao.value()

            if not nome:
                QMessageBox.warning(self, "Campo obrigatório", "O nome da licença é obrigatório.")
                return

            try:
                with criar_conexao() as conexao:
                    cursor = conexao.cursor()
                    cursor.execute("INSERT INTO tabela_licencas (nome_licenca, periodicidade, antecipacao) VALUES (?, ?, ?)",
                                (nome, periodicidade, antecipacao))
                    conexao.commit()
                    QMessageBox.information(self, "Sucesso", "Licença cadastrada com sucesso!")
                    self.carregar_licencas()
            except Exception as e:
                QMessageBox.critical(self, "Erro", str(e))

    def excluir_licenca_selecionada(self):
        linha_selecionada = self.tabela_licencas.currentRow()
        if linha_selecionada == -1:
            QMessageBox.warning(self, "Nenhuma seleção", "Selecione uma licença para exclusão")
            return
        
        nome_licenca = self.tabela_licencas.item(linha_selecionada, 0).text()

        # Confirmação Usuario
        resposta = QMessageBox.question(
            self, "Confirmar Exclusão",
            f"Tem certeza que deseja excluir a licença '{nome_licenca}'?",
            QMessageBox.Yes | QMessageBox.No
        )
         
        if resposta == QMessageBox.No:
            return
        
        try:
            with criar_conexao() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM relacao_empresa_licenca WHERE nome_licenca = ?", (nome_licenca,))
                associacoes = cursor.fetchone()[0]

                if associacoes > 0:
                    QMessageBox.warning(self, "Exclusão não permitida", "Essa licença está associada a uma ou mais empresas.")
                    return
                
                # Exclui a licença
                cursor.execute("""
                    DELETE FROM tabela_licencas 
                    WHERE nome_licenca = ?
                """, (nome_licenca,))
                conn.commit()

                QMessageBox.information(self, "Licença excluída", f"A licença '{nome_licenca}' foi excluída com sucesso.")
                self.carregar_licencas()

        except Exception as e:
            QMessageBox.critical(self, "Erro ao excluir", str(e))