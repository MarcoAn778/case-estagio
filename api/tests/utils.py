from fastapi.testclient import TestClient
from api.app.main import app

client = TestClient(app)

def login_request(email: str, password: str):
    return client.post(
        "/login",
        data={"username": email, "password": password}
    )

def login(email: str, password: str) -> str:
    response = login_request(email, password)
    assert response.status_code == 200, f"Login failed for {email}"
    return response.json()["access_token"]
