import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path="sighai.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS professores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT
            );""")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS turmas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL,
                curso TEXT NOT NULL,
                periodo TEXT CHECK(periodo IN ('MANHA', 'TARDE', 'NOITE')) NOT NULL
            );""")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS grade_horaria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                turma_id INTEGER,
                slot_id INTEGER,
                professor_id INTEGER,
                disciplina_nome TEXT,
                FOREIGN KEY(turma_id) REFERENCES turmas(id),
                FOREIGN KEY(professor_id) REFERENCES professores(id)
            );""")
            conn.commit()