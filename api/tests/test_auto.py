from fastapi.testclient import TestClient
from api.app.main import app
import pytest

client = TestClient(app)

def login_request(email: str, password: str):
    return client.post(
        "/login",
        data={"username": email, "password": password}
    )


def login(email: str, password: str):
    response = login_request(email, password)
    assert response.status_code == 200, f"Login failed for {email}"
    return response.json()["access_token"]


@pytest.fixture
def user_token():
    return login("user2@gmail.com", "908ijofff")


@pytest.fixture
def admin_token():
    return login("user1@gmail.com", "oeiruhn56146")



def test_login_success():
    response = login_request("user1@gmail.com", "oeiruhn56146")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_fail():
    response = login_request("user1@gmail.com", "senha_errada")
    assert response.status_code == 401
    body = response.json()
    assert body["detail"]["code"] == "AUTH_FAILED"


def test_metrics_user_hides_cost_micros(user_token):
    response = client.get("/metrics?limit=1", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    item = response.json()[0]
    assert "cost_micros" not in item


def test_metrics_admin_shows_cost_micros(admin_token):
    response = client.get("/metrics?limit=1", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    item = response.json()[0]
    assert item["cost_micros"] is not None


def test_metrics_filter_by_date(admin_token):
    response = client.get(
        "/metrics?start_date=2024-08-16&end_date=2024-08-16",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert all(item["date"] == "2024-08-16" for item in data)


def test_metrics_ordering(admin_token):
    response = client.get(
        "/metrics?order_by=clicks&desc=false&limit=5",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    clicks = [item["clicks"] for item in data]
    assert clicks == sorted(clicks)
