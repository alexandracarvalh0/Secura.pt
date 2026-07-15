# Secura.tech - Phishing Simulation Platform for SMEs

Secura.tech (internally codenamed PhishArmor) is a specialized security awareness and offensive security SaaS platform designed for Portuguese Small and Medium Enterprises (SMEs). It allows the administrator to simulate highly realistic phishing campaigns in Portuguese to test, evaluate, and educate client employees on digital threats.

This project uses a **B2B Push-Report model**: corporate clients do not have individual logins. Instead, the administrator controls everything via a centralized admin dashboard and sends monthly performance reports directly to clients via PDF.

---

## Technical Stack
* **Operating System**: Linux (Ubuntu Server target) 
* **Backend Framework**: Python with Flask (Application Factory & Blueprints pattern)
* **Database**: SQLite (Development) with SQLAlchemy ORM (configured for seamless future PostgreSQL migration) 

---

## Directory and File Architecture

```text
secura-tech/
├── app/                      # Main application package
│   ├── __init__.py           # Application Factory initialization
│   ├── models.py             # Database schemas & relationships (SQLAlchemy ORM)
│   ├── admin/                # Blueprint for central administrator features
│   │   └── routes.py         # Routes to manage clients and view simulations
│   ├── phishing/             # Blueprint for educational phishing simulations
│   │   └── routes.py         # Landing pages and click/submission counters
│   └── templates/            # HTML templates organized by blueprint
├── config.py                 # Central configurations & Environment Variables
├── run.py                    # Entry point script to run the local development server
└── requirements.txt          # Python dependencies list
```

---

## Module Breakdown

- **app/__init__.py**: Houses the `create_app()` factory function. Prevents circular imports, registers blueprints, and triggers the SQLite database creation on boot.

- **app/models.py**: Defines SQL tables. Integrates a strict security-by-design flow where raw passwords are never saved, respecting GDPR compliance guidelines.

- **app/admin/**: Accessible strictly by the core administrator to manage companies, track registered targets, and compile metrics.

- **app/phishing/**: Isolated tracking URLs (e.g., `/secure-login/<id>`) that capture user interactions dynamically without interfering with core administrative code.

---

## Setup & Local Installation

Follow these steps to run the application locally on your Linux environment:

1. Clone & Navigate
```bash
    git clone <your-repository-url>
    cd secura-tech
```

2. Configure Virtual Environment (venv)
```bash
    # Create the virtual environment
    python3 -m venv .venv

    # Activate the virtual environment
    source .venv/bin/activate
```

3. Install Dependencies
```bash
    pip install -r requirements.txt
```

4. Run the Server
```bash
    python run.py
```

The server will boot locally at `http://127.0.0.1:5000/`.

Access the central control board directly at `http://127.0.0.1:5000/admin/dashboard`.

---

## Compliance & Privacy Policy (GDPR)

Secura.tech evaluates corporate vulnerabilities without collecting high-risk private data.

- **No credentials are captured**: If an employee submits mock forms, the system increments an abstract numeric counter (`data_submission_count`).

- **Isolated tracking**: No personal identifiers are exposed to search engines or external tracking modules.