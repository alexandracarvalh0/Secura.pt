import os
from fpdf import FPDF
from datetime import datetime

class SecuraReport(FPDF):
    def header(self):
        # Top branding bar (Secura Dark Blue Theme)
        self.set_fill_color(26, 36, 43)
        self.rect(0, 0, 210, 30, 'F')
        
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.set_y(10)
        self.cell(0, 10, "Secura.tech - Relatorio Executivo de Seguranca", ln=True, align='L')
        self.ln(15)

    def footer(self):
        # Footer branding
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Confidencial - Gerado em {datetime.now().strftime('%d/%m/%Y')} - Pagina {self.page_no()}", align='C')

def generate_company_pdf(client, employees):
    """
    Generates an executive PDF report in Portuguese based on Client and TargetEmployee models.
    """
    pdf = SecuraReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Client Header Summary
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(26, 36, 43)
    pdf.cell(0, 10, f"Avaliacao de Seguranca para: {client.company_name}", ln=True)
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, f"Contacto Principal: {client.contact_email}", ln=True)
    pdf.ln(10)

    # Calculate Aggregated Metrics
    total_employees = len(employees)
    total_clicks = sum(emp.click_count for emp in employees)
    total_submissions = sum(emp.data_submission_count for emp in employees)
    
    # Executive Metrics Summary Title
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(26, 36, 43)
    pdf.cell(0, 10, "Resumo Executivo de Metricas", ln=True)
    
    # Table Header for Metrics
    pdf.set_fill_color(240, 242, 245)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(60, 8, "Metrica", border=1, fill=True)
    pdf.cell(40, 8, "Total Obtido", border=1, fill=True, align='C')
    pdf.cell(90, 8, "Avaliacao de Risco", border=1, fill=True)
    pdf.ln()
    
    # Table Rows
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(60, 8, "Colaboradores Avaliados", border=1)
    pdf.cell(40, 8, str(total_employees), border=1, align='C')
    pdf.cell(90, 8, "Grupo de amostragem inicial", border=1)
    pdf.ln()
    
    pdf.cell(60, 8, "Cliques em Links Suspeitos", border=1)
    pdf.cell(40, 8, str(total_clicks), border=1, align='C')
    if total_clicks > 0:
        pdf.set_text_color(200, 50, 50)  # Red alert
        msg = "CRITICO: Colaboradores interagiram com iscos falsos."
    else:
        pdf.set_text_color(50, 150, 50)  # Green
        msg = "Excelente: Nenhum clique registado ate ao momento."
    pdf.cell(90, 8, msg, border=1)
    pdf.ln()
    
    pdf.set_text_color(26, 36, 43)
    pdf.cell(60, 8, "Submissoes de Dados", border=1)
    pdf.cell(40, 8, str(total_submissions), border=1, align='C')
    if total_submissions > 0:
        pdf.set_text_color(200, 50, 50)
        msg = "RISCO ELEVADO: Detetada fuga simulada de credenciais!"
    else:
        pdf.set_text_color(50, 150, 50)
        msg = "Seguro: Nenhum dado foi submetido nos formularios."
    pdf.cell(90, 8, msg, border=1)
    pdf.ln(15)

    # Detailed Staff Breakdown Table
    pdf.set_text_color(26, 36, 43)
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 10, "Detoramento Granular de Alvos", ln=True)
    
    pdf.set_fill_color(26, 36, 43)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.cell(60, 8, "Nome do Colaborador", border=1, fill=True)
    pdf.cell(60, 8, "Email", border=1, fill=True)
    pdf.cell(25, 8, "Cliques", border=1, fill=True, align='C')
    pdf.cell(25, 8, "Submissoes", border=1, fill=True, align='C')
    pdf.cell(20, 8, "Estado", border=1, fill=True, align='C')
    pdf.ln()
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Helvetica', '', 10)
    
    for emp in employees:
        pdf.cell(60, 8, emp.full_name, border=1)
        pdf.cell(60, 8, emp.email, border=1)
        pdf.cell(25, 8, str(emp.click_count), border=1, align='C')
        pdf.cell(25, 8, str(emp.data_submission_count), border=1, align='C')
        
        if emp.data_submission_count > 0:
            pdf.set_text_color(200, 50, 50)
            status = "Vulneravel" # Compromised
        elif emp.click_count > 0:
            pdf.set_text_color(230, 120, 0)
            status = "Alerta" # Clicked
        else:
            pdf.set_text_color(50, 150, 50)
            status = "Seguro"
            
        pdf.cell(20, 8, status, border=1, align='C')
        pdf.set_text_color(0, 0, 0)
        pdf.ln()

    # Ensure output directory exists securely
    output_dir = os.path.join(os.getcwd(), 'instance', 'reports')
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_filename = f"report_client_{client.id}.pdf"
    pdf_path = os.path.join(output_dir, pdf_filename)
    pdf.output(pdf_path)
    
    return pdf_path