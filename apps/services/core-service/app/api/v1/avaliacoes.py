"""Rotas de avaliacoes — avaliacao de estadias concluidas.

Endpoints:
- POST /avaliacoes: Avaliar uma estadia (nota 1-5 + comentario)
- GET /avaliacoes/hotel/{hotel_id}: Listar avaliacoes de um hotel
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.avaliacao import Avaliacao
from app.models.reserva import Reserva
from app.models.usuario import Usuario
from app.schemas.hotelaria import AvaliacaoCreate, AvaliacaoResponse

router = APIRouter(prefix="/avaliacoes", tags=["Avaliações"])

# Mensagens de erro centralizadas (evita strings duplicadas)
MSG_RESERVA_NAO_ENCONTRADA = "Reserva nao encontrada"
MSG_RESERVA_DE_OUTRO_USUARIO = "Voce so pode avaliar suas proprias reservas"
MSG_RESERVA_STATUS_INVALIDO = "Reserva deve estar confirmada ou concluida para avaliar"
MSG_NOTA_INVALIDA = "Nota deve ser entre 1 e 5"
MSG_RESERVA_JA_AVALIADA = "Esta reserva ja foi avaliada"
MSG_QUARTO_SEM_HOTEL = "Quarto da reserva nao possui hotel associado"

# Respostas de erro documentadas no OpenAPI (Swagger) para POST /avaliacoes
RESPOSTAS_CRIAR_AVALIACAO = {
    400: {
        "description": (
            "Requisicao invalida: reserva fora de status CONFIRMADA/CONCLUIDA, "
            "nota fora do intervalo 1-5 ou quarto sem hotel associado"
        )
    },
    403: {"description": "A reserva pertence a outro usuario"},
    404: {"description": "Reserva nao encontrada"},
    409: {"description": "A reserva ja foi avaliada"},
}


@router.post(
    "",
    response_model=AvaliacaoResponse,
    status_code=201,
    responses=RESPOSTAS_CRIAR_AVALIACAO,
)
def criar_avaliacao(
    payload: AvaliacaoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    """Cria uma avaliacao para uma reserva concluida do usuario."""
    # Validar reserva
    reserva = db.query(Reserva).filter(Reserva.id == payload.reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail=MSG_RESERVA_NAO_ENCONTRADA)
    if reserva.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail=MSG_RESERVA_DE_OUTRO_USUARIO)
    if reserva.status not in ("CONFIRMADA", "CONCLUIDA"):
        raise HTTPException(status_code=400, detail=MSG_RESERVA_STATUS_INVALIDO)

    # Validar nota
    if payload.nota < 1 or payload.nota > 5:
        raise HTTPException(status_code=400, detail=MSG_NOTA_INVALIDA)

    # Verificar se ja avaliou
    existing = (
        db.query(Avaliacao).filter(Avaliacao.reserva_id == payload.reserva_id).first()
    )
    if existing:
        raise HTTPException(status_code=409, detail=MSG_RESERVA_JA_AVALIADA)

    # Obter hotel_id via quarto
    hotel_id = reserva.quarto.hotel_id if reserva.quarto else None
    if not hotel_id:
        raise HTTPException(status_code=400, detail=MSG_QUARTO_SEM_HOTEL)

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
