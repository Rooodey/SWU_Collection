import sys, os
from PyQt6.QtWidgets import QApplication
from SWU_Collection.models import init_db
from SWU_Collection.ui import DatabaseApp


init_db()

app = QApplication(sys.argv)
window = DatabaseApp()
window.show()
sys.exit(app.exec())
