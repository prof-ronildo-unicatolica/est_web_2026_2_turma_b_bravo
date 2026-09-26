"""Modelo da entidade Hotel — tabela `hoteis` no PostgreSQL."""

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.comodidade import hotel_comodidade
from app.models.tutorial import Base


class Hotel(Base):
    __tablename__ = "hoteis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    estrelas: Mapped[int] = mapped_column(Integer, nullable=False)  # 1 a 5
    cidade_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("cidades.id", ondelete="CASCADE"), nullable=False
    )
    imagem_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Relacionamentos
    cidade: Mapped["Cidade"] = relationship(back_populates="hoteis")  # noqa: F821
    quartos: Mapped[list["Quarto"]] = relationship(  # noqa: F821
        back_populates="hotel", cascade="all, delete-orphan"
    )
    comodidades: Mapped[list["Comodidade"]] = relationship(  # noqa: F821
        secondary=hotel_comodidade, back_populates="hoteis"
    )
    avaliacoes: Mapped[list["Avaliacao"]] = relationship(  # noqa: F821
        back_populates="hotel", cascade="all, delete-orphan"
    )
    tarifas_temporada: Mapped[list["TarifaTemporada"]] = relationship(  # noqa: F821
        back_populates="hotel", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Hotel(id={self.id}, nome='{self.nome}', estrelas={self.estrelas})>"
