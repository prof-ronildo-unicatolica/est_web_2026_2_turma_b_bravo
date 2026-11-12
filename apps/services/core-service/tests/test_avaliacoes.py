"""Testes de integracao da API de avaliacoes (/api/v1/avaliacoes).

Cobrem:
- Criacao: caminho feliz, comentario opcional e limites da nota (1 a 5)
- Validacoes: autenticacao, reserva inexistente, reserva de outro usuario,
  status nao avaliavel e avaliacao duplicada
- Listagem publica por hotel: ordenacao, isolamento entre hoteis e nome do autor
- Reflexo da avaliacao na media e no total exibidos no catalogo de hoteis
"""

from datetime import date, datetime, timedelta
from uuid import uuid4

import pytest

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash
from app.models.avaliacao import Avaliacao
from app.models.cidade import Cidade
from app.models.hotel import Hotel
from app.models.quarto import Quarto
from app.models.reserva import Reserva
from app.models.usuario import Usuario

AVALIACOES = f"{settings.API_V1_STR}/avaliacoes"
HOTEIS = f"{settings.API_V1_STR}/hoteis"


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _salvar(db_session, entidade):
    db_session.add(entidade)
    db_session.commit()
    db_session.refresh(entidade)
    return entidade


def _criar_quarto(db_session, cidade: Cidade, nome_hotel: str) -> Quarto:
    hotel = _salvar(
        db_session, Hotel(nome=nome_hotel, estrelas=4, cidade_id=cidade.id)
    )
    return _salvar(
        db_session,
        Quarto(
            hotel_id=hotel.id,
            tipo="Suite Standard",
            capacidade_adultos=2,
            capacidade_criancas=1,
            preco_diaria=300.0,
        ),
    )


def _criar_reserva(
    db_session, usuario: Usuario, quarto: Quarto, status: str = "CONCLUIDA"
) -> Reserva:
    checkin = date.today() - timedelta(days=10)
    return _salvar(
        db_session,
        Reserva(
            usuario_id=usuario.id,
            quarto_id=quarto.id,
            checkin=checkin,
            checkout=checkin + timedelta(days=3),
            num_adultos=2,
            status=status,
            valor_total=900.0,
        ),
    )


@pytest.fixture
def cidade(db_session):
    return _salvar(db_session, Cidade(nome="Guaramiranga", estado="CE"))


@pytest.fixture
def quarto(db_session, cidade):
    return _criar_quarto(db_session, cidade, "Hotel Serra Verde")


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


# ──── CRIACAO ───────────────────────────────────────────────────────────────


def test_criar_avaliacao_de_reserva_concluida(client, db_session, client_user, quarto):
    usuario, token = client_user
    reserva = _criar_reserva(db_session, usuario, quarto)

    resposta = client.post(
        AVALIACOES,
        json={
            "reserva_id": str(reserva.id),
            "nota": 5,
            "comentario": "Estadia excelente",
        },
        headers=_auth(token),
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["reserva_id"] == str(reserva.id)
    assert corpo["hotel_id"] == quarto.hotel_id
    assert corpo["usuario_id"] == usuario.id
    assert corpo["nota"] == 5
    assert corpo["comentario"] == "Estadia excelente"
    assert corpo["nome_usuario"] == usuario.nome
    assert corpo["created_at"]

    salva = db_session.query(Avaliacao).filter_by(reserva_id=reserva.id).one()
    assert salva.id == corpo["id"]
    assert salva.hotel_id == quarto.hotel_id


def test_criar_avaliacao_de_reserva_confirmada_sem_comentario(
    client, db_session, client_user, quarto
):
    usuario, token = client_user
    reserva = _criar_reserva(db_session, usuario, quarto, status="CONFIRMADA")

    resposta = client.post(
        AVALIACOES,
        json={"reserva_id": str(reserva.id), "nota": 3},
        headers=_auth(token),
    )

    assert resposta.status_code == 201
    assert resposta.json()["comentario"] is None


@pytest.mark.parametrize("nota", [1, 5])
def test_nota_nos_limites_e_aceita(client, db_session, client_user, quarto, nota):
    usuario, token = client_user
    reserva = _criar_reserva(db_session, usuario, quarto)

    resposta = client.post(
        AVALIACOES,
        json={"reserva_id": str(reserva.id), "nota": nota},
        headers=_auth(token),
    )

    assert resposta.status_code == 201
    assert resposta.json()["nota"] == nota


@pytest.mark.parametrize("nota", [-1, 0, 6])
def test_nota_fora_do_intervalo_retorna_400(
    client, db_session, client_user, quarto, nota
):
    usuario, token = client_user
    reserva = _criar_reserva(db_session, usuario, quarto)

    resposta = client.post(
        AVALIACOES,
        json={"reserva_id": str(reserva.id), "nota": nota},
        headers=_auth(token),
    )

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == "Nota deve ser entre 1 e 5"
    assert db_session.query(Avaliacao).count() == 0


# ──── VALIDACOES ────────────────────────────────────────────────────────────


def test_criar_avaliacao_sem_token_retorna_401(client, db_session, client_user, quarto):
    usuario, _ = client_user
    reserva = _criar_reserva(db_session, usuario, quarto)

    resposta = client.post(AVALIACOES, json={"reserva_id": str(reserva.id), "nota": 4})

    assert resposta.status_code == 401
    assert db_session.query(Avaliacao).count() == 0


def test_criar_avaliacao_de_reserva_inexistente_retorna_404(client, client_user):
    _, token = client_user

    resposta = client.post(
        AVALIACOES,
        json={"reserva_id": str(uuid4()), "nota": 4},
        headers=_auth(token),
    )

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Reserva nao encontrada"


def test_criar_avaliacao_com_reserva_id_malformado_retorna_422(client, client_user):
    _, token = client_user

    resposta = client.post(
        AVALIACOES,
        json={"reserva_id": "nao-e-um-uuid", "nota": 4},
        headers=_auth(token),
    )

    assert resposta.status_code == 422


def test_avaliar_reserva_de_outro_usuario_retorna_403(
    client, db_session, client_user, outro_usuario, quarto
):
    dono, _ = client_user
    _, token_do_outro = outro_usuario
    reserva = _criar_reserva(db_session, dono, quarto)

    resposta = client.post(
        AVALIACOES,
        json={"reserva_id": str(reserva.id), "nota": 1},
        headers=_auth(token_do_outro),
    )

    assert resposta.status_code == 403
    assert db_session.query(Avaliacao).count() == 0


@pytest.mark.parametrize("status", ["PENDENTE", "CANCELADA"])
def test_avaliar_reserva_em_status_nao_avaliavel_retorna_400(
    client, db_session, client_user, quarto, status
):
    usuario, token = client_user
    reserva = _criar_reserva(db_session, usuario, quarto, status=status)

    resposta = client.post(
        AVALIACOES,
        json={"reserva_id": str(reserva.id), "nota": 4},
        headers=_auth(token),
    )

    assert resposta.status_code == 400
    assert "confirmada ou concluida" in resposta.json()["detail"]
    assert db_session.query(Avaliacao).count() == 0


def test_avaliar_a_mesma_reserva_duas_vezes_retorna_409(
    client, db_session, client_user, quarto
):
    usuario, token = client_user
    reserva = _criar_reserva(db_session, usuario, quarto)
    payload = {"reserva_id": str(reserva.id), "nota": 4, "comentario": "Bom"}

    primeira = client.post(AVALIACOES, json=payload, headers=_auth(token))
    segunda = client.post(
        AVALIACOES, json={**payload, "nota": 1}, headers=_auth(token)
    )

    assert primeira.status_code == 201
    assert segunda.status_code == 409
    salva = db_session.query(Avaliacao).one()
    assert salva.nota == 4


# ──── LISTAGEM PUBLICA ──────────────────────────────────────────────────────


def test_listar_avaliacoes_de_hotel_sem_avaliacoes_retorna_lista_vazia(client, quarto):
    resposta = client.get(f"{AVALIACOES}/hotel/{quarto.hotel_id}")

    assert resposta.status_code == 200
    assert resposta.json() == []


def test_listagem_e_publica_ordenada_e_restrita_ao_hotel(
    client, db_session, client_user, outro_usuario, cidade, quarto
):
    usuario, _ = client_user
    outro, _ = outro_usuario
    quarto_de_outro_hotel = _criar_quarto(db_session, cidade, "Pousada do Vale")
    agora = datetime(2026, 11, 1, 12, 0, 0)

    def _avaliar(autor, quarto_avaliado, nota, criada_em):
        reserva = _criar_reserva(db_session, autor, quarto_avaliado)
        _salvar(
            db_session,
            Avaliacao(
                usuario_id=autor.id,
                hotel_id=quarto_avaliado.hotel_id,
                reserva_id=reserva.id,
                nota=nota,
                comentario=f"nota {nota}",
                created_at=criada_em,
            ),
        )

    _avaliar(usuario, quarto, 2, agora - timedelta(days=2))
    _avaliar(outro, quarto, 5, agora)
    _avaliar(usuario, quarto_de_outro_hotel, 1, agora - timedelta(days=1))

    # Sem cabecalho de autenticacao: a listagem e publica
    resposta = client.get(f"{AVALIACOES}/hotel/{quarto.hotel_id}")

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert [av["nota"] for av in corpo] == [5, 2]  # mais recente primeiro
    assert [av["nome_usuario"] for av in corpo] == [outro.nome, usuario.nome]
    assert {av["hotel_id"] for av in corpo} == {quarto.hotel_id}


# ──── REFLEXO NO CATALOGO ───────────────────────────────────────────────────


def test_avaliacoes_atualizam_media_e_total_no_catalogo(
    client, db_session, client_user, outro_usuario, quarto
):
    usuario, token = client_user
    outro, token_do_outro = outro_usuario
    reserva_a = _criar_reserva(db_session, usuario, quarto)
    reserva_b = _criar_reserva(db_session, outro, quarto)

    antes = client.get(f"{HOTEIS}/{quarto.hotel_id}").json()
    assert antes["total_avaliacoes"] == 0
    assert antes["media_avaliacoes"] is None

    for reserva, nota, tkn in ((reserva_a, 5, token), (reserva_b, 4, token_do_outro)):
        resposta = client.post(
            AVALIACOES,
            json={"reserva_id": str(reserva.id), "nota": nota},
            headers=_auth(tkn),
        )
        assert resposta.status_code == 201

    detalhe = client.get(f"{HOTEIS}/{quarto.hotel_id}").json()
    assert detalhe["total_avaliacoes"] == 2
    assert detalhe["media_avaliacoes"] == 4.5
    assert len(detalhe["avaliacoes"]) == 2

    listagem = client.get(HOTEIS).json()
    hotel_listado = next(h for h in listagem if h["id"] == quarto.hotel_id)
    assert hotel_listado["total_avaliacoes"] == 2
    assert hotel_listado["media_avaliacoes"] == 4.5
