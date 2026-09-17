import uuid
from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# A MESMA Base do restante do projeto. Nao crie outra: uma segunda Base
# significa um segundo registro de metadados, e o Alembic nao enxergaria
# estas tabelas -- em silencio, sem erro.
from app.models.tutorial import Base

class Hotel(Base):
    __tablename__ = "hoteis"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    # Sem unique: "Hotel Central" pode existir em Fortaleza e em Sobral.
    nome: Mapped[str] = mapped_column(String(100), nullable=False)

    # Lado N da relacao: a FK mora AQUI (decisao 3 da issue #9).
    cidade_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("cidades.id", ondelete="CASCADE"), nullable=False
    )

    # Lado N da navegacao: um hotel aponta para UMA cidade.
    cidade: Mapped["Cidade"] = relationship(back_populates="hoteis")