import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QLineEdit, QPushButton, QLabel, QFormLayout
)
from db.database import init_db, get_connection
from view_data_window import ViewDataWindow


# ---------------- MAIN APP ----------------
class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Finance Tracker")
        self.setGeometry(200, 200, 400, 300)

        # Inputs
        self.amount = QLineEdit()
        self.amount.setPlaceholderText("Enter amount")

        self.category = QLineEdit()
        self.category.setPlaceholderText("Enter category")

        self.note = QLineEdit()
        self.note.setPlaceholderText("Enter note")

        # Buttons
        self.add_btn = QPushButton("Add Expense")
        self.add_btn.clicked.connect(self.save_data)

        self.view_btn = QPushButton("View Expenses")
        self.view_btn.clicked.connect(self.open_view_window)

        # Status
        self.status = QLabel("")

        # -------- Layout --------
        form_layout = QFormLayout()
        form_layout.addRow("Amount:", self.amount)
        form_layout.addRow("Category:", self.category)
        form_layout.addRow("Note:", self.note)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.view_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.status)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # -------- Styling --------
        self.setStyleSheet("""
        QMainWindow {
            background-color: #1e1e2f;
            color: white;
        }

        QLineEdit {
            padding: 8px;
            border-radius: 6px;
            border: 1px solid #444;
            background-color: #2b2b3c;
            color: white;
        }

        QPushButton {
            padding: 8px;
            border-radius: 6px;
            background-color: #4CAF50;
            color: white;
        }

        QPushButton:hover {
            background-color: #45a049;
        }

        QLabel {
            color: #ddd;
        }
        """)

    # -------- Logic --------
    def save_data(self):
        conn = get_connection()

        conn.execute(
            "INSERT INTO expenses (amount, category, note) VALUES (?, ?, ?)",
            (
                float(self.amount.text()),
                self.category.text(),
                self.note.text()
            )
        )

        conn.close()

        self.status.setText("Saved ✅")
        self.status.setStyleSheet("color: lightgreen;")

        self.amount.clear()
        self.category.clear()
        self.note.clear()

    def open_view_window(self):
        self.view_window = ViewDataWindow()
        self.view_window.show()


# ---------------- RUN APP ----------------
app = QApplication(sys.argv)

init_db()

window = App()
window.show()

sys.exit(app.exec())