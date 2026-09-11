"""Servico de autenticacao — regras de negocio para registro e login.

Implementa:
- register_user: Cadastro de novo usuario com validacao de email unico
- authenticate_user: Validacao de credenciais e retorno do modelo
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.usuario import Usuario
from app.schemas.auth import UserCreate


def register_user(db: Session, user_in: UserCreate) -> Usuario:
    """Cadastra um novo usuario no sistema.

    Verifica se o email ja existe e retorna HTTP 409 em caso positivo.
    A senha e armazenada como hash bcrypt.
    """
    existing = db.query(Usuario).filter(Usuario.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email ja cadastrado no sistema",
        )

    usuario = Usuario(
        nome=user_in.nome,
        email=user_in.email,
        senha_hash=get_password_hash(user_in.senha),
        is_admin=False,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def authenticate_user(db: Session, email: str, password: str) -> Usuario | None:
    """Valida credenciais de login.

    Busca o usuario pelo email e verifica a senha com bcrypt.
    Retorna o modelo Usuario se valido, None caso contrario.
    """
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return None
    if not verify_password(password, usuario.senha_hash):
        return None
    return usuario
