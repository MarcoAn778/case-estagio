import pytest
from .utils import login, client as test_client

@pytest.fixture
def user_token():
    return login("user2@gmail.com", "908ijofff")

@pytest.fixture
def admin_token():
    return login("user1@gmail.com", "oeiruhn56146")

@pytest.fixture
def client_user(user_token):
    test_client.headers.update({"Authorization": f"Bearer {user_token}"})
    return test_client

@pytest.fixture
def client_admin(admin_token):
    test_client.headers.update({"Authorization": f"Bearer {admin_token}"})
    return test_client
