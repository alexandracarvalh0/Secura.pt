from flask import Blueprint, render_template, request, redirect, current_app
from flask_mail import Message
from app.models import db, TargetEmployee

# Phishing routes handle landing page interactions from the target links 
phishing_bp = Blueprint('phishing', __name__)

def send_phishing_email(employee):
    """Generates and send a simulated phishing email to a target employee."""
    # Break the circular import by importing 'mail' locally inside the function
    from app import mail

    # Generate the unique personalized URL for this employee to click
    # Under local testing, we hardcode localhost:5000. In production, we'll fetch our domain
    target_link = f"http://127.0.0.1:5000/secure-login/{employee.id}"

    # Define the bait email structure (using HTML to make it look realistic)
    subject = "Action Required: Immediate Security Token Verification"

    msg = Message(
        subject=subject,
        recipients=[employee.email],
        # The sender will fallback to MAIL_DEFAULT_SENDER config if not set 
    )

    # Phishing Email bait payload in PT-PT
    msg.html = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #ddd; max-width: 600px;">
        <h2 style="color: #de350b;">Alerta de Segurança - Acessos Corporativos</h2>
        <p>Olá <strong>{employee.full_name}</strong>,</p>
        <p>Os nossos sistemas de monitorização de segurança detetaram uma tentativa de acesso invulgar à sua conta através de um endereço IP não reconhecido.</p>
        <p>Para proteger a sua ligação e manter a sua conta ativa, é obrigatório revalidar o seu token de sessão Single Sign-On (SSO) nas próximas 24 horas.</p>
        <div style="margin: 30px 0; text-align: center;">
            <a href="{target_link}" style="background-color: #1877f2; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold; display: inline-block;">Verificar Acesso ao Painel</a>
        </div>
        <p style="font-size: 0.85rem; color: #777;">Se não realizar esta verificação, o seu acesso às ferramentas da empresa poderá ser temporariamente bloqueado.</p>
        <hr style="border: 0; border-top: 1px solid #eee; margin-top: 20px;">
        <p style="font-size: 0.8rem; color: #999;">Esta é uma notificação automática do sistema. Por favor, não responda diretamente a este e-mail.</p>
    </div>
    """
    
    try:
        mail.send(msg)
        return True
    except Exception as e:
        # If SMTP server fails or connection is lost, log the error safely
        print(f"Error sending email to {employee.email}: {e}")
        return False

@phishing_bp.route('/secure-login/<int:employee_id>', methods=['GET', 'POST'])
def mock_login(employee_id):
    """Simulates a secure portal to test employee security awareness."""
    employee = TargetEmployee.query.get_or_404(employee_id)

    if request.method == 'POST':
        # Target submitted form data - increment threshold counter for metrics
        employee.data_submission_count += 1 
        db.session.commit()
        # Redirect to an educational message or awareness training page
        return render_template('phishing/notice.html')   
    
    # GET request: Employee just clicked the link 
    employee.click_count += 1 
    db.session.commit()

    return render_template('phishing/fake_login.html', employee=employee)