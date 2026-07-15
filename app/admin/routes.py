from flask import Blueprint, render_template
from app.models import Client

# Define the blueprint with a dedicated URL prefix for administration 
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
def dashboard():
    """Fetches all clients and displays them on the admin panel."""
    all_clients = Client.query.all()
    return render_template('admin/dashboard.html', clients=all_clients)
