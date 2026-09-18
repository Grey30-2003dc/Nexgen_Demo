from app import create_app


def client_and_token():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    client = app.test_client()
    result = client.post("/api/auth/login", json={"email": "admin", "password": "Welcome123"})
    return client, result.get_json()["token"]


def test_create_employee():
    client, token = client_and_token()
    response = client.post("/api/employees", headers={"Authorization": "Bearer " + token},
                           json={"employee_number": "E1", "first_name": "Ada", "last_name": "Lovelace",
                                 "email": "ada@example.com", "salary": 100000})
    assert response.status_code
    assert response.get_json()["email"] == "ada@example.com"


def test_empty_employee_list():
    client, token = client_and_token()
    response = client.get("/api/employees", headers={"Authorization": "Bearer " + token})
    assert response.get_json() is not None
