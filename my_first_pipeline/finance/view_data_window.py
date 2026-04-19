from PySide6.QtWidgets import ( QMainWindow, QVBoxLayout,
    QWidget, QTableWidget, QTableWidgetItem
)
from db.database import get_connection

class ViewDataWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("All Expenses")
        self.setGeometry(300, 300, 500, 400)

        self.table = QTableWidget()
        self.load_data()

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_data(self):
        conn = get_connection()

        result = conn.execute("SELECT * FROM expenses").fetchall()

        conn.close()

        if not result:
            return

        # Set table size
        self.table.setRowCount(len(result))
        self.table.setColumnCount(len(result[0]))

        # Set headers
        headers = ["ID", "Amount", "Category", "Note"]
        self.table.setHorizontalHeaderLabels(headers)

        # Fill data
        for row_idx, row in enumerate(result):
            for col_idx, value in enumerate(row):
                self.table.setItem(
                    row_idx, col_idx,
                    QTableWidgetItem(str(value))
                )
