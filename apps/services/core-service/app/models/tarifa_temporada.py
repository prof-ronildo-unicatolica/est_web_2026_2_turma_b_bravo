"""Modelo da entidade TarifaTemporada — tabela `tarifas_temporada` no PostgreSQL.

Permite aplicar multiplicadores de preco em periodos especificos (alta temporada,
carnaval, reveillon, etc). Se hotel_id for NULL, aplica a toda a rede.
"""

from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.tutorial import Base


class TarifaTemporada(Base):
    __tablename__ = "tarifas_temporada"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # "Alta Temporada", "Carnaval 2027"
    data_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    data_fim: Mapped[date] = mapped_column(Date, nullable=False)
    multiplicador: Mapped[float] = mapped_column(
        Float, nullable=False, default=1.0
    )  # ex: 1.3 = +30%
    hotel_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("hoteis.id", ondelete="CASCADE"), nullable=True
    )

    # Relacionamento
    hotel: Mapped["Hotel | None"] = relationship(  # noqa: F821
        back_populates="tarifas_temporada"
    )

    def __repr__(self) -> str:
        return f"<TarifaTemporada(id={self.id}, nome='{self.nome}', mult={self.multiplicador})>"
