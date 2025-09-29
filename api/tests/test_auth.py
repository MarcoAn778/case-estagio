import pytest
from .utils import login_request

@pytest.mark.parametrize(
    "email,password,status,token_type",
    [
        ("user1@gmail.com", "oeiruhn56146", 200, "bearer"),
        ("user1@gmail.com", "senha_errada", 401, None)
    ]
)
def test_login(email, password, status, token_type):
    response = login_request(email, password)
    assert response.status_code == status, f"Falha de login para {email}"
    
    if status == 200:
        data = response.json()
        assert "access_token" in data, "Token de acesso não retornado"
        assert data["token_type"] == token_type, "Tipo de token incorreto"
    else:
        body = response.json()
        assert body["detail"]["code"] == "AUTH_FAILED", "Erro de autenticação incorreto"
