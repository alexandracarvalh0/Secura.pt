from flask import Blueprint, render_template, request, redirect, url_for, send_file
from app.models import db, Client, TargetEmployee
from app.phishing.routes import send_phishing_email
from app.utils.pdf_generator import generate_company_pdf

# Define the blueprint with a dedicated URL prefix for administration 
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
def dashboard():
    """Fetches all clients and displays them on the admin panel."""
    db.session.expire_all()
    
    all_clients = Client.query.all()
    return render_template('admin/dashboard.html', clients=all_clients)

@admin_bp.route('/client/add', methods=['POST'])
def add_client():
    """Handles the creation of a new corporate client from the dasboard form."""
    company_name = request.form.get('company_name')
    conctact_email = request.form.get('contact_email')

    if company_name and conctact_email:
        new_client = Client(company_name=company_name, contact_email=conctact_email)
        db.session.add(new_client)
        db.session.commit()
    
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/employee/add', methods=['POST'])
def add_employee():
    """Handles adding a new target employee to a specific client company."""
    full_name = request.form.get('full_name')
    email = request.form.get('email')
    client_id = request.form.get('client_id')

    if full_name and email and client_id: 
        new_employee = TargetEmployee(
            full_name=full_name,
            email=email,
            client_id=int(client_id)
        )
        db.session.add(new_employee)
        db.session.commit()
    
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/employee/send-email/<int:employee_id>', methods=['POST'])
def trigger_employee_email(employee_id):
    """Triggers a simulated phishing email to a specific target employee."""
    employee = TargetEmployee.query.get_or_404(employee_id)

    # Call the helper function designed in the phishing blueprint 
    sucess = send_phishing_email(employee)

    if sucess: 
        # For now, we print to console. Later we can add flash messages 
        print(f"Sucess: Phishing email successfully sent to {employee.email}")
    else: 
        print(f"Error: Failed to deliver email to {employee.email}")
    
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/client/download-report/<int:client_id>', methods=['GET'])
def download_client_report(client_id):
    """Fetches metrics from a client, triggers the PDF generation, and downloads it."""
    # 1. Fetches client database record
    client = Client.query.get_or_404(client_id)

    # 2. Get all target employees related to this client 
    employees = TargetEmployee.query.filter_by(client_id=client.id).all()

    # 3. Generate the PDF report using the updated utility service
    pdf_file_path = generate_company_pdf(client, employees)

    # 4. Stream file securely back to admin browser 
    return send_file(
        pdf_file_path,
        mimetype='application/pdf',
        as_attachment=True, 
        download_name=f"Secura_Report_{client.company_name.replace(' ', '_')}.pdf"
    )