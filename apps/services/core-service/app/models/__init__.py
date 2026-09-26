"""Registro centralizado de todos os modelos SQLAlchemy.

Este modulo importa e reexporta todos os models para que o Alembic e
outros componentes do sistema consigam descobrir todas as tabelas
automaticamente a partir de `Base.metadata`.
"""

# Base declarativa (definida em tutorial.py para manter compatibilidade)
from app.models.avaliacao import Avaliacao
from app.models.cidade import Cidade
from app.models.comodidade import Comodidade, hotel_comodidade
from app.models.hotel import Hotel
from app.models.quarto import Quarto
from app.models.reserva import Reserva, reserva_servico
from app.models.servico_adicional import ServicoAdicional
from app.models.tarifa_temporada import TarifaTemporada

# Models do tutorial (mantidos para compatibilidade com migracao inicial)
from app.models.tutorial import (
    Base,
    Disciplina,
    Linguagem,
    Professor,
    ProfessorDetail,
    Stack,
    Tecnologia,
)

# Models do dominio hoteleiro
from app.models.usuario import Usuario

__all__ = [
    "Base",
    # Dominio hoteleiro
    "Usuario",
    "Cidade",
    "Hotel",
    "Quarto",
    "Comodidade",
    "hotel_comodidade",
    "TarifaTemporada",
    "ServicoAdicional",
    "Reserva",
    "reserva_servico",
    "Avaliacao",
    # Tutorial (legado)
    "Professor",
    "ProfessorDetail",
    "Disciplina",
    "Stack",
    "Tecnologia",
    "Linguagem",
]
