import os 
from flask import Flask
from app.models import db
from app.admin.routes import admin_bp
from app.phishing.routes import phishing_bp

def create_app():
    """Application factory to initialize and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Ensure the instance folder exists for the SQLite database
    try: 
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize the database extension with the app context
    db.init_app(app)

    # Register Blueprints for modular routing 
    app.register_blueprint(admin_bp)
    app.register_blueprint(phishing_bp)

    # Create database tables automatically if they do not exist
    with app.app_context():
        db.create_all()
    
    return app