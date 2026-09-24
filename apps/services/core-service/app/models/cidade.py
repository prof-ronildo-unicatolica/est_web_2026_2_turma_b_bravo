"""Modelo da entidade Cidade — tabela `cidades` no PostgreSQL."""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.tutorial import Base


class Cidade(Base):
    __tablename__ = "cidades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    estado: Mapped[str] = mapped_column(String(2), nullable=False)  # UF: CE, SP, RJ...

    # Relacionamentos
    hoteis: Mapped[list["Hotel"]] = relationship(  # noqa: F821
        back_populates="cidade", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Cidade(id={self.id}, nome='{self.nome}', estado='{self.estado}')>"
