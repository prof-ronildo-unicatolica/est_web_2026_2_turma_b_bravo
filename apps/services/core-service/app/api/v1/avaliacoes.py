"""Rotas de avaliacoes — avaliacao de estadias concluidas.

Endpoints:
- POST /avaliacoes: Avaliar uma estadia (nota 1-5 + comentario)
- GET /avaliacoes/hotel/{hotel_id}: Listar avaliacoes de um hotel
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.avaliacao import Avaliacao
from app.models.reserva import Reserva
from app.models.usuario import Usuario
from app.schemas.hotelaria import AvaliacaoCreate, AvaliacaoResponse

router = APIRouter(prefix="/avaliacoes", tags=["Avaliações"])


@router.post("", response_model=AvaliacaoResponse, status_code=201)
def criar_avaliacao(
    payload: AvaliacaoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Cria uma avaliacao para uma reserva concluida do usuario."""
    # Validar reserva
    reserva = db.query(Reserva).filter(Reserva.id == payload.reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva nao encontrada")
    if reserva.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="Voce so pode avaliar suas proprias reservas")
    if reserva.status not in ("CONFIRMADA", "CONCLUIDA"):
        raise HTTPException(status_code=400, detail="Reserva deve estar confirmada ou concluida para avaliar")

    # Validar nota
    if payload.nota < 1 or payload.nota > 5:
        raise HTTPException(status_code=400, detail="Nota deve ser entre 1 e 5")

    # Verificar se ja avaliou
    existing = db.query(Avaliacao).filter(Avaliacao.reserva_id == payload.reserva_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Esta reserva ja foi avaliada")

    # Obter hotel_id via quarto
    hotel_id = reserva.quarto.hotel_id if reserva.quarto else None
    if not hotel_id:
        raise HTTPException(status_code=400, detail="Quarto da reserva nao possui hotel associado")

    avaliacao = Avaliacao(
        usuario_id=current_user.id,
        hotel_id=hotel_id,
        reserva_id=payload.reserva_id,
        nota=payload.nota,
        comentario=payload.comentario,
    )
    db.add(avaliacao)
    db.commit()
    db.refresh(avaliacao)

    return AvaliacaoResponse(
        id=avaliacao.id,
        usuario_id=avaliacao.usuario_id,
        hotel_id=avaliacao.hotel_id,
        reserva_id=avaliacao.reserva_id,
        nota=avaliacao.nota,
        comentario=avaliacao.comentario,
        created_at=avaliacao.created_at,
        nome_usuario=current_user.nome,
    )


@router.get("/hotel/{hotel_id}", response_model=list[AvaliacaoResponse])
def listar_avaliacoes_hotel(hotel_id: int, db: Session = Depends(get_db)):
    """Lista todas as avaliacoes de um hotel (publico)."""
    avaliacoes = (
        db.query(Avaliacao)
        .filter(Avaliacao.hotel_id == hotel_id)
        .order_by(Avaliacao.created_at.desc())
        .all()
    )
    result = []
    for av in avaliacoes:
        usuario = db.query(Usuario).get(av.usuario_id)
        result.append(
            AvaliacaoResponse(
                id=av.id,
                usuario_id=av.usuario_id,
                hotel_id=av.hotel_id,
                reserva_id=av.reserva_id,
                nota=av.nota,
                comentario=av.comentario,
                created_at=av.created_at,
                nome_usuario=usuario.nome if usuario else None,
            )
        )
    return result
