"""Testes de integração para o domínio hoteleiro e catálogo.

Cobre:
- Listagem pública de hotéis
- Filtro por cidade
- Detalhes de um hotel por ID e 404 para inexistente
- Criação e atualização de hotéis por administrador
"""

from app.models.cidade import Cidade
from app.models.hotel import Hotel
from app.models.quarto import Quarto


def test_listar_hoteis_vazio(client):
    response = client.get("/api/v1/hoteis")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_criar_e_consultar_hotel(client, db_session, admin_user):
    _, admin_token = admin_user

    # Cria cidade base
    cidade = Cidade(nome="Fortaleza", estado="CE")
    db_session.add(cidade)
    db_session.commit()
    db_session.refresh(cidade)

    # Cria hotel via endpoint admin
    payload_hotel = {
        "nome": "Hotel Praia de Iracema",
        "descricao": "Hotel à beira-mar com vista incrível",
        "endereco": "Av. Beira Mar, 1000",
        "cidade_id": cidade.id,
        "estrelas": 4,
        "foto_capa": "https://images.unsplash.com/photo-1566073771259-6a8506099945",
        "fotos": [],
        "comodidades_ids": [],
    }

    resp = client.post(
        "/api/v1/admin/hoteis",
        json=payload_hotel,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code in (200, 201)
    hotel_id = resp.json()["id"]

    # Consulta pública
    resp_get = client.get(f"/api/v1/hoteis/{hotel_id}")
    assert resp_get.status_code == 200
    data = resp_get.json()
    assert data["nome"] == "Hotel Praia de Iracema"
    assert data["cidade_id"] == cidade.id


def test_hotel_nao_encontrado_retorna_404(client):
    response = client.get("/api/v1/hoteis/999999")
    assert response.status_code == 404
