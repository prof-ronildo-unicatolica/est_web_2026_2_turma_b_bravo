"""Ponto de entrada da aplicacao FastAPI — StayFlow Core Service.

Registra todos os routers (auth, admin, hoteis, reservas, avaliacoes)
e configura CORS, lifespan e middlewares.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.api.v1.health import router as health_router
from app.api.v1.sobre import router as sobre_router
from app.api.v1.admin import router as admin_router
from app.api.v1.hoteis import router as hoteis_router
from app.api.v1.reservas import router as reservas_router
from app.api.v1.avaliacoes import router as avaliacoes_router
from app.core.config import settings
from app.core.database import get_mongo_db
from app.core.seed_mongo import seed_mongo_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Evento de inicialização: Popular/Semear o MongoDB (resiliente a falhas)
    try:
        mongo_db = get_mongo_db()
        await seed_mongo_users(mongo_db)
    except Exception:
        pass  # MongoDB pode nao estar disponivel em ambiente de teste
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Configuração de CORS para permitir acesso do Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas do tutorial/boilerplate (legado)
app.include_router(health_router, prefix=settings.API_V1_STR)
app.include_router(sobre_router, prefix=settings.API_V1_STR)

# Rotas do StayFlow
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)
app.include_router(hoteis_router, prefix=settings.API_V1_STR)
app.include_router(reservas_router, prefix=settings.API_V1_STR)
app.include_router(avaliacoes_router, prefix=settings.API_V1_STR)


@app.get("/")
def read_root():
    return {
        "sistema": "StayFlow",
        "descricao": "Sistema de Gestão de Rede Hoteleira",
        "versao": "1.0.0",
        "documentacao": "/docs",
    }
