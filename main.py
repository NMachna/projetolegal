from PySide6.QtWidgets import QApplication
from Interface.janela_principal import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    screen_geometry = app.primaryScreen().availableGeometry()
    window.setGeometry(screen_geometry)
    window.show()
    sys.exit(app.exec())