from app import create_app, db
from app.models import Client, TargetEmployee

app = create_app()

with app.app_context():
    # 1. Clean existing database data to avoid duplicates during testing
    db.session.query(TargetEmployee).delete()
    db.session.query(Client).delete()
    db.session.commit()

    # 2. Create a mock client (SME)
    test_client = Client(
        company_name="Algarve Tech Solutions",
        contact_email="geral@algarvetech.pt"
    )
    db.session.add(test_client)
    db.session.commit() # Commit to generate the client ID

    # 3. Create mock employees linked to this client
    employee_1 = TargetEmployee(
        full_name="João Silva",
        email="joao.silva@algarvetech.pt",
        client_id=test_client.id
    )
    employee_2 = TargetEmployee(
        full_name="Maria Santos",
        email="maria.santos@algarvetech.pt",
        client_id=test_client.id
    )

    db.session.add_all([employee_1, employee_2])
    db.session.commit()

    print("Database successfully populated with test data!")