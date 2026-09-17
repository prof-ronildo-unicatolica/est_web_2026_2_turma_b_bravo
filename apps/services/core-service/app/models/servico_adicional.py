"""Modelo da entidade ServicoAdicional — tabela `servicos_adicionais` no PostgreSQL.

Servicos opcionais que o hospede pode adicionar a reserva (cafe da manha,
translado aeroporto, pacote spa, etc).
"""

from sqlalchemy import Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.tutorial import Base


class ServicoAdicional(Base):
    __tablename__ = "servicos_adicionais"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    preco: Mapped[float] = mapped_column(Float, nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<ServicoAdicional(id={self.id}, nome='{self.nome}', preco={self.preco})>"
