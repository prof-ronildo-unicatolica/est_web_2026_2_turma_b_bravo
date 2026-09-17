"""Servico de precificacao — calcula valor total de uma reserva.

Motor de preco que considera:
- Preco base da diaria do quarto
- Numero de diarias
- Multiplicador de temporada (se aplicavel)
- Opcionais: early checkin (+15%), late checkout (+15%), berco (+R$30/dia)
- Desconto por tarifa nao reembolsavel (-10%)
- Servicos adicionais selecionados
"""

from datetime import date

from sqlalchemy.orm import Session

from app.models.quarto import Quarto
from app.models.servico_adicional import ServicoAdicional
from app.models.tarifa_temporada import TarifaTemporada


def calcular_preco(
    db: Session,
    quarto_id: int,
    checkin: date,
    checkout: date,
    tipo_tarifa: str = "REEMBOLSAVEL",
    early_checkin: bool = False,
    late_checkout: bool = False,
    berco: bool = False,
    servico_ids: list[int] | None = None,
) -> dict:
    """Calcula o preco total da reserva com detalhamento.

    Returns:
        Dict com: valor_diaria, num_diarias, multiplicador_temporada,
        subtotal, descontos, extras, valor_servicos, valor_total.
    """
    quarto = db.query(Quarto).get(quarto_id)
    if not quarto:
        raise ValueError("Quarto nao encontrado")

    num_diarias = (checkout - checkin).days
    if num_diarias <= 0:
        raise ValueError("Checkout deve ser posterior ao checkin")

    # 1. Preco base
    valor_diaria = quarto.preco_diaria

    # 2. Multiplicador de temporada (busca tarifa ativa para o periodo)
    tarifa = (
        db.query(TarifaTemporada)
        .filter(
            TarifaTemporada.data_inicio <= checkin,
            TarifaTemporada.data_fim >= checkin,
            (
                (TarifaTemporada.hotel_id == quarto.hotel_id)
                | (TarifaTemporada.hotel_id.is_(None))
            ),
        )
        .order_by(TarifaTemporada.multiplicador.desc())  # Usa o maior multiplicador
        .first()
    )
    multiplicador = tarifa.multiplicador if tarifa else 1.0

    # 3. Subtotal base
    subtotal = valor_diaria * num_diarias * multiplicador

    # 4. Extras opcionais
    extras = 0.0
    if early_checkin:
        extras += subtotal * 0.15  # +15%
    if late_checkout:
        extras += subtotal * 0.15  # +15%
    if berco:
        extras += 30.0 * num_diarias  # R$30/dia

    # 5. Desconto por tarifa nao reembolsavel
    desconto = 0.0
    if tipo_tarifa == "NAO_REEMBOLSAVEL":
        desconto = subtotal * 0.10  # -10%

    # 6. Servicos adicionais
    valor_servicos = 0.0
    if servico_ids:
        servicos = (
            db.query(ServicoAdicional)
            .filter(ServicoAdicional.id.in_(servico_ids))
            .all()
        )
        valor_servicos = sum(s.preco for s in servicos)

    valor_total = subtotal + extras - desconto + valor_servicos

    return {
        "valor_diaria": round(valor_diaria, 2),
        "num_diarias": num_diarias,
        "multiplicador_temporada": multiplicador,
        "subtotal": round(subtotal, 2),
        "extras": round(extras, 2),
        "desconto": round(desconto, 2),
        "valor_servicos": round(valor_servicos, 2),
        "valor_total": round(valor_total, 2),
    }
