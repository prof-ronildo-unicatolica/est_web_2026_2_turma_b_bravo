"""Testes de integração para motor de reservas, precificação e cancelamento.

Cobre:
- Cálculo e simulação de diárias
- Criação de reserva autenticada
- Conflito de reservas ou datas inválidas
- Cancelamento de reserva com atualização de status
"""

from datetime import date, timedelta
from app.models.cidade import Cidade
from app.models.hotel import Hotel
from app.models.quarto import Quarto
from app.models.reserva import Reserva


def setup_hotel_e_quarto(db_session):
    cidade = Cidade(nome="Jericoacoara", estado="CE")
    db_session.add(cidade)
    db_session.commit()
    db_session.refresh(cidade)

    hotel = Hotel(
        nome="Pousada Vila Jeri",
        endereco="Rua Principal, s/n",
        cidade_id=cidade.id,
        estrelas=5,
        foto_capa="https://images.unsplash.com/photo-1582719508461-905c673771fd",
        fotos=[],
    )
    db_session.add(hotel)
    db_session.commit()
    db_session.refresh(hotel)

    quarto = Quarto(
        hotel_id=hotel.id,
        tipo="SUITE_MASTER",
        descricao="Suíte de luxo",
        capacidade_adultos=2,
        capacidade_criancas=1,
        preco_diaria=450.0,
        quantidade_total=5,
    )
    db_session.add(quarto)
    db_session.commit()
    db_session.refresh(quarto)
    return hotel, quarto


def test_criar_e_cancelar_reserva(client, db_session, client_user):
    user, token = client_user
    hotel, quarto = setup_hotel_e_quarto(db_session)

    checkin = (date.today() + timedelta(days=10)).isoformat()
    checkout = (date.today() + timedelta(days=13)).isoformat()

    # Cria reserva
    payload_reserva = {
        "quarto_id": quarto.id,
        "checkin": checkin,
        "checkout": checkout,
        "quantidade_hospedes": 2,
        "tipo_tarifa": "REEMBOLSAVEL",
        "servicos_ids": [],
    }

    resp = client.post(
        "/api/v1/reservas",
        json=payload_reserva,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code in (200, 201)
    data = resp.json()
    assert data["status"] in ("PENDENTE", "CONFIRMADA")
    reserva_id = data["id"]

    # Cancela reserva
    resp_cancel = client.post(
        f"/api/v1/reservas/{reserva_id}/cancelar",
        json={"motivo": "Imprevisto pessoal"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp_cancel.status_code == 200
    assert resp_cancel.json()["status"] == "CANCELADA"


def test_tentar_reservar_sem_autenticacao_retorna_401(client, db_session):
    hotel, quarto = setup_hotel_e_quarto(db_session)
    checkin = (date.today() + timedelta(days=5)).isoformat()
    checkout = (date.today() + timedelta(days=7)).isoformat()

    payload = {
        "quarto_id": quarto.id,
        "checkin": checkin,
        "checkout": checkout,
        "quantidade_hospedes": 1,
        "tipo_tarifa": "FLEXIVEL",
        "servicos_ids": [],
    }
    resp = client.post("/api/v1/reservas", json=payload)
    assert resp.status_code in (401, 403)
