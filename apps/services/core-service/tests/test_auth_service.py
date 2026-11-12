"""Testes unitarios do AuthService (register_user e authenticate_user).

Chamam os services diretamente, sem TestClient, usando as fixtures
`db_session`, `admin_user` e `client_user` de `conftest.py`.
"""

import pytest
from fastapi import HTTPException

from app.core.security import verify_password
from app.models.usuario import Usuario
from app.schemas.auth import UserCreate
from app.services.auth_service import authenticate_user, register_user

NOVO_EMAIL = "novo@hotel.com"
NOVA_SENHA = "senha123"

# (nome da fixture do conftest, senha em texto plano usada ao cria-la)
USUARIOS_EXISTENTES = [
    ("admin_user", "admin123"),
    ("client_user", "cliente123"),
]


def _novo_usuario(email=NOVO_EMAIL, senha=NOVA_SENHA, nome="Novo Usuario"):
    return UserCreate(nome=nome, email=email, senha=senha)


class TestRegisterUser:
    def test_registro_com_sucesso_persiste_usuario(self, db_session):
        usuario = register_user(db_session, _novo_usuario())

        assert usuario.id is not None
        assert usuario.nome == "Novo Usuario"
        assert usuario.email == NOVO_EMAIL
        persistido = db_session.get(Usuario, usuario.id)
        assert persistido is not None
        assert persistido.email == NOVO_EMAIL

    def test_registro_nunca_concede_admin(self, db_session):
        usuario = register_user(db_session, _novo_usuario())
        assert usuario.is_admin is False

    @pytest.mark.parametrize("senha", ["senha123", "S3nh@F0rte!#", "senha-com-çãoü"])
    def test_senha_e_armazenada_como_hash_verificavel(self, db_session, senha):
        usuario = register_user(db_session, _novo_usuario(senha=senha))

        assert usuario.senha_hash != senha
        assert usuario.senha_hash.startswith("$2b$")
        assert verify_password(senha, usuario.senha_hash) is True
        assert verify_password(senha + "x", usuario.senha_hash) is False

    @pytest.mark.parametrize("fixture_name, _senha", USUARIOS_EXISTENTES)
    def test_email_duplicado_lanca_409(self, db_session, request, fixture_name, _senha):
        existente, _token = request.getfixturevalue(fixture_name)
        total_antes = db_session.query(Usuario).count()

        with pytest.raises(HTTPException) as exc:
            register_user(db_session, _novo_usuario(email=existente.email))

        assert exc.value.status_code == 409
        assert exc.value.detail == "Email ja cadastrado no sistema"
        assert db_session.query(Usuario).count() == total_antes

    def test_registro_duplo_pelo_service_e_rejeitado(self, db_session):
        primeiro = register_user(db_session, _novo_usuario())

        with pytest.raises(HTTPException) as exc:
            register_user(db_session, _novo_usuario(nome="Outro Nome", senha="xyz"))

        assert exc.value.status_code == 409
        assert db_session.query(Usuario).filter_by(email=NOVO_EMAIL).count() == 1
        assert db_session.get(Usuario, primeiro.id).nome == "Novo Usuario"

    def test_emails_diferentes_geram_usuarios_distintos(self, db_session):
        a = register_user(db_session, _novo_usuario(email="a@hotel.com"))
        b = register_user(db_session, _novo_usuario(email="b@hotel.com"))

        assert a.id != b.id
        assert db_session.query(Usuario).count() == 2


class TestAuthenticateUser:
    @pytest.mark.parametrize("fixture_name, senha", USUARIOS_EXISTENTES)
    def test_credenciais_corretas_devolvem_usuario(
        self, db_session, request, fixture_name, senha
    ):
        esperado, _token = request.getfixturevalue(fixture_name)

        usuario = authenticate_user(db_session, esperado.email, senha)

        assert usuario is not None
        assert usuario.id == esperado.id
        assert usuario.is_admin is esperado.is_admin

    @pytest.mark.parametrize(
        "senha_errada", ["Admin123", "admin1234", "admin12", "", "cliente123"]
    )
    def test_senha_errada_devolve_none(self, db_session, admin_user, senha_errada):
        usuario, _token = admin_user
        assert authenticate_user(db_session, usuario.email, senha_errada) is None

    @pytest.mark.parametrize(
        "email_inexistente", ["naoexiste@hotel.com", "admin@test.co", ""]
    )
    def test_email_inexistente_devolve_none(
        self, db_session, admin_user, email_inexistente
    ):
        assert authenticate_user(db_session, email_inexistente, "admin123") is None

    def test_banco_vazio_devolve_none(self, db_session):
        assert authenticate_user(db_session, NOVO_EMAIL, NOVA_SENHA) is None

    @pytest.mark.parametrize(
        "senha_informada, autentica", [(NOVA_SENHA, True), ("outra", False)]
    )
    def test_usuario_registrado_pelo_service(
        self, db_session, senha_informada, autentica
    ):
        registrado = register_user(db_session, _novo_usuario())

        resultado = authenticate_user(db_session, NOVO_EMAIL, senha_informada)

        if autentica:
            assert resultado is not None and resultado.id == registrado.id
        else:
            assert resultado is None
