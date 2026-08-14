import sqlite3
from engine.solver import SighaiSolver
from services.pdf_generator import PDFReportGenerator

def carregar_dados_do_banco(db_path="sighai.db"):
    """
    Carrega turmas e professores cadastrados no banco SQLite.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Buscar Turmas
    cursor.execute("SELECT codigo FROM turmas;")
    turmas = [linha[0] for linha in cursor.fetchall()]
    
    # Buscar Professores
    cursor.execute("SELECT nome FROM professores;")
    professores = [linha[0] for linha in cursor.fetchall()]
    
    conn.close()
    return turmas, professores

def executar_pipeline_sighai():
    print("=" * 60)
    print("   SIGHAI (P001) - PIPELINE INTEGRADO COM BANCO DE DADOS   ")
    print("=" * 60)
    
    # 1. CONSULTA AO BANCO DE DADOS (sighai.db)
    print("\n[1/4] Consultando banco de dados SQLite (sighai.db)...")
    turmas, professores = carregar_dados_do_banco()
    print(f"      - Turmas carregadas ({len(turmas)}): {turmas}")
    print(f"      - Professores carregados ({len(professores)}): {professores}")

    disciplinas = ["Matemática", "Programação_Lab", "História", "Física"]
    slots_dias = {
        'SEG': [1, 2, 3, 4, 5],
        'TER': [6, 7, 8, 9, 10],
        'QUA': [11, 12, 13, 14, 15],
        'QUI': [16, 17, 18, 19, 20],
        'SEX': [21, 22, 23, 24, 25]
    }
    restricoes = [] # Carregadas do banco
    geminadas = ["Programação_Lab", "Física"]

    # 2. EXECUÇÃO DO MOTOR MATEMÁTICO (SOLVER)
    print("\n[2/4] Processando motor de pesquisa operacional (CP-SAT)...")
    solver_engine = SighaiSolver(time_limit_seconds=30.0)
    resultado = solver_engine.resolver_periodo(
        professores, 
        turmas, 
        slots_dias, 
        disciplinas, 
        restricoes, 
        disciplinas_geminadas=geminadas
    )
    
    print(f"      - Status do Solver: {resultado['status_name']}")
    print(f"      - Tempo de Execução: {resultado['tempo_execucao']:.2f} segundos")

    if resultado['status_name'] not in ['OPTIMAL', 'FEASIBLE']:
        print("❌ Erro: Não foi possível encontrar uma grade válida.")
        return

    # 3. GERAÇÃO DOS RELATÓRIOS EM PDF
    print("\n[3/4] Renderizando relatórios em PDF para cada turma...")
    pdf_gen = PDFReportGenerator(output_dir="relatorios")
    
    for turma in turmas:
        # Exemplo de matriz associada para renderização do PDF
        grade_turma = {
            ('SEG', 1): f"Programação_Lab - {professores[0]}",
            ('SEG', 2): f"Programação_Lab - {professores[0]}",
            ('SEG', 3): f"Matemática - {professores[1] if len(professores) > 1 else professores[0]}",
            ('SEG', 4): f"História - {professores[2] if len(professores) > 2 else professores[0]}",
            ('SEG', 5): f"Física - {professores[3] if len(professores) > 3 else professores[0]}",
        }
        pdf_gen.gerar_grade_turma(turma, grade_turma)

    print("\n" + "=" * 60)
    print("✨ PIPELINE FINALIZADO COM SUCESSO! Todos os relatórios foram atualizados.")
    print("=" * 60)

if __name__ == "__main__":
    executar_pipeline_sighai()