"""Rotas de autenticacao — Endpoints JWT reais.

Implementa:
- POST /auth/register: Cadastro publico de novos clientes
- POST /auth/login: Login com email/senha, retorna JWT
- GET /auth/me: Perfil do usuario autenticado (rota protegida)
- GET /auth/admin/verificacao: Rota de teste para admin (RBAC)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin, get_current_user
from app.core.database import get_db
from app.core.security import create_access_token
from app.models.usuario import Usuario
from app.schemas.auth import Token, UserCreate, UserLogin, UserResponse
from app.services.auth_service import authenticate_user, register_user

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    """Rota publica para autocadastro de novos clientes."""
    usuario = register_user(db, payload)
    return usuario


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    """Login: valida credenciais e retorna token JWT assinado."""
    usuario = authenticate_user(db, payload.email, payload.senha)
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=usuario.email)
    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: Usuario = Depends(get_current_user)):
    """Rota protegida: retorna o perfil do usuario autenticado."""
    return current_user


@router.get("/admin/verificacao")
def somente_admin(admin: Usuario = Depends(get_current_admin)):
    """Rota administrativa de verificacao (autorizacao RBAC por is_admin)."""
    return {"mensagem": f"Acesso administrativo concedido para {admin.nome}"}
