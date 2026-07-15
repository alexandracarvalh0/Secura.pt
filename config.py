import os 

class Config: 
    """Base configuration class for the application."""
    # Secret key for signing cookies and session data
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-this-secure-key-12345'

    # Define the SQLite database location inside the instance folder
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'secura_tech.db')}"

    # Disable tracking modifications to save memory and resources 
    SQLALCHEMY_TRACK_MODIFICATIONS = False