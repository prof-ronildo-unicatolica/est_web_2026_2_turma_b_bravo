"""Modelo da entidade Reserva — tabela `reservas` no PostgreSQL.

Inclui tabela associativa `reserva_servico` para servicos adicionais (N:M).
Status possiveis: PENDENTE, CONFIRMADA, CANCELADA, CONCLUIDA.
"""

import uuid
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.tutorial import Base

# Tabela Associativa N:M entre Reserva e ServicoAdicional
reserva_servico = Table(
    "reserva_servico",
    Base.metadata,
    Column(
        "reserva_id",
        UUID(as_uuid=True),
        ForeignKey("reservas.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "servico_id",
        Integer,
        ForeignKey("servicos_adicionais.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Reserva(Base):
    __tablename__ = "reservas"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    usuario_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False
    )
    quarto_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("quartos.id", ondelete="CASCADE"), nullable=False
    )

    # Datas da estadia
    checkin: Mapped[date] = mapped_column(Date, nullable=False)
    checkout: Mapped[date] = mapped_column(Date, nullable=False)

    # Hospedes
    num_adultos: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    num_criancas: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    num_bebes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Status do processamento
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="PENDENTE"
    )  # PENDENTE, CONFIRMADA, CANCELADA, CONCLUIDA

    # Opcoes de tarifa
    tipo_tarifa: Mapped[str] = mapped_column(
        String(20), nullable=False, default="REEMBOLSAVEL"
    )  # REEMBOLSAVEL, NAO_REEMBOLSAVEL

    # Opcionais
    early_checkin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    late_checkout: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    berco: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Valor calculado
    valor_total: Mapped[float] = mapped_column(Float, nullable=False)

    # Motivo de cancelamento
    motivo_cancelamento: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    # Relacionamentos
    usuario: Mapped["Usuario"] = relationship(back_populates="reservas")  # noqa: F821
    quarto: Mapped["Quarto"] = relationship(back_populates="reservas")  # noqa: F821
    servicos: Mapped[list["ServicoAdicional"]] = relationship(  # noqa: F821
        secondary=reserva_servico
    )
    avaliacao: Mapped["Avaliacao | None"] = relationship(  # noqa: F821
        back_populates="reserva", uselist=False
    )

    def __repr__(self) -> str:
        return f"<Reserva(id={self.id}, status='{self.status}', valor={self.valor_total})>"
