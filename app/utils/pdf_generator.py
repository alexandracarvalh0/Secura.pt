import os
from fpdf import FPDF
from datetime import datetime

class SecuraReport(FPDF):
    def header(self):
        # Top branding bar (Secura Dark Blue Theme)
        self.set_fill_color(26, 36, 43) # Navy Blue
        self.rect(0, 0, 210, 28, 'F')
        
        # Header Brand Text
        self.set_font('Helvetica', 'B', 15)
        self.set_text_color(255, 255, 255)
        self.set_xy(12, 9)
        self.cell(0, 10, "Secura.pt  |  Relatorio Executivo de Riscos", ln=False, align='L')
        
        # Security Badge/Tag on top right
        self.set_font('Helvetica', 'B', 8)
        self.set_fill_color(40, 54, 64)
        self.rect(155, 10, 42, 8, 'F')
        self.set_xy(155, 9)
        self.cell(42, 10, "CONFIDENCIAL", align='C')
        
        self.ln(22)

    def footer(self):
        # Bottom Line
        self.set_draw_color(220, 224, 230)
        self.line(10, 282, 200, 282)
        
        # Footer branding & Page Numbering
        self.set_y(-12)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(130, 130, 130)
        self.cell(100, 10, f"Secura.pt - Plataforma de Sensibilizacao de Riscos Digitais", align='L')
        self.cell(90, 10, f"Gerado em {datetime.now().strftime('%d/%m/%Y')} | Pagina {self.page_no()}", align='R')

    def draw_card(self, x, y, width, height, title, value, status_color, subtitle=""):
        """Draws a clean executive KPI metric card."""
        self.set_fill_color(248, 249, 250)
        self.set_draw_color(220, 224, 230)
        self.rect(x, y, width, height, 'DF')
        
        # Colored left accent border
        self.set_fill_color(*status_color)
        self.rect(x, y, 3, height, 'F')
        
        # Card Title
        self.set_xy(x + 6, y + 3)
        self.set_font('Helvetica', 'B', 8)
        self.set_text_color(100, 110, 120)
        self.cell(width - 8, 5, title.upper(), ln=True)
        
        # Card Main Value
        self.set_xy(x + 6, y + 9)
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(26, 36, 43)
        self.cell(width - 8, 8, str(value), ln=True)
        
        # Card Subtitle / Indicator
        if subtitle:
            self.set_xy(x + 6, y + 17)
            self.set_font('Helvetica', '', 7)
            self.set_text_color(*status_color)
            self.cell(width - 8, 4, subtitle, ln=True)

def generate_company_pdf(client, employees):
    """
    Generates a premium executive PDF report in Portuguese.
    """
    pdf = SecuraReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # ---------------------------------------------------------
    # 1. CLIENT HEADER & SUMMARY
    # ---------------------------------------------------------
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(26, 36, 43)
    pdf.cell(0, 7, f"Avaliacao de Vulnerabilidade Humana: {client.company_name}", ln=True)
    
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(110, 110, 110)
    pdf.cell(0, 5, f"Email Corporativo de Contacto: {client.contact_email}", ln=True)
    pdf.ln(5)
    
    # Separator Line
    pdf.set_draw_color(230, 235, 240)
    pdf.line(10, 48, 200, 48)
    pdf.ln(8)

    # ---------------------------------------------------------
    # 2. METRICS CALCULATION & KPI CARDS
    # ---------------------------------------------------------
    total_employees = len(employees)
    total_clicks = sum(emp.click_count for emp in employees)
    total_submissions = sum(emp.data_submission_count for emp in employees)
    
    # Risk Rate Calculation
    vulnerable_count = sum(1 for emp in employees if emp.data_submission_count > 0 or emp.click_count > 0)
    vuln_rate = round((vulnerable_count / total_employees * 100), 1) if total_employees > 0 else 0
    
    # Color logic based on vulnerability rate
    if vuln_rate > 30:
        overall_status_color = (217, 83, 79) # Red
        overall_status_text = "Nivel de Risco: CRITICO"
    elif vuln_rate > 0:
        overall_status_color = (240, 173, 78) # Orange
        overall_status_text = "Nivel de Risco: MODERADO"
    else:
        overall_status_color = (92, 184, 92) # Green
        overall_status_text = "Nivel de Risco: SEGURO"

    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(26, 36, 43)
    pdf.cell(0, 6, "1. Indicadores Chave de Desempenho (KPIs)", ln=True)
    pdf.ln(3)

    # KPI Cards Row (4 Cards layout)
    card_y = pdf.get_y()
    pdf.draw_card(10, card_y, 44, 24, "Amostragem", f"{total_employees} Colab.", (26, 36, 43), "Grupo sob teste")
    pdf.draw_card(58, card_y, 44, 24, "Interacoes", f"{total_clicks} Cliques", (240, 173, 78) if total_clicks > 0 else (92, 184, 92), "Links acedidos")
    pdf.draw_card(106, card_y, 44, 24, "Credenciais", f"{total_submissions} Dados", (217, 83, 79) if total_submissions > 0 else (92, 184, 92), "Submissoes de formularios")
    pdf.draw_card(154, card_y, 46, 24, "Taxa de Risco", f"{vuln_rate}%", overall_status_color, overall_status_text)

    pdf.set_y(card_y + 30)

    # ---------------------------------------------------------
    # 3. VISUAL PROGRESS BAR (NATIVE GRAPH)
    # ---------------------------------------------------------
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(26, 36, 43)
    pdf.cell(0, 6, "Exposicao Global da Equipas (Distribuicao de Risco)", ln=True)
    pdf.ln(2)

    bar_y = pdf.get_y()
    bar_width = 190
    bar_height = 10
    
    # Calculate widths for green vs red/orange bar
    safe_count = total_employees - vulnerable_count
    safe_ratio = safe_count / total_employees if total_employees > 0 else 1
    safe_width = bar_width * safe_ratio
    vuln_width = bar_width - safe_width

    # Draw Safe Part (Green)
    pdf.set_fill_color(92, 184, 92)
    pdf.rect(10, bar_y, safe_width, bar_height, 'F')

    # Draw Vulnerable Part (Red/Orange)
    if vuln_width > 0:
        pdf.set_fill_color(217, 83, 79)
        pdf.rect(10 + safe_width, bar_y, vuln_width, bar_height, 'F')

    # Legend Below Bar
    pdf.set_y(bar_y + 12)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(92, 184, 92)
    pdf.cell(95, 5, f"[+] Resilientes: {safe_count} colaboradores ({round(safe_ratio*100,1)}%)", align='L')
    pdf.set_text_color(217, 83, 79)
    pdf.cell(95, 5, f"[-] Vulneraveis: {vulnerable_count} colaboradores ({round((1-safe_ratio)*100,1)}%)", align='R', ln=True)
    pdf.ln(8)

    # ---------------------------------------------------------
    # 4. GRANULAR TARGET BREAKDOWN TABLE
    # ---------------------------------------------------------
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(26, 36, 43)
    pdf.cell(0, 6, "2. Detalhamento Granular por Colaborador", ln=True)
    pdf.ln(3)

    # Table Header
    pdf.set_fill_color(26, 36, 43)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(50, 7, "  Nome do Colaborador", border=0, fill=True)
    pdf.cell(65, 7, "Email", border=0, fill=True)
    pdf.cell(25, 7, "Cliques", border=0, fill=True, align='C')
    pdf.cell(25, 7, "Submissoes", border=0, fill=True, align='C')
    pdf.cell(25, 7, "Estado", border=0, fill=True, align='C')
    pdf.ln()

    # Table Body Rows
    pdf.set_font('Helvetica', '', 9)
    fill_row = False
    
    for emp in employees:
        # Alternating background row color
        if fill_row:
            pdf.set_fill_color(248, 249, 250)
        else:
            pdf.set_fill_color(255, 255, 255)

        pdf.set_text_color(40, 40, 40)
        pdf.cell(50, 7, f"  {emp.full_name[:24]}", border='B', fill=True)
        pdf.cell(65, 7, f"{emp.email[:32]}", border='B', fill=True)
        pdf.cell(25, 7, str(emp.click_count), border='B', fill=True, align='C')
        pdf.cell(25, 7, str(emp.data_submission_count), border='B', fill=True, align='C')

        # Status Tag logic
        if emp.data_submission_count > 0:
            pdf.set_text_color(217, 83, 79) # Red
            status_str = "Comprometido"
        elif emp.click_count > 0:
            pdf.set_text_color(240, 173, 78) # Orange
            status_str = "Em Alerta"
        else:
            pdf.set_text_color(92, 184, 92) # Green
            status_str = "Seguro"

        pdf.set_font('Helvetica', 'B', 8)
        pdf.cell(25, 7, status_str, border='B', fill=True, align='C')
        pdf.set_font('Helvetica', '', 9)
        pdf.ln()
        
        fill_row = not fill_row

    pdf.ln(10)

    # ---------------------------------------------------------
    # 5. EXECUTIVE RECOMMENDATIONS BOX
    # ---------------------------------------------------------
    pdf.set_fill_color(240, 244, 248)
    pdf.set_draw_color(200, 215, 230)
    
    box_y = pdf.get_y()
    pdf.rect(10, box_y, 190, 26, 'DF')
    
    pdf.set_xy(14, box_y + 3)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(26, 36, 43)
    pdf.cell(0, 5, "Recomendacao da Secura.pt para a Direcao:", ln=True)
    
    pdf.set_x(14)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(80, 90, 100)
    
    if vuln_rate > 0:
        rec_text = "Foram detetadas interacoes com iscos de simulacao. E altamente recomendado promover um ciclo de formaçoes curtas sobre identificacao de phishing para reduzir a vulnerabilidade da empresa perante ameacas reais."
    else:
        rec_text = "Excelente postura preventiva demonstrada pela equipa. Recomenda-se a realizacao periodica de novas simulacoes contextuais para manter o nivel de alerta elevado perante novas tecnicas de engenharia social."
        
    pdf.multi_cell(182, 4, rec_text)

    # ---------------------------------------------------------
    # SAVE PDF OUTPUT
    # ---------------------------------------------------------
    output_dir = os.path.join(os.getcwd(), 'instance', 'reports')
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_filename = f"report_client_{client.id}.pdf"
    pdf_path = os.path.join(output_dir, pdf_filename)
    pdf.output(pdf_path)
    
    return pdf_path