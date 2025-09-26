from fastapi.testclient import TestClient
from api.app.main import app

client = TestClient(app)

def login(email: str, password: str):
    return client.post(
        "/login",
        data={"username": email, "password": password}
    )

def test_login_success():
    response = login("user1@gmail.com", "oeiruhn56146")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_fail():
    response = login("user1@gmail.com", "senha_errada")
    assert response.status_code == 401
    body = response.json()
    assert body["detail"]["code"] == "AUTH_FAILED"

def test_metrics_user_hides_cost_micros():
    token = login("user2@gmail.com", "908ijofff").json()["access_token"]
    response = client.get("/metrics?limit=1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    item = response.json()[0]
    assert item["cost_micros"] is None

def test_metrics_admin_shows_cost_micros():
    token = login("user1@gmail.com", "oeiruhn56146").json()["access_token"]
    response = client.get("/metrics?limit=1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    item = response.json()[0]
    assert item["cost_micros"] is not None
