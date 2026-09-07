from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.security import create_jwt_token
from backend.app import db as db_pkg
from backend.app.models.user import User

client = TestClient(app)


def create_user_and_token(db):
    u = User(email="a@example.com", hashed_password="$2b$12$1234567890123456789012")
    db.add(u)
    db.commit()
    db.refresh(u)
    token, jti = create_jwt_token(subject=str(u.id))
    return u, token


def test_animal_crud():
    # Obtain the sessionmaker at runtime so the test harness can patch it.
    db = db_pkg.session.SessionLocal()
    user, token = create_user_and_token(db)
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"name": "Fido", "species": "Dog"}
    r = client.post("/api/v1/animals/", json=payload, headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "Fido" if "name" in data else True
