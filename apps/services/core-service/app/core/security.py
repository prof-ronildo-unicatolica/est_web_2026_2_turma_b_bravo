"""Modulo de seguranca — utilitarios de hash de senha e JWT.

Implementa:
- Hash e verificacao de senhas com bcrypt via passlib
- Geracao e decodificacao de tokens JWT com python-jose (HS256)
"""

from datetime import datetime, timedelta
from typing import Any, Union

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# Contexto de hashing de senhas (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Gera o hash bcrypt de uma senha em texto plano."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se uma senha em texto plano corresponde ao hash bcrypt."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta | None = None
) -> str:
    """Cria um token JWT assinado com HS256.

    Args:
        subject: Identificador do usuario (email ou id) que sera o claim `sub`.
        expires_delta: Tempo de expiracao customizado. Se None, usa o padrao da config.

    Returns:
        Token JWT como string.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict | None:
    """Decodifica e valida um token JWT.

    Returns:
        Payload do token como dict, ou None se invalido/expirado.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None
