from flask import Blueprint, render_template, request, redirect
from app.models import db, TargetEmployee

# Phishing routes handle landing page interactions from the target links 
phishing_bp = Blueprint('phishing', __name__)

@phishing_bp.route('/secure-login/<int:employee_id>', methods=['GET', 'POST'])
def mock_login(employee_id):
    """Simulates a secure portal to test employee security awareness."""
    employee = TargetEmployee.query.get_or_404(employee_id)

    if request.method == 'POST':
        # Target submitted form data - increment threshold counter for metrics
        employee.data_submission_count += 1 
        db.session.commit()
        # Redirect to an educational message or awareness training page
        return "Security Notice: This was a simulated phishing test."
    
    # GET request: Employee just clicked the link 
    employee.click_count += 1 
    db.session.commit()

    return render_template('phishing/fake_login.html', employee=employee)