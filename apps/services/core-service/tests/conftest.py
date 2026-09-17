"""Fixtures de teste para o StayFlow.

Configura:
- Banco SQLite em memoria para testes isolados
- TestClient com override de get_db
- Fixtures de usuario admin e cliente
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import get_db
from app.core.security import get_password_hash
from app.main import app
from app.models import Base
from app.models.usuario import Usuario

# Banco SQLite em arquivo temporario para os testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    # Desativamos raise_server_exceptions para validar retornos de erro 500
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def admin_user(db_session):
    """Cria um usuario admin de teste e retorna (usuario, token)."""
    from app.core.security import create_access_token

    user = Usuario(
        nome="Admin Teste",
        email="admin@test.com",
        senha_hash=get_password_hash("admin123"),
        is_admin=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    token = create_access_token(subject=user.email)
    return user, token


@pytest.fixture(scope="function")
def client_user(db_session):
    """Cria um usuario cliente de teste e retorna (usuario, token)."""
    from app.core.security import create_access_token

    user = Usuario(
        nome="Cliente Teste",
        email="cliente@test.com",
        senha_hash=get_password_hash("cliente123"),
        is_admin=False,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    token = create_access_token(subject=user.email)
    return user, token
