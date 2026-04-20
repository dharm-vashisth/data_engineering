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

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.load_data()

    def load_data(self):
        conn = get_connection()
        data = conn.execute("SELECT * FROM expenses").fetchall()
        conn.close()

        if not data:
            return

        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data[0]))
        self.table.setHorizontalHeaderLabels(["ID", "Amount", "Category", "Note"])

        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.resizeColumnsToContents()
