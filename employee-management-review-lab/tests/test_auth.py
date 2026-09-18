from app import create_app


def test_admin_can_login():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    client = app.test_client()
    response = client.post("/api/auth/login", json={"email": "admin", "password": "Welcome123"})
    assert response.status_code == 200
    assert response.get_json()


def test_bad_login_fails():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})
    response = app.test_client().post("/api/auth/login", json={"email": "x", "password": "x"})
    assert response.status_code != 200
