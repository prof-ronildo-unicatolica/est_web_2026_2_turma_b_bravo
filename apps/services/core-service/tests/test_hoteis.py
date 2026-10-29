"""Testes de integracao do catalogo publico de hoteis (/api/v1/hoteis).

Recuperados do PR #46 e adaptados ao contrato atual da API. Cobrem:
- Listagem publica com filtros (cidade, estrelas, nome) e ordenacao
- Criacao de hotel pelo admin seguida de consulta publica
- Detalhe do hotel com quartos, comodidades e media de avaliacoes
- 404 para hotel inexistente
- Endpoints auxiliares publicos (servicos e tarifas ativas)
"""

from datetime import date, timedelta

import pytest

from app.core.config import settings
from app.models.avaliacao import Avaliacao
from app.models.cidade import Cidade
from app.models.comodidade import Comodidade
from app.models.hotel import Hotel
from app.models.quarto import Quarto
from app.models.reserva import Reserva
from app.models.servico_adicional import ServicoAdicional
from app.models.tarifa_temporada import TarifaTemporada

HOTEIS = f"{settings.API_V1_STR}/hoteis"
ADMIN = f"{settings.API_V1_STR}/admin"


def _salvar(db_session, entidade):
    db_session.add(entidade)
    db_session.commit()
    db_session.refresh(entidade)
    return entidade


@pytest.fixture
def cidades(db_session):
    fortaleza = _salvar(db_session, Cidade(nome="Fortaleza", estado="CE"))
    jeri = _salvar(db_session, Cidade(nome="Jericoacoara", estado="CE"))
    return fortaleza, jeri


@pytest.fixture
def hoteis(db_session, cidades):
    fortaleza, jeri = cidades
    beira_mar = _salvar(
        db_session, Hotel(nome="Hotel Beira-Mar", estrelas=5, cidade_id=fortaleza.id)
    )
    economico = _salvar(
        db_session, Hotel(nome="Hotel Economico", estrelas=2, cidade_id=fortaleza.id)
    )
    pousada = _salvar(
        db_session, Hotel(nome="Pousada Vila Jeri", estrelas=4, cidade_id=jeri.id)
    )
    return beira_mar, economico, pousada


# ──── LISTAGEM PUBLICA ──────────────────────────────────────────────────────


def test_listar_hoteis_vazio(client):
    response = client.get(HOTEIS)
    assert response.status_code == 200
    assert response.json() == []


def test_listar_hoteis_ordena_por_estrelas_e_inclui_cidade(client, hoteis):
    response = client.get(HOTEIS)
    assert response.status_code == 200
    corpo = response.json()

    assert [h["nome"] for h in corpo] == [
        "Hotel Beira-Mar",
        "Pousada Vila Jeri",
        "Hotel Economico",
    ]
    assert corpo[0]["cidade"]["nome"] == "Fortaleza"
    assert corpo[0]["media_avaliacoes"] is None
    assert corpo[0]["total_avaliacoes"] == 0


def test_listar_hoteis_filtra_por_cidade(client, cidades, hoteis):
    _, jeri = cidades
    response = client.get(HOTEIS, params={"cidade_id": jeri.id})
    assert [h["nome"] for h in response.json()] == ["Pousada Vila Jeri"]


def test_listar_hoteis_filtra_por_estrelas_minimas(client, hoteis):
    response = client.get(HOTEIS, params={"estrelas": 4})
    assert [h["nome"] for h in response.json()] == [
        "Hotel Beira-Mar",
        "Pousada Vila Jeri",
    ]


def test_listar_hoteis_filtra_por_nome_parcial(client, hoteis):
    response = client.get(HOTEIS, params={"nome": "pousada"})
    assert [h["nome"] for h in response.json()] == ["Pousada Vila Jeri"]


# ──── CRIACAO PELO ADMIN + CONSULTA PUBLICA ────────────────────────────────


def test_criar_hotel_como_admin_e_consultar_publicamente(
    client, db_session, admin_user, cidades
):
    _, admin_token = admin_user
    fortaleza, _ = cidades
    wifi = _salvar(db_session, Comodidade(nome="Wi-Fi", icone="wifi"))

    payload = {
        "nome": "Hotel Praia de Iracema",
        "descricao": "Hotel a beira-mar",
        "estrelas": 4,
        "cidade_id": fortaleza.id,
        "imagem_url": "https://exemplo.com/iracema.jpg",
        "comodidade_ids": [wifi.id],
    }
    criado = client.post(
        f"{ADMIN}/hoteis",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert criado.status_code == 201
    hotel_id = criado.json()["id"]

    detalhe = client.get(f"{HOTEIS}/{hotel_id}")
    assert detalhe.status_code == 200
    corpo = detalhe.json()
    assert corpo["nome"] == "Hotel Praia de Iracema"
    assert corpo["cidade"]["id"] == fortaleza.id
    assert [c["nome"] for c in corpo["comodidades"]] == ["Wi-Fi"]
    assert corpo["quartos"] == []
    assert corpo["avaliacoes"] == []


# ──── DETALHE ───────────────────────────────────────────────────────────────


def test_detalhe_hotel_inclui_quartos_e_media_de_avaliacoes(
    client, db_session, client_user, hoteis
):
    usuario, _ = client_user
    beira_mar, _, _ = hoteis
    quarto = _salvar(
        db_session, Quarto(hotel_id=beira_mar.id, tipo="Suite", preco_diaria=500.0)
    )
    reserva = _salvar(
        db_session,
        Reserva(
            usuario_id=usuario.id,
            quarto_id=quarto.id,
            checkin=date(2026, 11, 1),
            checkout=date(2026, 11, 3),
            status="CONCLUIDA",
            valor_total=1000.0,
        ),
    )
    _salvar(
        db_session,
        Avaliacao(
            usuario_id=usuario.id,
            hotel_id=beira_mar.id,
            reserva_id=reserva.id,
            nota=4,
            comentario="Otima estadia",
        ),
    )

    response = client.get(f"{HOTEIS}/{beira_mar.id}")
    assert response.status_code == 200
    corpo = response.json()

    assert [q["tipo"] for q in corpo["quartos"]] == ["Suite"]
    assert corpo["media_avaliacoes"] == 4.0
    assert corpo["total_avaliacoes"] == 1
    assert corpo["avaliacoes"][0]["nome_usuario"] == usuario.nome
    assert corpo["avaliacoes"][0]["comentario"] == "Otima estadia"


def test_hotel_nao_encontrado_retorna_404(client):
    response = client.get(f"{HOTEIS}/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Hotel nao encontrado"


def test_listar_quartos_do_hotel(client, db_session, hoteis):
    beira_mar, economico, _ = hoteis
    _salvar(
        db_session, Quarto(hotel_id=beira_mar.id, tipo="Simples", preco_diaria=200.0)
    )
    _salvar(db_session, Quarto(hotel_id=beira_mar.id, tipo="Casal", preco_diaria=300.0))
    _salvar(
        db_session, Quarto(hotel_id=economico.id, tipo="Simples", preco_diaria=90.0)
    )

    response = client.get(f"{HOTEIS}/{beira_mar.id}/quartos")
    assert response.status_code == 200
    assert sorted(q["tipo"] for q in response.json()) == ["Casal", "Simples"]


# ──── ENDPOINTS AUXILIARES PUBLICOS ────────────────────────────────────────


def test_listar_servicos_publico_ordena_por_nome(client, db_session):
    _salvar(db_session, ServicoAdicional(nome="Translado", preco=120.0))
    _salvar(db_session, ServicoAdicional(nome="Cafe da Manha", preco=30.0))

    response = client.get(f"{HOTEIS}/auxiliar/servicos")
    assert response.status_code == 200
    assert [s["nome"] for s in response.json()] == ["Cafe da Manha", "Translado"]


def test_listar_tarifas_publico_retorna_apenas_vigentes(client, db_session):
    hoje = date.today()
    _salvar(
        db_session,
        TarifaTemporada(
            nome="Expirada",
            data_inicio=hoje - timedelta(days=30),
            data_fim=hoje - timedelta(days=1),
            multiplicador=1.2,
        ),
    )
    _salvar(
        db_session,
        TarifaTemporada(
            nome="Alta Temporada",
            data_inicio=hoje + timedelta(days=10),
            data_fim=hoje + timedelta(days=40),
            multiplicador=1.5,
        ),
    )

    response = client.get(f"{HOTEIS}/auxiliar/tarifas")
    assert response.status_code == 200
    assert [t["nome"] for t in response.json()] == ["Alta Temporada"]
