"""Testes de integracao do auth basico."""

BASE = "/api/v1/auth"


def _garantir_cliente(client):
    client.post(
        f"{BASE}/register",
        json={"nome": "Cliente Teste", "email": "cliente@hotel.com", "senha": "cliente123"},
    )


def test_login_valido_retorna_token(client):
    _garantir_cliente(client)
    resp = client.post(
        f"{BASE}/login", json={"email": "cliente@hotel.com", "senha": "cliente123"}
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_invalido_retorna_401(client):
    resp = client.post(
        f"{BASE}/login", json={"email": "cliente@hotel.com", "senha": "errada"}
    )
    assert resp.status_code in (401, 404)


def test_rota_protegida_sem_token_e_bloqueada(client):
    resp = client.get(f"{BASE}/me")
    assert resp.status_code in (401, 403)


def test_rota_protegida_com_token_retorna_perfil(client):
    _garantir_cliente(client)
    token = client.post(
        f"{BASE}/login", json={"email": "cliente@hotel.com", "senha": "cliente123"}
    ).json()["access_token"]
    resp = client.get(f"{BASE}/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["email"] == "cliente@hotel.com"
    assert body["is_admin"] is False
    assert "senha" not in body


def test_cliente_nao_acessa_rota_admin(client):
    _garantir_cliente(client)
    token = client.post(
        f"{BASE}/login", json={"email": "cliente@hotel.com", "senha": "cliente123"}
    ).json()["access_token"]
    resp = client.get(
        "/api/v1/admin/cidades", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 403


def test_admin_acessa_rota_admin(client, admin_user):
    _, token = admin_user
    resp = client.get(
        "/api/v1/admin/cidades", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200

