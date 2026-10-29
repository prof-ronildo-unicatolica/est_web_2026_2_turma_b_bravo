"""Testes das rotas administrativas (/api/v1/admin) e do detalhe publico de hotel.

Cobre:
- Protecao do router: 401 sem token e 403 para usuario cliente
- CRUD de cidades e os 404 lancados para recursos inexistentes
- Sanitizacao de referencias no corpo (400) em hoteis, quartos e tarifas
- Presenca dos status de erro documentados no schema OpenAPI (Swagger)
"""

import pytest

from app.core.config import settings
from app.models.cidade import Cidade
from app.models.comodidade import Comodidade
from app.models.hotel import Hotel

ADMIN = f"{settings.API_V1_STR}/admin"
HOTEIS = f"{settings.API_V1_STR}/hoteis"


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(admin_user):
    _, token = admin_user
    return _auth(token)


@pytest.fixture
def cidade(db_session):
    entidade = Cidade(nome="Fortaleza", estado="CE")
    db_session.add(entidade)
    db_session.commit()
    db_session.refresh(entidade)
    return entidade


@pytest.fixture
def comodidade(db_session):
    entidade = Comodidade(nome="Wi-Fi", icone="wifi")
    db_session.add(entidade)
    db_session.commit()
    db_session.refresh(entidade)
    return entidade


@pytest.fixture
def hotel(db_session, cidade):
    entidade = Hotel(nome="Hotel Teste", estrelas=4, cidade_id=cidade.id)
    db_session.add(entidade)
    db_session.commit()
    db_session.refresh(entidade)
    return entidade


# ──── PROTECAO DO ROUTER ────────────────────────────────────────────────────


def test_rotas_admin_exigem_token(client):
    response = client.get(f"{ADMIN}/hoteis")
    assert response.status_code == 401


def test_rotas_admin_bloqueiam_cliente(client, client_user):
    _, token = client_user
    response = client.get(f"{ADMIN}/hoteis", headers=_auth(token))
    assert response.status_code == 403


# ──── CIDADES ───────────────────────────────────────────────────────────────


def test_crud_cidade(client, admin_headers):
    criada = client.post(
        f"{ADMIN}/cidades",
        json={"nome": "Sobral", "estado": "CE"},
        headers=admin_headers,
    )
    assert criada.status_code == 201
    cidade_id = criada.json()["id"]

    atualizada = client.put(
        f"{ADMIN}/cidades/{cidade_id}",
        json={"nome": "Sobral-CE"},
        headers=admin_headers,
    )
    assert atualizada.status_code == 200
    assert atualizada.json() == {"id": cidade_id, "nome": "Sobral-CE", "estado": "CE"}

    listagem = client.get(f"{ADMIN}/cidades", headers=admin_headers)
    assert [c["id"] for c in listagem.json()] == [cidade_id]

    excluida = client.delete(f"{ADMIN}/cidades/{cidade_id}", headers=admin_headers)
    assert excluida.status_code == 204
    assert client.get(f"{ADMIN}/cidades", headers=admin_headers).json() == []


def test_atualizar_cidade_inexistente_retorna_404(client, admin_headers):
    response = client.put(
        f"{ADMIN}/cidades/9999", json={"nome": "Nada"}, headers=admin_headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Cidade nao encontrada"


@pytest.mark.parametrize(
    ("recurso", "mensagem"),
    [
        ("cidades", "Cidade nao encontrada"),
        ("comodidades", "Comodidade nao encontrada"),
        ("hoteis", "Hotel nao encontrado"),
        ("quartos", "Quarto nao encontrado"),
        ("servicos", "Servico nao encontrado"),
        ("tarifas", "Tarifa nao encontrada"),
    ],
)
def test_excluir_recurso_inexistente_retorna_404(
    client, admin_headers, recurso, mensagem
):
    response = client.delete(f"{ADMIN}/{recurso}/9999", headers=admin_headers)
    assert response.status_code == 404
    assert response.json()["detail"] == mensagem


# ──── HOTEIS (sanitizacao de referencias) ──────────────────────────────────


def test_criar_hotel_com_comodidades(
    client, admin_headers, db_session, cidade, comodidade
):
    payload = {
        "nome": "Hotel Praia",
        "estrelas": 5,
        "cidade_id": cidade.id,
        "comodidade_ids": [comodidade.id],
    }
    response = client.post(f"{ADMIN}/hoteis", json=payload, headers=admin_headers)
    assert response.status_code == 201

    hotel_criado = db_session.get(Hotel, response.json()["id"])
    assert [c.id for c in hotel_criado.comodidades] == [comodidade.id]


def test_criar_hotel_com_cidade_inexistente_retorna_400(client, admin_headers):
    payload = {"nome": "Hotel Fantasma", "estrelas": 3, "cidade_id": 9999}
    response = client.post(f"{ADMIN}/hoteis", json=payload, headers=admin_headers)
    assert response.status_code == 400
    assert "cidade_id" in response.json()["detail"]


def test_criar_hotel_com_comodidade_inexistente_retorna_400(
    client, admin_headers, cidade
):
    payload = {
        "nome": "Hotel Fantasma",
        "estrelas": 3,
        "cidade_id": cidade.id,
        "comodidade_ids": [9999],
    }
    response = client.post(f"{ADMIN}/hoteis", json=payload, headers=admin_headers)
    assert response.status_code == 400
    assert "comodidade_ids" in response.json()["detail"]


def test_atualizar_hotel_substitui_comodidades(
    client, admin_headers, db_session, hotel, comodidade
):
    hotel.comodidades = [comodidade]
    db_session.commit()

    response = client.put(
        f"{ADMIN}/hoteis/{hotel.id}",
        json={"nome": "Hotel Renomeado", "comodidade_ids": []},
        headers=admin_headers,
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Hotel Renomeado"

    db_session.refresh(hotel)
    assert hotel.comodidades == []


def test_atualizar_hotel_sem_comodidade_ids_preserva_comodidades(
    client, admin_headers, db_session, hotel, comodidade
):
    hotel.comodidades = [comodidade]
    db_session.commit()

    response = client.put(
        f"{ADMIN}/hoteis/{hotel.id}", json={"estrelas": 2}, headers=admin_headers
    )
    assert response.status_code == 200
    assert response.json()["estrelas"] == 2

    db_session.refresh(hotel)
    assert [c.id for c in hotel.comodidades] == [comodidade.id]


# ──── QUARTOS E TARIFAS (sanitizacao de referencias) ───────────────────────


def test_criar_quarto_com_hotel_inexistente_retorna_400(client, admin_headers):
    payload = {"hotel_id": 9999, "tipo": "Simples", "preco_diaria": 150.0}
    response = client.post(f"{ADMIN}/quartos", json=payload, headers=admin_headers)
    assert response.status_code == 400
    assert "hotel_id" in response.json()["detail"]


def test_criar_quarto_valido(client, admin_headers, hotel):
    payload = {"hotel_id": hotel.id, "tipo": "Casal Luxo", "preco_diaria": 320.0}
    response = client.post(f"{ADMIN}/quartos", json=payload, headers=admin_headers)
    assert response.status_code == 201
    assert response.json()["hotel_id"] == hotel.id


def test_criar_tarifa_sem_hotel_vale_para_toda_rede(client, admin_headers):
    payload = {
        "nome": "Alta Temporada",
        "data_inicio": "2026-12-20",
        "data_fim": "2027-01-10",
        "multiplicador": 1.3,
    }
    response = client.post(f"{ADMIN}/tarifas", json=payload, headers=admin_headers)
    assert response.status_code == 201
    assert response.json()["hotel_id"] is None


def test_criar_tarifa_com_hotel_inexistente_retorna_400(client, admin_headers):
    payload = {
        "nome": "Carnaval",
        "data_inicio": "2027-02-13",
        "data_fim": "2027-02-18",
        "multiplicador": 1.5,
        "hotel_id": 9999,
    }
    response = client.post(f"{ADMIN}/tarifas", json=payload, headers=admin_headers)
    assert response.status_code == 400


# ──── ROTA PUBLICA DE HOTEIS ────────────────────────────────────────────────


def test_detalhe_hotel_inexistente_retorna_404(client):
    response = client.get(f"{HOTEIS}/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Hotel nao encontrado"


# ──── DOCUMENTACAO OPENAPI (SWAGGER) ───────────────────────────────────────


def test_openapi_documenta_erros_das_rotas_admin(client):
    paths = client.get(f"{settings.API_V1_STR}/openapi.json").json()["paths"]

    # 401/403 herdados do router em qualquer rota admin
    listar_hoteis = paths[f"{ADMIN}/hoteis"]["get"]["responses"]
    assert {"401", "403"} <= set(listar_hoteis)

    # 404 nas rotas que recebem id na URL
    for recurso, chave in [
        ("cidades", "cidade_id"),
        ("comodidades", "comodidade_id"),
        ("hoteis", "hotel_id"),
        ("quartos", "quarto_id"),
        ("servicos", "servico_id"),
        ("tarifas", "tarifa_id"),
    ]:
        excluir = paths[f"{ADMIN}/{recurso}/{{{chave}}}"]["delete"]["responses"]
        assert "404" in excluir, f"DELETE /{recurso} sem 404 documentado"

    # 400 nas rotas que validam referencias no corpo
    assert "400" in paths[f"{ADMIN}/hoteis"]["post"]["responses"]
    assert "400" in paths[f"{ADMIN}/quartos"]["post"]["responses"]
    assert "400" in paths[f"{ADMIN}/tarifas"]["post"]["responses"]
    atualizar_hotel = paths[f"{ADMIN}/hoteis/{{hotel_id}}"]["put"]["responses"]
    assert {"400", "404"} <= set(atualizar_hotel)


def test_openapi_documenta_404_do_detalhe_publico_de_hotel(client):
    paths = client.get(f"{settings.API_V1_STR}/openapi.json").json()["paths"]
    assert "404" in paths[f"{HOTEIS}/{{hotel_id}}"]["get"]["responses"]
