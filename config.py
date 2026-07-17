import os 
from dotenv import load_dotenv

# Load variables from .env file 
load_dotenv()

class Config: 
    """Base configuration class for the application."""
    # Secret key for signing cookies and session data
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-key-change-in-production')
    
    # Define the SQLite database location inside the instance folder
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'secura_tech.db')}"

    # Disable tracking modifications to save memory and resources 
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail / SMTP Server Configuration 
    MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USE_TLS = True 
    MAIL_USE_SSL = False 
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'security@secura.tech')