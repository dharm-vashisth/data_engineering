import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout,
    QWidget, QLineEdit, QPushButton, QLabel
)
from db.database import init_db, get_connection
from view_data_window import ViewDataWindow


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Finance Tracker")
        self.setGeometry(200, 200, 400, 300)

        # Inputs
        self.amount = QLineEdit()
        self.amount.setPlaceholderText("Amount")

        self.category = QLineEdit()
        self.category.setPlaceholderText("Category")

        self.note = QLineEdit()
        self.note.setPlaceholderText("Note")

        # Button
        self.button = QPushButton("Add Expense")
        self.button.clicked.connect(self.save_data)

        self.view_button = QPushButton("View Expenses")
        self.view_button.clicked.connect(self.open_view_window)

        # Status
        self.status = QLabel("")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.amount)
        layout.addWidget(self.category)
        layout.addWidget(self.note)
        layout.addWidget(self.button)
        layout.addWidget(self.view_button)
        layout.addWidget(self.status)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def save_data(self):
        conn = get_connection()

        # Generate ID
        result = conn.execute(
            "SELECT COALESCE(MAX(id), 0) + 1 FROM expenses"
        ).fetchone()

        next_id = result[0]

        conn.execute(
            "INSERT INTO expenses VALUES (?, ?, ?, ?)",
            (
                next_id,
                float(self.amount.text()),
                self.category.text(),
                self.note.text()
            )
        )

        conn.close()

        self.status.setText("Saved ✅")

        # Clear inputs
        self.amount.clear()
        self.category.clear()
        self.note.clear()

    def open_view_window(self):
        self.view_window = ViewDataWindow()
        self.view_window.show()


# Run app
app = QApplication(sys.argv)

init_db()

window = App()
window.show()

sys.exit(app.exec())