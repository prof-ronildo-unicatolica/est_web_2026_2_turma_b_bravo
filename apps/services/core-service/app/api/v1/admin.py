"""Rotas administrativas — CRUDs protegidos por is_admin.

Gerencia: Cidades, Hoteis, Quartos, Comodidades, Servicos Adicionais, Tarifas de Temporada.
Todas as rotas exigem autenticacao JWT + perfil de administrador.

Documentacao de erros (OpenAPI/Swagger):
- Os status 401 e 403 sao herdados por todas as rotas via `RESPOSTAS_ADMIN`,
  pois o router inteiro depende de `get_current_admin`.
- Cada rota declara em `responses` os demais `HTTPException` que pode lancar
  (404 para recurso inexistente na URL, 400 para referencia invalida no corpo).
"""

from typing import TypeVar

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.database import get_db
from app.models import Base
from app.models.cidade import Cidade
from app.models.comodidade import Comodidade
from app.models.hotel import Hotel
from app.models.quarto import Quarto
from app.models.servico_adicional import ServicoAdicional
from app.models.tarifa_temporada import TarifaTemporada
from app.schemas.hotelaria import (
    CidadeCreate,
    CidadeResponse,
    CidadeUpdate,
    ComodidadeCreate,
    ComodidadeResponse,
    HotelCreate,
    HotelResponse,
    HotelUpdate,
    QuartoCreate,
    QuartoResponse,
    QuartoUpdate,
    ServicoCreate,
    ServicoResponse,
    TarifaCreate,
    TarifaResponse,
)

# ──── MENSAGENS DE ERRO (centralizadas para evitar literais repetidos) ─────

MSG_CIDADE_NAO_ENCONTRADA = "Cidade nao encontrada"
MSG_COMODIDADE_NAO_ENCONTRADA = "Comodidade nao encontrada"
MSG_HOTEL_NAO_ENCONTRADO = "Hotel nao encontrado"
MSG_QUARTO_NAO_ENCONTRADO = "Quarto nao encontrado"
MSG_SERVICO_NAO_ENCONTRADO = "Servico nao encontrado"
MSG_TARIFA_NAO_ENCONTRADA = "Tarifa nao encontrada"

MSG_CIDADE_INVALIDA = "cidade_id informado nao corresponde a uma cidade existente"
MSG_HOTEL_INVALIDO = "hotel_id informado nao corresponde a um hotel existente"
MSG_COMODIDADES_INVALIDAS = "comodidade_ids contem comodidades inexistentes"

# ──── RESPOSTAS DOCUMENTADAS NO OPENAPI ────────────────────────────────────

# Herdadas por todas as rotas do router (dependencia get_current_admin).
RESPOSTAS_ADMIN = {
    401: {"description": "Token JWT ausente, invalido ou expirado"},
    403: {"description": "Acesso restrito a administradores"},
}

RESPOSTA_CIDADE_404 = {404: {"description": MSG_CIDADE_NAO_ENCONTRADA}}
RESPOSTA_COMODIDADE_404 = {404: {"description": MSG_COMODIDADE_NAO_ENCONTRADA}}
RESPOSTA_HOTEL_404 = {404: {"description": MSG_HOTEL_NAO_ENCONTRADO}}
RESPOSTA_QUARTO_404 = {404: {"description": MSG_QUARTO_NAO_ENCONTRADO}}
RESPOSTA_SERVICO_404 = {404: {"description": MSG_SERVICO_NAO_ENCONTRADO}}
RESPOSTA_TARIFA_404 = {404: {"description": MSG_TARIFA_NAO_ENCONTRADA}}

RESPOSTA_HOTEL_400 = {
    400: {"description": f"{MSG_CIDADE_INVALIDA}; ou {MSG_COMODIDADES_INVALIDAS}"}
}
RESPOSTA_QUARTO_400 = {400: {"description": MSG_HOTEL_INVALIDO}}
RESPOSTA_TARIFA_400 = {400: {"description": MSG_HOTEL_INVALIDO}}

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(get_current_admin)],
    responses=RESPOSTAS_ADMIN,
)

# ──── FUNCOES AUXILIARES (persistencia e sanitizacao) ──────────────────────

ModeloT = TypeVar("ModeloT", bound=Base)


def _obter_ou_404(
    db: Session, modelo: type[ModeloT], entidade_id: int, mensagem: str
) -> ModeloT:
    """Carrega a entidade pela chave primaria ou lanca HTTP 404."""
    entidade = db.get(modelo, entidade_id)
    if entidade is None:
        raise HTTPException(status_code=404, detail=mensagem)
    return entidade


def _validar_referencia(
    db: Session, modelo: type[Base], entidade_id: int | None, mensagem: str
) -> None:
    """Garante que um id referenciado no corpo da requisicao existe (HTTP 400).

    Ids opcionais (`None`) sao ignorados. Evita violacao de chave estrangeira
    no banco, que resultaria em erro 500 sem mensagem util ao cliente.
    """
    if entidade_id is not None and db.get(modelo, entidade_id) is None:
        raise HTTPException(status_code=400, detail=mensagem)


def _buscar_comodidades(db: Session, comodidade_ids: list[int]) -> list[Comodidade]:
    """Resolve a lista de ids em entidades Comodidade, exigindo que todas existam."""
    ids_unicos = set(comodidade_ids)
    if not ids_unicos:
        return []
    comodidades = db.query(Comodidade).filter(Comodidade.id.in_(ids_unicos)).all()
    if len(comodidades) != len(ids_unicos):
        raise HTTPException(status_code=400, detail=MSG_COMODIDADES_INVALIDAS)
    return comodidades


def _aplicar_campos(entidade: Base, dados: dict) -> None:
    """Copia para a entidade apenas os campos enviados no payload de atualizacao."""
    for campo, valor in dados.items():
        setattr(entidade, campo, valor)


def _persistir(db: Session, entidade: ModeloT) -> ModeloT:
    """Adiciona (quando nova), confirma a transacao e recarrega a entidade."""
    db.add(entidade)
    db.commit()
    db.refresh(entidade)
    return entidade


def _remover(db: Session, entidade: Base) -> None:
    """Exclui a entidade e confirma a transacao."""
    db.delete(entidade)
    db.commit()


# ──── CIDADES ───────────────────────────────────────────────────────────────


@router.get("/cidades", response_model=list[CidadeResponse])
def listar_cidades(db: Session = Depends(get_db)):
    return db.query(Cidade).order_by(Cidade.nome).all()


@router.post("/cidades", response_model=CidadeResponse, status_code=201)
def criar_cidade(payload: CidadeCreate, db: Session = Depends(get_db)):
    return _persistir(db, Cidade(**payload.model_dump()))


@router.put(
    "/cidades/{cidade_id}",
    response_model=CidadeResponse,
    responses=RESPOSTA_CIDADE_404,
)
def atualizar_cidade(
    cidade_id: int, payload: CidadeUpdate, db: Session = Depends(get_db)
):
    cidade = _obter_ou_404(db, Cidade, cidade_id, MSG_CIDADE_NAO_ENCONTRADA)
    _aplicar_campos(cidade, payload.model_dump(exclude_unset=True))
    return _persistir(db, cidade)


@router.delete("/cidades/{cidade_id}", status_code=204, responses=RESPOSTA_CIDADE_404)
def excluir_cidade(cidade_id: int, db: Session = Depends(get_db)):
    cidade = _obter_ou_404(db, Cidade, cidade_id, MSG_CIDADE_NAO_ENCONTRADA)
    _remover(db, cidade)


# ──── COMODIDADES ───────────────────────────────────────────────────────────


@router.get("/comodidades", response_model=list[ComodidadeResponse])
def listar_comodidades(db: Session = Depends(get_db)):
    return db.query(Comodidade).order_by(Comodidade.nome).all()


@router.post("/comodidades", response_model=ComodidadeResponse, status_code=201)
def criar_comodidade(payload: ComodidadeCreate, db: Session = Depends(get_db)):
    return _persistir(db, Comodidade(**payload.model_dump()))


@router.delete(
    "/comodidades/{comodidade_id}",
    status_code=204,
    responses=RESPOSTA_COMODIDADE_404,
)
def excluir_comodidade(comodidade_id: int, db: Session = Depends(get_db)):
    comodidade = _obter_ou_404(
        db, Comodidade, comodidade_id, MSG_COMODIDADE_NAO_ENCONTRADA
    )
    _remover(db, comodidade)


# ──── HOTEIS ────────────────────────────────────────────────────────────────


@router.get("/hoteis", response_model=list[HotelResponse])
def listar_hoteis_admin(db: Session = Depends(get_db)):
    return db.query(Hotel).order_by(Hotel.nome).all()


@router.post(
    "/hoteis",
    response_model=HotelResponse,
    status_code=201,
    responses=RESPOSTA_HOTEL_400,
)
def criar_hotel(payload: HotelCreate, db: Session = Depends(get_db)):
    _validar_referencia(db, Cidade, payload.cidade_id, MSG_CIDADE_INVALIDA)
    hotel = Hotel(**payload.model_dump(exclude={"comodidade_ids"}))
    hotel.comodidades = _buscar_comodidades(db, payload.comodidade_ids)
    return _persistir(db, hotel)


@router.put(
    "/hoteis/{hotel_id}",
    response_model=HotelResponse,
    responses={**RESPOSTA_HOTEL_404, **RESPOSTA_HOTEL_400},
)
def atualizar_hotel(hotel_id: int, payload: HotelUpdate, db: Session = Depends(get_db)):
    hotel = _obter_ou_404(db, Hotel, hotel_id, MSG_HOTEL_NAO_ENCONTRADO)
    _validar_referencia(db, Cidade, payload.cidade_id, MSG_CIDADE_INVALIDA)
    _aplicar_campos(
        hotel, payload.model_dump(exclude_unset=True, exclude={"comodidade_ids"})
    )
    if payload.comodidade_ids is not None:
        hotel.comodidades = _buscar_comodidades(db, payload.comodidade_ids)
    return _persistir(db, hotel)


@router.delete("/hoteis/{hotel_id}", status_code=204, responses=RESPOSTA_HOTEL_404)
def excluir_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = _obter_ou_404(db, Hotel, hotel_id, MSG_HOTEL_NAO_ENCONTRADO)
    _remover(db, hotel)


# ──── QUARTOS ───────────────────────────────────────────────────────────────


@router.get("/quartos", response_model=list[QuartoResponse])
def listar_quartos_admin(hotel_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Quarto)
    if hotel_id:
        query = query.filter(Quarto.hotel_id == hotel_id)
    return query.all()


@router.post(
    "/quartos",
    response_model=QuartoResponse,
    status_code=201,
    responses=RESPOSTA_QUARTO_400,
)
def criar_quarto(payload: QuartoCreate, db: Session = Depends(get_db)):
    _validar_referencia(db, Hotel, payload.hotel_id, MSG_HOTEL_INVALIDO)
    return _persistir(db, Quarto(**payload.model_dump()))


@router.put(
    "/quartos/{quarto_id}",
    response_model=QuartoResponse,
    responses=RESPOSTA_QUARTO_404,
)
def atualizar_quarto(
    quarto_id: int, payload: QuartoUpdate, db: Session = Depends(get_db)
):
    quarto = _obter_ou_404(db, Quarto, quarto_id, MSG_QUARTO_NAO_ENCONTRADO)
    _aplicar_campos(quarto, payload.model_dump(exclude_unset=True))
    return _persistir(db, quarto)


@router.delete("/quartos/{quarto_id}", status_code=204, responses=RESPOSTA_QUARTO_404)
def excluir_quarto(quarto_id: int, db: Session = Depends(get_db)):
    quarto = _obter_ou_404(db, Quarto, quarto_id, MSG_QUARTO_NAO_ENCONTRADO)
    _remover(db, quarto)


# ──── SERVICOS ADICIONAIS ──────────────────────────────────────────────────


@router.get("/servicos", response_model=list[ServicoResponse])
def listar_servicos(db: Session = Depends(get_db)):
    return db.query(ServicoAdicional).order_by(ServicoAdicional.nome).all()


@router.post("/servicos", response_model=ServicoResponse, status_code=201)
def criar_servico(payload: ServicoCreate, db: Session = Depends(get_db)):
    return _persistir(db, ServicoAdicional(**payload.model_dump()))


@router.delete(
    "/servicos/{servico_id}", status_code=204, responses=RESPOSTA_SERVICO_404
)
def excluir_servico(servico_id: int, db: Session = Depends(get_db)):
    servico = _obter_ou_404(
        db, ServicoAdicional, servico_id, MSG_SERVICO_NAO_ENCONTRADO
    )
    _remover(db, servico)


# ──── TARIFAS DE TEMPORADA ─────────────────────────────────────────────────


@router.get("/tarifas", response_model=list[TarifaResponse])
def listar_tarifas(db: Session = Depends(get_db)):
    return db.query(TarifaTemporada).order_by(TarifaTemporada.data_inicio).all()


@router.post(
    "/tarifas",
    response_model=TarifaResponse,
    status_code=201,
    responses=RESPOSTA_TARIFA_400,
)
def criar_tarifa(payload: TarifaCreate, db: Session = Depends(get_db)):
    # hotel_id e opcional: tarifa sem hotel vale para toda a rede.
    _validar_referencia(db, Hotel, payload.hotel_id, MSG_HOTEL_INVALIDO)
    return _persistir(db, TarifaTemporada(**payload.model_dump()))


@router.delete("/tarifas/{tarifa_id}", status_code=204, responses=RESPOSTA_TARIFA_404)
def excluir_tarifa(tarifa_id: int, db: Session = Depends(get_db)):
    tarifa = _obter_ou_404(db, TarifaTemporada, tarifa_id, MSG_TARIFA_NAO_ENCONTRADA)
    _remover(db, tarifa)


# ──── AUDITORIA NOSQL (MONGODB) ───────────────────────────────────────────


@router.get("/logs")
async def listar_logs_auditoria(limite: int = 50):
    """Consulta os últimos eventos de auditoria assíncrona gravados no MongoDB."""
    from motor.motor_asyncio import AsyncIOMotorClient

    from app.core.config import settings

    try:
        mongo_client = AsyncIOMotorClient(
            settings.MONGODB_URL, serverSelectionTimeoutMS=2000
        )
        db = mongo_client[settings.MONGODB_DB]
        cursor = (
            db["logs_auditoria"]
            .find({}, {"_id": 0})
            .sort("timestamp", -1)
            .limit(limite)
        )
        logs = await cursor.to_list(length=limite)
        return logs
    except Exception as e:
        # Fallback gracioso se MongoDB estiver indisponível
        return [
            {
                "evento": "aviso.mongodb_offline",
                "detalhes": f"Não foi possível obter logs do MongoDB: {str(e)}",
                "timestamp": "N/A",
            }
        ]
