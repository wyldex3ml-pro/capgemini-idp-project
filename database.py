"""
database.py
------------
Handles storage of processed documents using SQLite (no separate DB server needed,
easy to demo). This is where extracted + classified data is persisted.
"""

import sqlite3

DB_PATH = "idp_database.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            doc_type TEXT,
            vendor TEXT,
            invoice_number TEXT,
            date TEXT,
            amount TEXT,
            raw_text TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_document(filename, doc_type, fields, raw_text):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO documents (filename, doc_type, vendor, invoice_number, date, amount, raw_text)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        filename, doc_type, fields.get("vendor"), fields.get("invoice_number"),
        fields.get("date"), fields.get("amount"), raw_text
    ))
    conn.commit()
    conn.close()


def get_all_documents():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, filename, doc_type, vendor, invoice_number, date, amount FROM documents ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows
