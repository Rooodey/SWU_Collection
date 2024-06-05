import sys, os
from PyQt6.QtWidgets import QApplication
from models import init_db
from ui import DatabaseApp


init_db()

app = QApplication(sys.argv)
window = DatabaseApp()
window.show()
sys.exit(app.exec())
