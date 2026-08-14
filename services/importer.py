import sqlite3
import os

class DataImporter:
    """
    Módulo do SIGHAI responsável por inicializar o esquema do banco de dados SQLite (sighai.db),
    sanitizar e importar registros de professores e turmas.
    """
    def __init__(self, db_path="sighai.db"):
        self.db_path = db_path
        self.inicializar_schema()

    def inicializar_schema(self):
        """
        Garante a criação de todas as tabelas necessárias no SQLite (DDL) 
        antes de qualquer operação de leitura ou escrita.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 1. Tabela de Professores
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS professores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT
            );
        """)
        
        # 2. Tabela de Turmas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS turmas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                curso TEXT NOT NULL,
                periodo TEXT NOT NULL
            );
        """)

        # 3. Tabela de Indisponibilidades / Blockouts
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS indisponibilidades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                professor_id INTEGER,
                slot_id INTEGER,
                FOREIGN KEY(professor_id) REFERENCES professores(id)
            );
        """)

        conn.commit()
        conn.close()

    def popular_banco_simulado(self):
        """
        Popula o banco SQLite com a estrutura inicial de homologação do CEEP.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Limpa dados anteriores para homologação (Agora com a garantia que as tabelas existem)
        cursor.execute("DELETE FROM professores;")
        cursor.execute("DELETE FROM turmas;")
        cursor.execute("DELETE FROM indisponibilidades;")
        
        # Inserir Turmas
        turmas_demo = [
            ("1º_Ano_Informatica", "TÉCNICO EM INFORMÁTICA", "MANHA"),
            ("2º_Ano_Informatica", "TÉCNICO EM INFORMÁTICA", "MANHA"),
            ("3º_Ano_Informatica", "TÉCNICO EM INFORMÁTICA", "MANHA"),
            ("1º_Ano_Eletrotecnica", "TÉCNICO EM ELETROTÉCNICA", "TARDE")
        ]
        cursor.executemany("INSERT INTO turmas (codigo, curso, periodo) VALUES (?, ?, ?);", turmas_demo)

        # Inserir Professores
        profs_demo = [
            ("Anete", "anete@ceep.edu.br"),
            ("Carlos Alberto", "carlos@ceep.edu.br"),
            ("Mariana Souza", "mariana@ceep.edu.br"),
            ("Roberto Dias", "roberto@ceep.edu.br")
        ]
        cursor.executemany("INSERT INTO professores (nome, email) VALUES (?, ?);", profs_demo)
        
        conn.commit()
        conn.close()
        print("=" * 60)
        print("✅ BANCO DE DADOS 'sighai.db' ESTRUTURADO E POPULADO COM SUCESSO!")
        print("=" * 60)

if __name__ == "__main__":
    importer = DataImporter()
    importer.popular_banco_simulado()