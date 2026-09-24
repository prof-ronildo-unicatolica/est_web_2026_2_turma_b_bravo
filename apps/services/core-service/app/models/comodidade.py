"""Modelo da entidade Comodidade — tabela `comodidades` no PostgreSQL.

Comodidades sao amenidades oferecidas pelos hoteis (Wi-Fi, Piscina, Academia, etc).
A relacao com Hotel e N:M via tabela associativa `hotel_comodidade`.
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.tutorial import Base

# Tabela Associativa N:M entre Hotel e Comodidade
hotel_comodidade = Table(
    "hotel_comodidade",
    Base.metadata,
    Column(
        "hotel_id",
        Integer,
        ForeignKey("hoteis.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "comodidade_id",
        Integer,
        ForeignKey("comodidades.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Comodidade(Base):
    __tablename__ = "comodidades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    icone: Mapped[str] = mapped_column(
        String(50), nullable=False, default="star"
    )  # nome do icone Lucide: wifi, waves, dumbbell, etc.

    # Relacionamento N:M inverso
    hoteis: Mapped[list["Hotel"]] = relationship(  # noqa: F821
        secondary=hotel_comodidade, back_populates="comodidades"
    )

    def __repr__(self) -> str:
        return f"<Comodidade(id={self.id}, nome='{self.nome}')>"
