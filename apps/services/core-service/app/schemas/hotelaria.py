"""Schemas Pydantic para entidades do dominio hoteleiro.

Define contratos de validacao para CRUDs de:
Cidade, Hotel, Quarto, Comodidade, ServicoAdicional, TarifaTemporada, Reserva, Avaliacao.
"""

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

# ──── CIDADE ────────────────────────────────────────────────────────────────

class CidadeCreate(BaseModel):
    nome: str
    estado: str  # UF: CE, SP, RJ...


class CidadeUpdate(BaseModel):
    nome: str | None = None
    estado: str | None = None


class CidadeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    estado: str


# ──── COMODIDADE ────────────────────────────────────────────────────────────

class ComodidadeCreate(BaseModel):
    nome: str
    icone: str = "star"


class ComodidadeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    icone: str


# ──── HOTEL ─────────────────────────────────────────────────────────────────

class HotelCreate(BaseModel):
    nome: str
    descricao: str | None = None
    estrelas: int
    cidade_id: int
    imagem_url: str | None = None
    comodidade_ids: list[int] = []


class HotelUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    estrelas: int | None = None
    cidade_id: int | None = None
    imagem_url: str | None = None
    comodidade_ids: list[int] | None = None


class HotelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    descricao: str | None = None
    estrelas: int
    cidade_id: int
    imagem_url: str | None = None


class HotelListResponse(BaseModel):
    """Resposta de hotel para listagem publica (inclui cidade e comodidades)."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    descricao: str | None = None
    estrelas: int
    imagem_url: str | None = None
    cidade: CidadeResponse
    comodidades: list[ComodidadeResponse] = []
    media_avaliacoes: float | None = None
    total_avaliacoes: int = 0


class HotelDetailResponse(HotelListResponse):
    """Resposta detalhada de hotel (inclui quartos e avaliacoes)."""
    quartos: list["QuartoResponse"] = []
    avaliacoes: list["AvaliacaoResponse"] = []


# ──── QUARTO ────────────────────────────────────────────────────────────────

class QuartoCreate(BaseModel):
    hotel_id: int
    tipo: str
    capacidade_adultos: int = 2
    capacidade_criancas: int = 0
    preco_diaria: float


class QuartoUpdate(BaseModel):
    tipo: str | None = None
    capacidade_adultos: int | None = None
    capacidade_criancas: int | None = None
    preco_diaria: float | None = None


class QuartoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    hotel_id: int
    tipo: str
    capacidade_adultos: int
    capacidade_criancas: int
    preco_diaria: float


# ──── SERVICO ADICIONAL ─────────────────────────────────────────────────────

class ServicoCreate(BaseModel):
    nome: str
    preco: float
    descricao: str | None = None


class ServicoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    preco: float
    descricao: str | None = None


# ──── TARIFA TEMPORADA ──────────────────────────────────────────────────────

class TarifaCreate(BaseModel):
    nome: str
    data_inicio: date
    data_fim: date
    multiplicador: float
    hotel_id: int | None = None


class TarifaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    data_inicio: date
    data_fim: date
    multiplicador: float
    hotel_id: int | None = None


# ──── RESERVA ───────────────────────────────────────────────────────────────

class ReservaCreate(BaseModel):
    quarto_id: int
    checkin: date
    checkout: date
    num_adultos: int = 1
    num_criancas: int = 0
    num_bebes: int = 0
    tipo_tarifa: str = "REEMBOLSAVEL"
    early_checkin: bool = False
    late_checkout: bool = False
    berco: bool = False
    servico_ids: list[int] = []


class ReservaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    usuario_id: int
    quarto_id: int
    checkin: date
    checkout: date
    num_adultos: int
    num_criancas: int
    num_bebes: int
    status: str
    tipo_tarifa: str
    early_checkin: bool
    late_checkout: bool
    berco: bool
    valor_total: float
    motivo_cancelamento: str | None = None
    created_at: datetime


class ReservaCancelRequest(BaseModel):
    motivo: str | None = None


# ──── AVALIACAO ─────────────────────────────────────────────────────────────

class AvaliacaoCreate(BaseModel):
    reserva_id: UUID
    nota: int  # 1 a 5
    comentario: str | None = None


class AvaliacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    usuario_id: int
    hotel_id: int
    reserva_id: UUID
    nota: int
    comentario: str | None = None
    created_at: datetime
    nome_usuario: str | None = None


# Resolve forward refs
HotelDetailResponse.model_rebuild()
