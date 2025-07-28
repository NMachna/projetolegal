
ESTILO_BOTAO = """
    QPushButton {
        background-color: #3498db;
        color: white;
        border-radius: 4px;
        padding: 6px 12px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #2980b9;
    }
"""

ESTILO_INPUT = "QLineEdit { padding: 6px; font-size: 14px; }"
ESTILO_LABEL = "QLabel { font-size: 14px; }"

ESTILO_TABELA = """
    QTableWidget {
        font-size: 13px;
        alternate-background-color: #f5f5f5;
        background-color: white;
        gridline-color: #dcdcdc;
    }
    QHeaderView::section {
        background-color: #3498db;
        color: white;
        padding: 4px;
        border: 1px solid #ddd;
        font-weight: bold;
    }
    QTableWidget::item {
        padding: 4px;
    }
"""
ESTILO_COMBOBOX = """
    QComboBox {
        padding: 4px;
        font-size: 14px;
    }
"""

ESTILO_DATEEDIT = """
    QDateEdit {
        padding: 4px;
        font-size: 14px;
    }
"""

def formatar_cnpj(cnpj: str) -> str:
    if len(cnpj) != 14:
        return cnpj
    
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"