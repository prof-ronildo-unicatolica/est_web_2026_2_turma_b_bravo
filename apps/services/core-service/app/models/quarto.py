"""Modelo da entidade Quarto — tabela `quartos` no PostgreSQL."""

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.tutorial import Base


class Quarto(Base):
    __tablename__ = "quartos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("hoteis.id", ondelete="CASCADE"), nullable=False
    )
    tipo: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # Simples, Casal Luxo, Familia Premium, Suite Master
    capacidade_adultos: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    capacidade_criancas: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0
    )
    preco_diaria: Mapped[float] = mapped_column(Float, nullable=False)

    # Relacionamentos
    hotel: Mapped["Hotel"] = relationship(back_populates="quartos")  # noqa: F821
    reservas: Mapped[list["Reserva"]] = relationship(  # noqa: F821
        back_populates="quarto", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Quarto(id={self.id}, tipo='{self.tipo}', preco={self.preco_diaria})>"
