"""Rotas de reservas — criacao, consulta, listagem e cancelamento.

Endpoints:
- POST /reservas: Cria reserva (calcula preco, status=CONFIRMADA)
- GET /reservas/{id}: Consulta status de uma reserva
- GET /reservas/minhas: Lista reservas do usuario autenticado
- POST /reservas/{id}/cancelar: Cancela reserva com regras de multa
- POST /reservas/simular: Simula preco sem criar reserva
"""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.rabbitmq import publish_event
from app.models.quarto import Quarto
from app.models.reserva import Reserva
from app.models.servico_adicional import ServicoAdicional
from app.models.usuario import Usuario
from app.schemas.hotelaria import ReservaCancelRequest, ReservaCreate, ReservaResponse
from app.services.pricing_service import calcular_preco

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reservas", tags=["Reservas"])

# Mensagens reutilizadas (evita string literal repetida)
MSG_RESERVA_NAO_ENCONTRADA = "Reserva nao encontrada"
MSG_ACESSO_NEGADO = "Acesso negado"

# Documentacao dos erros no Swagger (so entram os status que a rota realmente lanca)
RESP_400_DADOS_INVALIDOS = {400: {"description": "Datas ou dados invalidos"}}
RESP_404_QUARTO = {404: {"description": "Quarto nao encontrado"}}
RESP_403_ACESSO = {403: {"description": "Acesso negado (nao e o proprietario nem admin)"}}
RESP_404_RESERVA = {404: {"description": "Reserva nao encontrada"}}


# ---------------------------------------------------------------------------
# Funcoes auxiliares
# ---------------------------------------------------------------------------
def _calcular_preco_ou_400(db: Session, payload: ReservaCreate) -> dict:
    """Calcula o preco; converte ValueError do service em HTTP 400."""
    try:
        return calcular_preco(
            db=db,
            quarto_id=payload.quarto_id,
            checkin=payload.checkin,
            checkout=payload.checkout,
            tipo_tarifa=payload.tipo_tarifa,
            early_checkin=payload.early_checkin,
            late_checkout=payload.late_checkout,
            berco=payload.berco,
            servico_ids=payload.servico_ids,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def _buscar_reserva_autorizada(
    db: Session, reserva_id: UUID, current_user: Usuario
) -> Reserva:
    """Busca a reserva e garante que o usuario e o dono ou admin."""
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail=MSG_RESERVA_NAO_ENCONTRADA)
    if reserva.usuario_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail=MSG_ACESSO_NEGADO)
    return reserva


def _validar_cancelavel(reserva: Reserva) -> None:
    """Levanta HTTP 400 se a reserva nao puder mais ser cancelada."""
    if reserva.status == "CANCELADA":
        raise HTTPException(status_code=400, detail="Reserva ja cancelada")
    if reserva.status == "CONCLUIDA":
        raise HTTPException(status_code=400, detail="Reserva ja concluida")


async def _publicar_auditoria(evento: dict) -> None:
    """Publica evento de auditoria; falha no RabbitMQ nao bloqueia a requisicao."""
    try:
        await publish_event("audit.logs", evento)
    except Exception:
        logger.warning("Nao foi possivel publicar evento de auditoria", exc_info=True)


# ---------------------------------------------------------------------------
# Rotas
# ---------------------------------------------------------------------------
@router.post("/simular", responses=RESP_400_DADOS_INVALIDOS)
def simular_preco(
    payload: ReservaCreate,
    db: Session = Depends(get_db),
):
    """Simula o calculo de preco sem criar a reserva (nao exige login)."""
    return _calcular_preco_ou_400(db, payload)


@router.post(
    "",
    response_model=ReservaResponse,
    status_code=201,
    responses={**RESP_400_DADOS_INVALIDOS, **RESP_404_QUARTO},
)
async def criar_reserva(
    payload: ReservaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Cria uma nova reserva. Calcula o preco e publica evento no RabbitMQ."""
    # Validar quarto existe
    quarto = db.query(Quarto).get(payload.quarto_id)
    if not quarto:
        raise HTTPException(status_code=404, detail="Quarto nao encontrado")

    # Calcular preco
    preco = _calcular_preco_ou_400(db, payload)

    # Criar reserva
    reserva = Reserva(
        usuario_id=current_user.id,
        quarto_id=payload.quarto_id,
        checkin=payload.checkin,
        checkout=payload.checkout,
        num_adultos=payload.num_adultos,
        num_criancas=payload.num_criancas,
        num_bebes=payload.num_bebes,
        status="CONFIRMADA",
        tipo_tarifa=payload.tipo_tarifa,
        early_checkin=payload.early_checkin,
        late_checkout=payload.late_checkout,
        berco=payload.berco,
        valor_total=preco["valor_total"],
    )

    # Associar servicos adicionais
    if payload.servico_ids:
        servicos = (
            db.query(ServicoAdicional)
            .filter(ServicoAdicional.id.in_(payload.servico_ids))
            .all()
        )
        reserva.servicos = servicos

    db.add(reserva)
    db.commit()
    db.refresh(reserva)

    # Publicar evento no RabbitMQ para auditoria
    await _publicar_auditoria(
        {
            "evento": "reserva.criada",
            "reserva_id": str(reserva.id),
            "usuario_email": current_user.email,
            "hotel_nome": quarto.hotel.nome if quarto.hotel else "N/A",
            "quarto_tipo": quarto.tipo,
            "valor_total": preco["valor_total"],
            "checkin": str(payload.checkin),
            "checkout": str(payload.checkout),
        }
    )

    return reserva


@router.get("/minhas", response_model=list[ReservaResponse])
def minhas_reservas(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Lista todas as reservas do usuario autenticado."""
    return (
        db.query(Reserva)
        .filter(Reserva.usuario_id == current_user.id)
        .order_by(Reserva.created_at.desc())
        .all()
    )


@router.get(
    "/{reserva_id}",
    response_model=ReservaResponse,
    responses={**RESP_403_ACESSO, **RESP_404_RESERVA},
)
def detalhe_reserva(
    reserva_id: UUID,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Consulta detalhes de uma reserva (so o proprietario ou admin)."""
    return _buscar_reserva_autorizada(db, reserva_id, current_user)


@router.post(
    "/{reserva_id}/cancelar",
    response_model=ReservaResponse,
    responses={
        400: {"description": "Reserva ja cancelada ou ja concluida"},
        **RESP_403_ACESSO,
        **RESP_404_RESERVA,
    },
)
async def cancelar_reserva(
    reserva_id: UUID,
    payload: ReservaCancelRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Cancela uma reserva existente. Aplica regras de multa conforme tipo_tarifa."""
    reserva = _buscar_reserva_autorizada(db, reserva_id, current_user)
    _validar_cancelavel(reserva)

    reserva.status = "CANCELADA"
    reserva.motivo_cancelamento = payload.motivo

    db.commit()
    db.refresh(reserva)

    # Auditoria
    await _publicar_auditoria(
        {
            "evento": "reserva.cancelada",
            "reserva_id": str(reserva.id),
            "usuario_email": current_user.email,
            "motivo": payload.motivo or "Sem motivo informado",
        }
    )

    return reserva
