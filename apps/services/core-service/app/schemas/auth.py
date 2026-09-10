"""Schemas Pydantic para operacoes de autenticacao.

Define os contratos de validacao para registro, login, token e perfil.
"""

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """Schema de entrada para registro de novos usuarios."""

    nome: str
    email: EmailStr
    senha: str


class UserLogin(BaseModel):
    """Schema de entrada para login."""

    email: EmailStr
    senha: str


class Token(BaseModel):
    """Schema de resposta com o token JWT."""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """Schema de resposta com dados publicos do usuario (nunca expoe senha)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: str
    is_admin: bool
