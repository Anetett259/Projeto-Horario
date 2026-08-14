import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class PDFReportGenerator:
    """
    Módulo do SIGHAI responsável por converter os resultados do Solver 
    em relatórios em PDF formatados e prontos para impressão.
    """
    def __init__(self, output_dir="relatorios"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def gerar_grade_turma(self, nome_turma, matriz_horario, dias=['SEG', 'TER', 'QUA', 'QUI', 'SEX'], num_aulas=5):
        """
        Gera o PDF da grade horária para uma turma específica.
        :param matriz_horario: Dicionário no formato {(dia, aula_num): "Disciplina - Professor"}
        """
        filepath = os.path.join(self.output_dir, f"Grade_{nome_turma}.pdf")
        doc = SimpleDocTemplate(filepath, pagesize=landscape(A4), rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Título do Relatório
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1A365D'),
            alignment=1, # Centralizado
            spaceAfter=15
        )
        elements.append(Paragraph(f"<b>CEEP AI LAB - Grade Horária: {nome_turma}</b>", title_style))
        elements.append(Spacer(1, 10))

        # Montagem da Tabela (Cabeçalho: Horário / Dias)
        data = [["Aula / Horário"] + dias]
        
        for aula in range(1, num_aulas + 1):
            linha = [f"{aula}ª Aula"]
            for dia in dias:
                conteudo = matriz_horario.get((dia, aula), "VAGO")
                linha.append(conteudo)
            data.append(linha)

        # Estilização Profissional da Tabela
        tabela = Table(data, colWidths=[90] + [140]*len(dias))
        tabela.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A365D')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E0')),
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#EDF2F7')),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ]))
        
        elements.append(tabela)
        doc.build(elements)
        print(f"📄 Relatório gerado com sucesso: {filepath}")
        return filepath

if __name__ == "__main__":
    # Teste isolado do gerador de PDF
    generator = PDFReportGenerator()
    
    # Matriz simulada retornada pelo Solver
    grade_exemplo = {
        ('SEG', 1): "Programação - Prof_1",
        ('SEG', 2): "Programação - Prof_1",
        ('SEG', 3): "Matemática - Prof_4",
        ('SEG', 4): "História - Prof_8",
        ('SEG', 5): "Física - Prof_12",
        ('TER', 1): "Banco de Dados - Prof_2",
        ('TER', 2): "Banco de Dados - Prof_2",
    }
    
    generator.gerar_grade_turma("3º_Ano_Informatica", grade_exemplo)