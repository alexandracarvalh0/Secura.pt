from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy instance
db = SQLAlchemy()

class Client(db.Model):
    """Represents a corporate client (SME) registered in the system."""
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(120), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    # Relationship: One client can have multiple target employees
    employees = db.relationship('TargetEmployee', backref='client', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Client {self.company_name}>"

class TargetEmployee(db.Model):
    """Represents an employee who whill be targetted in phishing simulations."""
    __tablename__ = 'target_employees'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    # Foreign key linking to the parent Client 
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    # Simulation interaction metrics 
    click_count = db.Column(db.Integer, default=0)
    data_submission_count = db.Column(db.Integer, default=0) # Tracks actions without storing credentials

    def __repr__(self):
        return f"<Employee {self.email} | Clicks: {self.click_count}>"