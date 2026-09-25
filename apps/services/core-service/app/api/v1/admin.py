"""Rotas administrativas — CRUDs protegidos por is_admin.

Gerencia: Cidades, Hoteis, Quartos, Comodidades, Servicos Adicionais, Tarifas de Temporada.
Todas as rotas exigem autenticacao JWT + perfil de administrador.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.core.database import get_db
from app.models.cidade import Cidade
from app.models.comodidade import Comodidade
from app.models.hotel import Hotel
from app.models.quarto import Quarto
from app.models.servico_adicional import ServicoAdicional
from app.models.tarifa_temporada import TarifaTemporada
from app.models.usuario import Usuario
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

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(get_current_admin)])

# ──── CIDADES ───────────────────────────────────────────────────────────────


@router.get("/cidades", response_model=list[CidadeResponse])
def listar_cidades(db: Session = Depends(get_db)):
    return db.query(Cidade).order_by(Cidade.nome).all()


@router.post("/cidades", response_model=CidadeResponse, status_code=201)
def criar_cidade(payload: CidadeCreate, db: Session = Depends(get_db)):
    cidade = Cidade(**payload.model_dump())
    db.add(cidade)
    db.commit()
    db.refresh(cidade)
    return cidade


@router.put("/cidades/{cidade_id}", response_model=CidadeResponse)
def atualizar_cidade(
    cidade_id: int, payload: CidadeUpdate, db: Session = Depends(get_db)
):
    cidade = db.query(Cidade).get(cidade_id)
    if not cidade:
        raise HTTPException(status_code=404, detail="Cidade nao encontrada")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(cidade, key, value)
    db.commit()
    db.refresh(cidade)
    return cidade


@router.delete("/cidades/{cidade_id}", status_code=204)
def excluir_cidade(cidade_id: int, db: Session = Depends(get_db)):
    cidade = db.query(Cidade).get(cidade_id)
    if not cidade:
        raise HTTPException(status_code=404, detail="Cidade nao encontrada")
    db.delete(cidade)
    db.commit()


# ──── COMODIDADES ───────────────────────────────────────────────────────────


@router.get("/comodidades", response_model=list[ComodidadeResponse])
def listar_comodidades(db: Session = Depends(get_db)):
    return db.query(Comodidade).order_by(Comodidade.nome).all()


@router.post("/comodidades", response_model=ComodidadeResponse, status_code=201)
def criar_comodidade(payload: ComodidadeCreate, db: Session = Depends(get_db)):
    comodidade = Comodidade(**payload.model_dump())
    db.add(comodidade)
    db.commit()
    db.refresh(comodidade)
    return comodidade


@router.delete("/comodidades/{comodidade_id}", status_code=204)
def excluir_comodidade(comodidade_id: int, db: Session = Depends(get_db)):
    comod = db.query(Comodidade).get(comodidade_id)
    if not comod:
        raise HTTPException(status_code=404, detail="Comodidade nao encontrada")
    db.delete(comod)
    db.commit()


# ──── HOTEIS ────────────────────────────────────────────────────────────────


@router.get("/hoteis", response_model=list[HotelResponse])
def listar_hoteis_admin(db: Session = Depends(get_db)):
    return db.query(Hotel).order_by(Hotel.nome).all()


@router.post("/hoteis", response_model=HotelResponse, status_code=201)
def criar_hotel(payload: HotelCreate, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude={"comodidade_ids"})
    hotel = Hotel(**data)
    if payload.comodidade_ids:
        comodidades = (
            db.query(Comodidade)
            .filter(Comodidade.id.in_(payload.comodidade_ids))
            .all()
        )
        hotel.comodidades = comodidades
    db.add(hotel)
    db.commit()
    db.refresh(hotel)
    return hotel


@router.put("/hoteis/{hotel_id}", response_model=HotelResponse)
def atualizar_hotel(
    hotel_id: int, payload: HotelUpdate, db: Session = Depends(get_db)
):
    hotel = db.query(Hotel).get(hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel nao encontrado")
    data = payload.model_dump(exclude_unset=True, exclude={"comodidade_ids"})
    for key, value in data.items():
        setattr(hotel, key, value)
    if payload.comodidade_ids is not None:
        comodidades = (
            db.query(Comodidade)
            .filter(Comodidade.id.in_(payload.comodidade_ids))
            .all()
        )
        hotel.comodidades = comodidades
    db.commit()
    db.refresh(hotel)
    return hotel


@router.delete("/hoteis/{hotel_id}", status_code=204)
def excluir_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.query(Hotel).get(hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel nao encontrado")
    db.delete(hotel)
    db.commit()


# ──── QUARTOS ───────────────────────────────────────────────────────────────


@router.get("/quartos", response_model=list[QuartoResponse])
def listar_quartos_admin(hotel_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(Quarto)
    if hotel_id:
        query = query.filter(Quarto.hotel_id == hotel_id)
    return query.all()


@router.post("/quartos", response_model=QuartoResponse, status_code=201)
def criar_quarto(payload: QuartoCreate, db: Session = Depends(get_db)):
    quarto = Quarto(**payload.model_dump())
    db.add(quarto)
    db.commit()
    db.refresh(quarto)
    return quarto


@router.put("/quartos/{quarto_id}", response_model=QuartoResponse)
def atualizar_quarto(
    quarto_id: int, payload: QuartoUpdate, db: Session = Depends(get_db)
):
    quarto = db.query(Quarto).get(quarto_id)
    if not quarto:
        raise HTTPException(status_code=404, detail="Quarto nao encontrado")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(quarto, key, value)
    db.commit()
    db.refresh(quarto)
    return quarto


@router.delete("/quartos/{quarto_id}", status_code=204)
def excluir_quarto(quarto_id: int, db: Session = Depends(get_db)):
    quarto = db.query(Quarto).get(quarto_id)
    if not quarto:
        raise HTTPException(status_code=404, detail="Quarto nao encontrado")
    db.delete(quarto)
    db.commit()


# ──── SERVICOS ADICIONAIS ──────────────────────────────────────────────────


@router.get("/servicos", response_model=list[ServicoResponse])
def listar_servicos(db: Session = Depends(get_db)):
    return db.query(ServicoAdicional).order_by(ServicoAdicional.nome).all()


@router.post("/servicos", response_model=ServicoResponse, status_code=201)
def criar_servico(payload: ServicoCreate, db: Session = Depends(get_db)):
    servico = ServicoAdicional(**payload.model_dump())
    db.add(servico)
    db.commit()
    db.refresh(servico)
    return servico


@router.delete("/servicos/{servico_id}", status_code=204)
def excluir_servico(servico_id: int, db: Session = Depends(get_db)):
    servico = db.query(ServicoAdicional).get(servico_id)
    if not servico:
        raise HTTPException(status_code=404, detail="Servico nao encontrado")
    db.delete(servico)
    db.commit()


# ──── TARIFAS DE TEMPORADA ─────────────────────────────────────────────────


@router.get("/tarifas", response_model=list[TarifaResponse])
def listar_tarifas(db: Session = Depends(get_db)):
    return db.query(TarifaTemporada).order_by(TarifaTemporada.data_inicio).all()


@router.post("/tarifas", response_model=TarifaResponse, status_code=201)
def criar_tarifa(payload: TarifaCreate, db: Session = Depends(get_db)):
    tarifa = TarifaTemporada(**payload.model_dump())
    db.add(tarifa)
    db.commit()
    db.refresh(tarifa)
    return tarifa


@router.delete("/tarifas/{tarifa_id}", status_code=204)
def excluir_tarifa(tarifa_id: int, db: Session = Depends(get_db)):
    tarifa = db.query(TarifaTemporada).get(tarifa_id)
    if not tarifa:
        raise HTTPException(status_code=404, detail="Tarifa nao encontrada")
    db.delete(tarifa)
    db.commit()


# ──── AUDITORIA NOSQL (MONGODB) ───────────────────────────────────────────


@router.get("/logs")
async def listar_logs_auditoria(limite: int = 50):
    """Consulta os últimos eventos de auditoria assíncrona gravados no MongoDB."""
    from motor.motor_asyncio import AsyncIOMotorClient
    from app.core.config import settings

    try:
        mongo_client = AsyncIOMotorClient(settings.MONGODB_URL, serverSelectionTimeoutMS=2000)
        db = mongo_client[settings.MONGODB_DB]
        cursor = db["logs_auditoria"].find({}, {"_id": 0}).sort("timestamp", -1).limit(limite)
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

