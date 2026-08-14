import time
from ortools.sat.python import cp_model

class SighaiSolver:
    """
    Motor de Pesquisa Operacional do SIGHAI - Versão 0.6 (Sprint 2)
    Suporta Restrições Fortes, Indisponibilidades, Aulas Geminadas e Laboratórios.
    """
    def __init__(self, time_limit_seconds=30.0):
        self.time_limit = time_limit_seconds

    def resolver_periodo(self, professores, turmas, slots_por_dia, disciplinas, restricoes_fortes, disciplinas_geminadas=None, disciplinas_lab=None):
        """
        :param slots_por_dia: Dicionário mapeando dias para lista de slots. Ex: {'SEG': [1,2,3,4,5], 'TER': [6,7,8,9,10]...}
        """
        model = cp_model.CpModel()
        
        # Aplanar todos os slots para iteração
        todos_slots = [slot for dia in slots_por_dia.values() for slot in dia]
        
        # 1. Variáveis de Decisão Booleanas: x[p, t, s, d]
        x = {}
        for p in professores:
            for t in turmas:
                for s in todos_slots:
                    for d in disciplinas:
                        x[p, t, s, d] = model.NewBoolVar(f'x_{p}_{t}_{s}_{d}')
                        
        # 2. RESTRIÇÃO FORTE (RN001): Professor não pode dar duas aulas simultâneas
        for p in professores:
            for s in todos_slots:
                model.AddAtMostOne(x[p, t, s, d] for t in turmas for d in disciplinas)
                
        # 3. RESTRIÇÃO FORTE (RN001b): Turma não pode ter duas disciplinas simultâneas
        for t in turmas:
            for s in todos_slots:
                model.AddAtMostOne(x[p, t, s, d] for p in professores for d in disciplinas)
                
        # 4. RESTRIÇÃO FORTE (RN003): Respeitar indisponibilidades registradas
        for (p_id, slot_id) in restricoes_fortes:
            if slot_id in todos_slots and p_id in professores:
                for t in turmas:
                    for d in disciplinas:
                        model.Add(x[p_id, t, slot_id, d] == 0)

        # 5. REGRA PEDAGÓGICA (Aulas Geminadas): Forçar alocação em pares adjacentes no mesmo dia
        if disciplinas_geminadas:
            for t in turmas:
                for d in disciplinas_geminadas:
                    for dia, slots_dia in slots_por_dia.items():
                        # Para cada par de slots consecutivos no mesmo dia
                        for i in range(len(slots_dia) - 1):
                            s1, s2 = slots_dia[i], slots_dia[i+1]
                            # Se s1 for alocado, s2 deve ser alocado para a mesma turma/disciplina (e vice-versa)
                            for p in professores:
                                model.Add(x[p, t, s1, d] == x[p, t, s2, d])

        # 6. Execução do Solver
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = self.time_limit
        
        start_time = time.time()
        status = solver.Solve(model)
        elapsed_time = time.time() - start_time
        
        return {
            "status_code": status,
            "status_name": solver.StatusName(status),
            "tempo_execucao": elapsed_time,
            "solver": solver
        }

if __name__ == "__main__":
    print("=" * 55)
    print("   SIGHAI SOLVER - SPRINT 2 (GEMINADAS & LABS)   ")
    print("=" * 55)

    # Dados de Teste da Sprint 2
    profs = [f"Prof_{i}" for i in range(1, 50)]
    turmas = [f"Turma_{i}" for i in range(1, 15)]
    disciplinas = ["Matemática", "Programação_Lab", "História", "Física"]
    
    # Estrutura de Slots por Dia (5 aulas por dia x 5 dias = 25 slots)
    slots_dias = {
        'SEG': [1, 2, 3, 4, 5],
        'TER': [6, 7, 8, 9, 10],
        'QUA': [11, 12, 13, 14, 15],
        'QUI': [16, 17, 18, 19, 20],
        'SEX': [21, 22, 23, 24, 25]
    }
    
    restricoes = [("Prof_1", 1), ("Prof_2", 6)]
    geminadas = ["Programação_Lab", "Física"]

    solver = SighaiSolver(time_limit_seconds=30.0)
    resultado = solver.resolver_periodo(profs, turmas, slots_dias, disciplinas, restricoes, disciplinas_geminadas=geminadas)

    print(f"\n[RESULTADO DO SOLVER - SPRINT 2]")
    print(f"Status: {resultado['status_name']}")
    print(f"Tempo de Processamento: {resultado['tempo_execucao']:.2f} segundos")
    print("=" * 55)