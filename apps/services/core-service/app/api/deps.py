"""Dependencias de autenticacao/autorizacao — VERSAO JWT REAL.

Implementa guards de injecao de dependencia do FastAPI:
- get_db: Sessao transacional do PostgreSQL
- get_current_user: Decodifica JWT e carrega o usuario autenticado
- get_current_admin: Verifica se o usuario possui is_admin=True (RBAC)
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.usuario import Usuario

# Esquema OAuth2 — espera o token Bearer no header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> Usuario:
    """Valida o token JWT e retorna o usuario autenticado.

    Decodifica o JWT, extrai o claim `sub` (email), consulta no banco
    e retorna o modelo Usuario. Lanca HTTP 401 se invalido.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario is None:
        raise credentials_exception

    return usuario


def get_current_admin(
    current_user: Usuario = Depends(get_current_user),
) -> Usuario:
    """Autorizacao RBAC: exige que o usuario seja administrador.

    Lanca HTTP 403 se o usuario autenticado nao possui is_admin=True.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores",
        )
    return current_user
