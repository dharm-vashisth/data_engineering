from db.database import get_connection


def add_expense(amount, category, note):
    conn = get_connection()

    conn.execute(
        "INSERT INTO expenses (amount, category, note) VALUES (?, ?, ?)",
        (amount, category, note)
    )

    conn.close()


def get_all_expenses():
    conn = get_connection()

    data = conn.execute("SELECT * FROM expenses").fetchall()

    conn.close()
    return data