"""Modelo da entidade Avaliacao — tabela `avaliacoes` no PostgreSQL.

Uma avaliacao e vinculada a uma reserva concluida. Cada reserva pode ter
no maximo uma avaliacao (relacao 1:1 via unique constraint).
"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.tutorial import Base


class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False
    )
    hotel_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("hoteis.id", ondelete="CASCADE"), nullable=False
    )
    reserva_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("reservas.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    nota: Mapped[int] = mapped_column(Integer, nullable=False)  # 1 a 5
    comentario: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relacionamentos
    usuario: Mapped["Usuario"] = relationship(back_populates="avaliacoes")  # noqa: F821
    hotel: Mapped["Hotel"] = relationship(back_populates="avaliacoes")  # noqa: F821
    reserva: Mapped["Reserva"] = relationship(back_populates="avaliacao")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Avaliacao(id={self.id}, nota={self.nota}, hotel_id={self.hotel_id})>"
