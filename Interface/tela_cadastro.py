from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, 
    QFormLayout, QLineEdit, QComboBox, 
    QPushButton, QMessageBox, QDialog, 
    QDialogButtonBox, QDateEdit, QHBoxLayout
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont
from banco.banco import criar_conexao
from Interface.estilos import ESTILO_BOTAO, ESTILO_COMBOBOX, ESTILO_DATEEDIT, ESTILO_INPUT, ESTILO_LABEL
from datetime import datetime

class TelaCadastroEmpresa(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        titulo = QLabel("Cadastro de Empresa")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(titulo)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignLeft)

        self.input_codigo = QLineEdit()
        self.input_cnpj = QLineEdit()
        self.input_nome = QLineEdit()
        self.input_municipio = QLineEdit()
        self.input_email = QLineEdit()
        self.input_tag = QComboBox()
        self.input_tag.setStyleSheet(ESTILO_COMBOBOX)

        for label, input_widget in [
            ("Código:", self.input_codigo),
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
        self.botao_salvar.clicked.connect(self.salvar_empresa)
        layout.addWidget(self.botao_salvar, alignment=Qt.AlignRight)

        self.setLayout(layout)
        self.carregar_tags()


    """Seleciona todas as Tags dentro do DB e os adiciona no Combo Box do input TAG"""
    def carregar_tags(self):
        try:
            with criar_conexao() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT nome_tag FROM tabela_tags")
                tags = cursor.fetchall()
                self.input_tag.clear()
                self.input_tag.addItems([tag[0] for tag in tags])
        
        except Exception as e:
            QMessageBox.critical(self, "Erro ao carregar TAGs", str(e))


    
    def salvar_empresa(self):
        codigo = self.input_codigo.text().strip()
        cnpj = self.input_cnpj.text().strip()
        nome = self.input_nome.text().strip()
        municipio = self.input_municipio.text().strip()
        email = self.input_email.text().strip()
        tag = self.input_tag.currentText().strip()

        if not all([codigo, cnpj, nome, municipio, email, tag]):
            QMessageBox.warning(self, "Campos obrigatórios", "Preencha todos os campos.")
            return

        try:
            with criar_conexao() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tabela_empresas WHERE cnpj = ? OR codigo = ?", (cnpj, codigo))
                
                if cursor.fetchone():
                    QMessageBox.warning(self, "Duplicidade", "CNPJ ou Código já cadastrado.")
                    return
                
                cursor.execute("""
                    INSERT INTO tabela_empresas (codigo, cnpj, nome_empresa, municipio, tag, email)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (codigo, cnpj, nome, municipio, tag, email))

                cursor.execute("""
                    SELECT l.id, l.nome_licenca, l.periodicidade, l.antecipacao
                    FROM tabela_tags t
                    JOIN tabela_licencas l ON t.id_licenca = l.id
                    WHERE t.nome_tag = ?
                """, (tag,))
                licencas = cursor.fetchall()

                datas = self.abrir_dialogo_datas(licencas)
                if datas is None:
                    return # Caso o Usuario cancelar a ação
                
                for i, licenca in enumerate(licencas):
                    _, nome_licenca, periodicidade, antecipacao = licenca

                    data_base = datas[i].toString("yyyy-MM-dd")
                    cursor.execute("""
                        INSERT INTO relacao_empresa_licenca (cnpj, nome_licenca, data_base, periodicidade, antecipacao)
                        VALUES (?, ?, ?, ?, ?)
                    """, (cnpj, nome_licenca, data_base, periodicidade, antecipacao))
                conn.commit()

                QMessageBox.information(self, "Sucesso", f"Empresa '{nome}' cadastrada com sucesso!")

        except Exception as e:
            QMessageBox.critical(self, "Erro ao salvar", str(e))
    

    """Uma espécie de Tela Separada para digitar as Datas Bases das licenças adicionadas da TAG selecionada"""
    def abrir_dialogo_datas(self, licencas):
        dialogo = QDialog(self)
        dialogo.setWindowTitle("Informe as Datas Base das Licenças")
        layout = QVBoxLayout()
        campos_data = []

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        for _, nome_licenca, _, _ in licencas:
            linha = QHBoxLayout()
            label = QLabel(nome_licenca)
            data_edit = QDateEdit()
            data_edit.setStyleSheet(ESTILO_DATEEDIT)
            data_edit.setCalendarPopup(True)
            data_edit.setDate(QDate.currentDate())
            linha.addWidget(label)
            linha.addWidget(data_edit)
            layout.addLayout(linha)
            campos_data.append(data_edit)

        botoes = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        botoes.accepted.connect(dialogo.accept)
        botoes.rejected.connect(dialogo.reject)
        layout.addWidget(botoes)

        dialogo.setLayout(layout)
        dialogo.setFont(QFont("Segoe UI", 12))

        if dialogo.exec():
            return [campo.date() for campo in campos_data]  # Retorna as datas, não os widgets
        
        return None