"""Testes de integracao do motor de reservas (/api/v1/reservas).

Recuperados do PR #46 e adaptados ao contrato atual da API. Cobrem:
- Simulacao de preco: diarias, temporada, extras, desconto e servicos
- Validacoes: datas invalidas, quarto inexistente, autenticacao obrigatoria
- Fluxo completo: criar, listar, consultar e cancelar reserva
- Controle de acesso: dono, outro usuario e admin
- Publicacao dos eventos de auditoria (RabbitMQ substituido por stub)
"""

from datetime import date, timedelta
from uuid import uuid4

import pytest

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash
from app.models.cidade import Cidade
from app.models.hotel import Hotel
from app.models.quarto import Quarto
from app.models.servico_adicional import ServicoAdicional
from app.models.tarifa_temporada import TarifaTemporada
from app.models.usuario import Usuario

RESERVAS = f"{settings.API_V1_STR}/reservas"
PRECO_DIARIA = 450.0


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _salvar(db_session, entidade):
    db_session.add(entidade)
    db_session.commit()
    db_session.refresh(entidade)
    return entidade


@pytest.fixture(autouse=True)
def eventos_auditoria(monkeypatch):
    """Substitui o publicador RabbitMQ por um stub que registra os eventos."""
    publicados: list[tuple[str, dict]] = []

    async def _publicar_stub(fila: str, evento: dict):
        publicados.append((fila, evento))

    monkeypatch.setattr("app.api.v1.reservas.publish_event", _publicar_stub)
    return publicados


@pytest.fixture
def quarto(db_session):
    cidade = _salvar(db_session, Cidade(nome="Jericoacoara", estado="CE"))
    hotel = _salvar(
        db_session, Hotel(nome="Pousada Vila Jeri", estrelas=5, cidade_id=cidade.id)
    )
    return _salvar(
        db_session,
        Quarto(
            hotel_id=hotel.id,
            tipo="Suite Master",
            capacidade_adultos=2,
            capacidade_criancas=1,
            preco_diaria=PRECO_DIARIA,
        ),
    )


@pytest.fixture
def outro_usuario(db_session):
    usuario = _salvar(
        db_session,
        Usuario(
            nome="Outro Cliente",
            email="outro@test.com",
            senha_hash=get_password_hash("outro123"),
            is_admin=False,
        ),
    )
    return usuario, create_access_token(subject=usuario.email)


def _periodo(dias_a_frente: int, noites: int) -> tuple[date, date]:
    checkin = date.today() + timedelta(days=dias_a_frente)
    return checkin, checkin + timedelta(days=noites)


def _payload(quarto_id: int, checkin: date, checkout: date, **extras) -> dict:
    return {
        "quarto_id": quarto_id,
        "checkin": checkin.isoformat(),
        "checkout": checkout.isoformat(),
        "num_adultos": 2,
        **extras,
    }


# ──── SIMULACAO DE PRECO ────────────────────────────────────────────────────


def test_simular_preco_calcula_diarias_sem_temporada(client, quarto):
    checkin, checkout = _periodo(10, 3)
    response = client.post(
        f"{RESERVAS}/simular", json=_payload(quarto.id, checkin, checkout)
    )
    assert response.status_code == 200
    corpo = response.json()

    assert corpo["num_diarias"] == 3
    assert corpo["valor_diaria"] == PRECO_DIARIA
    assert corpo["multiplicador_temporada"] == 1.0
    assert corpo["subtotal"] == 1350.0
    assert corpo["extras"] == 0.0
    assert corpo["desconto"] == 0.0
    assert corpo["valor_servicos"] == 0.0
    assert corpo["valor_total"] == 1350.0


def test_simular_preco_aplica_temporada_extras_desconto_e_servicos(
    client, db_session, quarto
):
    checkin, checkout = _periodo(30, 2)
    _salvar(
        db_session,
        TarifaTemporada(
            nome="Reveillon",
            data_inicio=checkin - timedelta(days=1),
            data_fim=checkin + timedelta(days=10),
            multiplicador=1.5,
        ),
    )
    translado = _salvar(db_session, ServicoAdicional(nome="Translado", preco=120.0))

    payload = _payload(
        quarto.id,
        checkin,
        checkout,
        tipo_tarifa="NAO_REEMBOLSAVEL",
        early_checkin=True,
        berco=True,
        servico_ids=[translado.id],
    )
    response = client.post(f"{RESERVAS}/simular", json=payload)
    assert response.status_code == 200
    corpo = response.json()

    # 450 x 2 noites x 1.5 = 1350; early checkin 15% (202.5) + berco 30/dia (60)
    # desconto nao reembolsavel 10% (135); servico 120
    assert corpo["multiplicador_temporada"] == 1.5
    assert corpo["subtotal"] == 1350.0
    assert corpo["extras"] == 262.5
    assert corpo["desconto"] == 135.0
    assert corpo["valor_servicos"] == 120.0
    assert corpo["valor_total"] == 1597.5


def test_simular_preco_com_datas_invalidas_retorna_400(client, quarto):
    checkin, _ = _periodo(10, 1)
    response = client.post(
        f"{RESERVAS}/simular", json=_payload(quarto.id, checkin, checkin)
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Checkout deve ser posterior ao checkin"


def test_simular_preco_quarto_inexistente_retorna_400(client):
    checkin, checkout = _periodo(10, 2)
    response = client.post(
        f"{RESERVAS}/simular", json=_payload(9999, checkin, checkout)
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Quarto nao encontrado"


# ──── CRIACAO DE RESERVA ────────────────────────────────────────────────────


def test_criar_reserva_sem_autenticacao_retorna_401(client, quarto):
    checkin, checkout = _periodo(5, 2)
    response = client.post(RESERVAS, json=_payload(quarto.id, checkin, checkout))
    assert response.status_code == 401


def test_criar_reserva_quarto_inexistente_retorna_404(client, client_user):
    _, token = client_user
    checkin, checkout = _periodo(5, 2)
    response = client.post(
        RESERVAS, json=_payload(9999, checkin, checkout), headers=_auth(token)
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Quarto nao encontrado"


def test_criar_reserva_com_datas_invalidas_retorna_400(client, client_user, quarto):
    _, token = client_user
    checkin, _ = _periodo(5, 1)
    response = client.post(
        RESERVAS,
        json=_payload(quarto.id, checkin, checkin - timedelta(days=1)),
        headers=_auth(token),
    )
    assert response.status_code == 400


# ──── FLUXO COMPLETO: CRIAR, CONSULTAR E CANCELAR ──────────────────────────


def test_criar_consultar_e_cancelar_reserva(
    client, client_user, quarto, eventos_auditoria
):
    usuario, token = client_user
    checkin, checkout = _periodo(10, 3)

    criada = client.post(
        RESERVAS, json=_payload(quarto.id, checkin, checkout), headers=_auth(token)
    )
    assert criada.status_code == 201
    corpo = criada.json()
    assert corpo["status"] == "CONFIRMADA"
    assert corpo["usuario_id"] == usuario.id
    assert corpo["valor_total"] == 1350.0
    reserva_id = corpo["id"]

    minhas = client.get(f"{RESERVAS}/minhas", headers=_auth(token))
    assert minhas.status_code == 200
    assert [r["id"] for r in minhas.json()] == [reserva_id]

    detalhe = client.get(f"{RESERVAS}/{reserva_id}", headers=_auth(token))
    assert detalhe.status_code == 200
    assert detalhe.json()["quarto_id"] == quarto.id

    cancelada = client.post(
        f"{RESERVAS}/{reserva_id}/cancelar",
        json={"motivo": "Imprevisto pessoal"},
        headers=_auth(token),
    )
    assert cancelada.status_code == 200
    assert cancelada.json()["status"] == "CANCELADA"
    assert cancelada.json()["motivo_cancelamento"] == "Imprevisto pessoal"

    # Eventos de auditoria publicados na fila audit.logs
    assert [(fila, ev["evento"]) for fila, ev in eventos_auditoria] == [
        ("audit.logs", "reserva.criada"),
        ("audit.logs", "reserva.cancelada"),
    ]
    assert eventos_auditoria[0][1]["reserva_id"] == reserva_id
    assert eventos_auditoria[1][1]["motivo"] == "Imprevisto pessoal"


def test_cancelar_reserva_ja_cancelada_retorna_400(client, client_user, quarto):
    _, token = client_user
    checkin, checkout = _periodo(10, 2)
    reserva_id = client.post(
        RESERVAS, json=_payload(quarto.id, checkin, checkout), headers=_auth(token)
    ).json()["id"]

    primeira = client.post(
        f"{RESERVAS}/{reserva_id}/cancelar", json={}, headers=_auth(token)
    )
    assert primeira.status_code == 200

    segunda = client.post(
        f"{RESERVAS}/{reserva_id}/cancelar", json={}, headers=_auth(token)
    )
    assert segunda.status_code == 400
    assert segunda.json()["detail"] == "Reserva ja cancelada"


# ──── CONTROLE DE ACESSO ────────────────────────────────────────────────────


def test_reserva_de_outro_usuario_e_bloqueada_mas_visivel_ao_admin(
    client, client_user, outro_usuario, admin_user, quarto
):
    _, token_dono = client_user
    _, token_outro = outro_usuario
    _, token_admin = admin_user
    checkin, checkout = _periodo(10, 2)
    reserva_id = client.post(
        RESERVAS, json=_payload(quarto.id, checkin, checkout), headers=_auth(token_dono)
    ).json()["id"]

    assert (
        client.get(f"{RESERVAS}/{reserva_id}", headers=_auth(token_outro)).status_code
        == 403
    )
    assert (
        client.post(
            f"{RESERVAS}/{reserva_id}/cancelar", json={}, headers=_auth(token_outro)
        ).status_code
        == 403
    )
    assert (
        client.get(f"{RESERVAS}/{reserva_id}", headers=_auth(token_admin)).status_code
        == 200
    )
    assert client.get(f"{RESERVAS}/minhas", headers=_auth(token_outro)).json() == []


def test_reserva_inexistente_retorna_404(client, client_user):
    _, token = client_user
    response = client.get(f"{RESERVAS}/{uuid4()}", headers=_auth(token))
    assert response.status_code == 404
    assert response.json()["detail"] == "Reserva nao encontrada"


def test_reserva_com_id_fora_do_formato_uuid_retorna_422(client, client_user):
    _, token = client_user
    response = client.get(f"{RESERVAS}/nao-e-uuid", headers=_auth(token))
    assert response.status_code == 422
