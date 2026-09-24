"""Testes de autenticacao — registro, login e RBAC."""

import pytest


class TestAuthRegister:
    """Testes para POST /api/v1/auth/register"""

    def test_register_sucesso(self, client):
        response = client.post(
            "/api/v1/auth/register",
            json={"nome": "Joao Silva", "email": "joao@test.com", "senha": "senha123"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "joao@test.com"
        assert data["nome"] == "Joao Silva"
        assert data["is_admin"] is False
        assert "id" in data

    def test_register_email_duplicado(self, client):
        # Primeiro registro
        client.post(
            "/api/v1/auth/register",
            json={"nome": "Maria", "email": "maria@test.com", "senha": "senha123"},
        )
        # Segundo com mesmo email
        response = client.post(
            "/api/v1/auth/register",
            json={"nome": "Maria 2", "email": "maria@test.com", "senha": "senha456"},
        )
        assert response.status_code == 409

    def test_register_email_invalido(self, client):
        response = client.post(
            "/api/v1/auth/register",
            json={"nome": "Test", "email": "nao-e-email", "senha": "senha123"},
        )
        assert response.status_code == 422


class TestAuthLogin:
    """Testes para POST /api/v1/auth/login"""

    def test_login_sucesso(self, client):
        # Registrar primeiro
        client.post(
            "/api/v1/auth/register",
            json={"nome": "Login Test", "email": "login@test.com", "senha": "senha123"},
        )
        # Fazer login
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "login@test.com", "senha": "senha123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_credenciais_invalidas(self, client):
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "inexistente@test.com", "senha": "errada"},
        )
        assert response.status_code == 401

    def test_login_senha_errada(self, client):
        client.post(
            "/api/v1/auth/register",
            json={"nome": "Test", "email": "test@test.com", "senha": "correta"},
        )
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@test.com", "senha": "errada"},
        )
        assert response.status_code == 401


class TestAuthMe:
    """Testes para GET /api/v1/auth/me"""

    def test_me_autenticado(self, client, client_user):
        user, token = client_user
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == user.email
        assert data["nome"] == user.nome

    def test_me_sem_token(self, client):
        response = client.get("/api/v1/auth/me")
        assert response.status_code in (401, 403)

    def test_me_token_invalido(self, client):
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer token_invalido"},
        )
        assert response.status_code == 401


class TestAuthRBAC:
    """Testes de autorizacao RBAC (admin vs cliente)."""

    def test_admin_endpoint_como_admin(self, client, admin_user):
        _, token = admin_user
        response = client.get(
            "/api/v1/auth/admin/verificacao",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200

    def test_admin_endpoint_como_cliente(self, client, client_user):
        _, token = client_user
        response = client.get(
            "/api/v1/auth/admin/verificacao",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    def test_admin_endpoint_sem_auth(self, client):
        response = client.get("/api/v1/auth/admin/verificacao")
        assert response.status_code in (401, 403)
