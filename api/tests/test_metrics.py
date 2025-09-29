import pytest

@pytest.mark.parametrize("limit", [1])
def test_metrics_user_hides_cost_micros(client_user, limit):
    response = client_user.get(f"/metrics?limit={limit}")
    assert response.status_code == 200, "Falha ao buscar métricas como user"
    item = response.json()[0]
    assert "cost_micros" not in item, "User não deve ver cost_micros"

@pytest.mark.parametrize("limit", [1])
def test_metrics_admin_shows_cost_micros(client_admin, limit):
    response = client_admin.get(f"/metrics?limit={limit}")
    assert response.status_code == 200, "Falha ao buscar métricas como admin"
    item = response.json()[0]
    assert item.get("cost_micros") is not None, "Admin deve ver cost_micros"

def test_metrics_filter_by_date(client_admin):
    response = client_admin.get("/metrics?start_date=2024-08-16&end_date=2024-08-16")
    assert response.status_code == 200
    data = response.json()
    assert all(item["date"] == "2024-08-16" for item in data), "Datas filtradas incorretamente"

def test_metrics_ordering(client_admin):
    response = client_admin.get("/metrics?order_by=clicks&desc=false&limit=5")
    assert response.status_code == 200
    data = response.json()
    clicks = [item["clicks"] for item in data]
    assert clicks == sorted(clicks), "Métricas não estão ordenadas corretamente"
