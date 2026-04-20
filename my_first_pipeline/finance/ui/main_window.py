from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QLineEdit, QPushButton, QLabel, QFormLayout
)

from features.expenses import add_expense
from ui.view_data_window import ViewDataWindow


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Finance Tracker")
        self.setGeometry(200, 200, 400, 300)

        # Inputs
        self.amount = QLineEdit()
        self.category = QLineEdit()
        self.note = QLineEdit()

        # Buttons
        self.add_btn = QPushButton("Add Expense")
        self.add_btn.clicked.connect(self.save_data)

        self.view_btn = QPushButton("View Expenses")
        self.view_btn.clicked.connect(self.open_view_window)

        # Status
        self.status = QLabel("")

        # Layout
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

    def save_data(self):
        add_expense(
            float(self.amount.text()),
            self.category.text(),
            self.note.text()
        )

        self.status.setText("Saved ✅")

        self.amount.clear()
        self.category.clear()
        self.note.clear()

    def open_view_window(self):
        self.view_window = ViewDataWindow()
        self.view_window.show()