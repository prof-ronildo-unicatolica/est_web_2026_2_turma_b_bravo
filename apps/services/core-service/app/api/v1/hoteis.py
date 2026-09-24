"""Rotas publicas de hoteis — busca, listagem e detalhes.

Endpoints acessiveis sem autenticacao (exceto onde indicado).
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.models.avaliacao import Avaliacao
from app.models.hotel import Hotel
from app.models.quarto import Quarto
from app.schemas.hotelaria import (
    ComodidadeResponse,
    CidadeResponse,
    HotelDetailResponse,
    HotelListResponse,
    QuartoResponse,
    AvaliacaoResponse,
    ServicoResponse,
    TarifaResponse,
)
from app.models.servico_adicional import ServicoAdicional
from app.models.tarifa_temporada import TarifaTemporada

router = APIRouter(prefix="/hoteis", tags=["Hotéis (público)"])


@router.get("", response_model=list[HotelListResponse])
def listar_hoteis(
    cidade_id: int | None = None,
    estrelas: int | None = None,
    nome: str | None = None,
    db: Session = Depends(get_db),
):
    """Busca publica de hoteis com filtros opcionais."""
    query = (
        db.query(Hotel)
        .options(joinedload(Hotel.cidade), joinedload(Hotel.comodidades))
    )

    if cidade_id:
        query = query.filter(Hotel.cidade_id == cidade_id)
    if estrelas:
        query = query.filter(Hotel.estrelas >= estrelas)
    if nome:
        query = query.filter(Hotel.nome.ilike(f"%{nome}%"))

    hoteis = query.order_by(Hotel.estrelas.desc()).all()

    # Calcular media de avaliacoes para cada hotel
    result = []
    for hotel in hoteis:
        avg_nota = (
            db.query(func.avg(Avaliacao.nota))
            .filter(Avaliacao.hotel_id == hotel.id)
            .scalar()
        )
        total_avals = (
            db.query(func.count(Avaliacao.id))
            .filter(Avaliacao.hotel_id == hotel.id)
            .scalar()
        )
        hotel_data = HotelListResponse(
            id=hotel.id,
            nome=hotel.nome,
            descricao=hotel.descricao,
            estrelas=hotel.estrelas,
            imagem_url=hotel.imagem_url,
            cidade=CidadeResponse.model_validate(hotel.cidade),
            comodidades=[
                ComodidadeResponse.model_validate(c) for c in hotel.comodidades
            ],
            media_avaliacoes=round(float(avg_nota), 1) if avg_nota else None,
            total_avaliacoes=total_avals or 0,
        )
        result.append(hotel_data)

    return result


@router.get("/{hotel_id}", response_model=HotelDetailResponse)
def detalhe_hotel(hotel_id: int, db: Session = Depends(get_db)):
    """Detalhes completos de um hotel: quartos, comodidades, avaliacoes."""
    hotel = (
        db.query(Hotel)
        .options(
            joinedload(Hotel.cidade),
            joinedload(Hotel.comodidades),
            joinedload(Hotel.quartos),
            joinedload(Hotel.avaliacoes).joinedload(Avaliacao.usuario),
        )
        .filter(Hotel.id == hotel_id)
        .first()
    )

    if not hotel:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Hotel nao encontrado")

    avg_nota = (
        db.query(func.avg(Avaliacao.nota))
        .filter(Avaliacao.hotel_id == hotel.id)
        .scalar()
    )
    total_avals = (
        db.query(func.count(Avaliacao.id))
        .filter(Avaliacao.hotel_id == hotel.id)
        .scalar()
    )

    avaliacoes_response = []
    for av in hotel.avaliacoes:
        avaliacoes_response.append(
            AvaliacaoResponse(
                id=av.id,
                usuario_id=av.usuario_id,
                hotel_id=av.hotel_id,
                reserva_id=av.reserva_id,
                nota=av.nota,
                comentario=av.comentario,
                created_at=av.created_at,
                nome_usuario=av.usuario.nome if av.usuario else None,
            )
        )

    return HotelDetailResponse(
        id=hotel.id,
        nome=hotel.nome,
        descricao=hotel.descricao,
        estrelas=hotel.estrelas,
        imagem_url=hotel.imagem_url,
        cidade=CidadeResponse.model_validate(hotel.cidade),
        comodidades=[
            ComodidadeResponse.model_validate(c) for c in hotel.comodidades
        ],
        quartos=[QuartoResponse.model_validate(q) for q in hotel.quartos],
        avaliacoes=avaliacoes_response,
        media_avaliacoes=round(float(avg_nota), 1) if avg_nota else None,
        total_avaliacoes=total_avals or 0,
    )


@router.get("/{hotel_id}/quartos", response_model=list[QuartoResponse])
def listar_quartos_hotel(hotel_id: int, db: Session = Depends(get_db)):
    """Lista quartos disponiveis de um hotel."""
    return db.query(Quarto).filter(Quarto.hotel_id == hotel_id).all()


# ──── ENDPOINTS AUXILIARES (publicos) ────────────────────────────────────────

@router.get("/auxiliar/servicos", response_model=list[ServicoResponse], tags=["Auxiliar"])
def listar_servicos_publico(db: Session = Depends(get_db)):
    """Lista servicos adicionais disponiveis (para o checkout)."""
    return db.query(ServicoAdicional).order_by(ServicoAdicional.nome).all()


@router.get("/auxiliar/tarifas", response_model=list[TarifaResponse], tags=["Auxiliar"])
def listar_tarifas_publico(db: Session = Depends(get_db)):
    """Lista tarifas de temporada ativas."""
    from datetime import date
    hoje = date.today()
    return (
        db.query(TarifaTemporada)
        .filter(TarifaTemporada.data_fim >= hoje)
        .order_by(TarifaTemporada.data_inicio)
        .all()
    )
