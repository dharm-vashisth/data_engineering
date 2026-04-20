import sys
from PySide6.QtWidgets import QApplication

from db.database import init_db
from ui.main_window import App
from ui.styles import APP_STYLE

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)
    init_db()
    window = App()
    window.show()
    sys.exit(app.exec())
