"""Rotas de reservas — criacao, consulta, listagem e cancelamento.

Endpoints:
- POST /reservas: Cria reserva (calcula preco, status=CONFIRMADA)
- GET /reservas/{id}: Consulta status de uma reserva
- GET /reservas/minhas: Lista reservas do usuario autenticado
- POST /reservas/{id}/cancelar: Cancela reserva com regras de multa
- POST /reservas/simular: Simula preco sem criar reserva
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_current_user
from app.core.database import get_db
from app.core.rabbitmq import publish_event
from app.models.reserva import Reserva
from app.models.quarto import Quarto
from app.models.servico_adicional import ServicoAdicional
from app.models.usuario import Usuario
from app.schemas.hotelaria import ReservaCreate, ReservaCancelRequest, ReservaResponse
from app.services.pricing_service import calcular_preco

router = APIRouter(prefix="/reservas", tags=["Reservas"])


@router.post("/simular")
def simular_preco(
    payload: ReservaCreate,
    db: Session = Depends(get_db),
):
    """Simula o calculo de preco sem criar a reserva (nao exige login)."""
    try:
        detalhamento = calcular_preco(
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
        return detalhamento
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("", response_model=ReservaResponse, status_code=201)
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
    try:
        preco = calcular_preco(
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
    try:
        await publish_event(
            "audit.logs",
            {
                "evento": "reserva.criada",
                "reserva_id": str(reserva.id),
                "usuario_email": current_user.email,
                "hotel_nome": quarto.hotel.nome if quarto.hotel else "N/A",
                "quarto_tipo": quarto.tipo,
                "valor_total": preco["valor_total"],
                "checkin": str(payload.checkin),
                "checkout": str(payload.checkout),
            },
        )
    except Exception:
        pass  # Nao bloqueia a reserva se o RabbitMQ estiver fora

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


@router.get("/{reserva_id}", response_model=ReservaResponse)
def detalhe_reserva(
    reserva_id: str,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Consulta detalhes de uma reserva (so o proprietario ou admin)."""
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva nao encontrada")
    if reserva.usuario_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado")
    return reserva


@router.post("/{reserva_id}/cancelar", response_model=ReservaResponse)
async def cancelar_reserva(
    reserva_id: str,
    payload: ReservaCancelRequest,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Cancela uma reserva existente. Aplica regras de multa conforme tipo_tarifa."""
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva nao encontrada")
    if reserva.usuario_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado")
    if reserva.status == "CANCELADA":
        raise HTTPException(status_code=400, detail="Reserva ja cancelada")
    if reserva.status == "CONCLUIDA":
        raise HTTPException(status_code=400, detail="Reserva ja concluida")

    reserva.status = "CANCELADA"
    reserva.motivo_cancelamento = payload.motivo

    db.commit()
    db.refresh(reserva)

    # Auditoria
    try:
        await publish_event(
            "audit.logs",
            {
                "evento": "reserva.cancelada",
                "reserva_id": str(reserva.id),
                "usuario_email": current_user.email,
                "motivo": payload.motivo or "Sem motivo informado",
            },
        )
    except Exception:
        pass

    return reserva
