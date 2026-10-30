"""Testes unitarios do PricingService (calcular_preco)."""

from datetime import date

import pytest

from app.models.cidade import Cidade
from app.models.hotel import Hotel
from app.models.quarto import Quarto
from app.models.servico_adicional import ServicoAdicional
from app.models.tarifa_temporada import TarifaTemporada
from app.services.pricing_service import calcular_preco

CHECKIN = date(2026, 3, 10)
CHECKOUT = date(2026, 3, 13)  # 3 diarias
PRECO_DIARIA = 200.0


@pytest.fixture
def quarto(db_session):
    cidade = Cidade(nome="Fortaleza", estado="CE")
    db_session.add(cidade)
    db_session.flush()
    hotel = Hotel(nome="Hotel Teste", estrelas=4, cidade_id=cidade.id)
    db_session.add(hotel)
    db_session.flush()
    quarto = Quarto(hotel_id=hotel.id, tipo="Simples", preco_diaria=PRECO_DIARIA)
    db_session.add(quarto)
    db_session.commit()
    db_session.refresh(quarto)
    return quarto


def _tarifa(db, multiplicador, inicio, fim, hotel_id=None, nome="Temporada"):
    db.add(
        TarifaTemporada(
            nome=nome,
            data_inicio=inicio,
            data_fim=fim,
            multiplicador=multiplicador,
            hotel_id=hotel_id,
        )
    )
    db.commit()


class TestDiariaBase:
    def test_calculo_diarias_base(self, db_session, quarto):
        r = calcular_preco(db_session, quarto.id, CHECKIN, CHECKOUT)

        assert r["valor_diaria"] == 200.0
        assert r["num_diarias"] == 3
        assert r["multiplicador_temporada"] == 1.0
        assert r["subtotal"] == 600.0
        assert r["extras"] == 0.0
        assert r["desconto"] == 0.0
        assert r["valor_servicos"] == 0.0
        assert r["valor_total"] == 600.0

    @pytest.mark.parametrize("dias", [1, 2, 7, 30])
    def test_total_proporcional_ao_numero_de_diarias(self, db_session, quarto, dias):
        checkout = date(2026, 3, 10 + dias) if dias < 22 else date(2026, 4, 9)
        r = calcular_preco(db_session, quarto.id, CHECKIN, checkout)
        assert r["num_diarias"] == (checkout - CHECKIN).days
        assert r["valor_total"] == PRECO_DIARIA * r["num_diarias"]


class TestTarifaSazonal:
    def test_alta_temporada_aplica_multiplicador(self, db_session, quarto):
        _tarifa(db_session, 1.5, date(2026, 3, 1), date(2026, 3, 31), quarto.hotel_id)

        r = calcular_preco(db_session, quarto.id, CHECKIN, CHECKOUT)

        assert r["multiplicador_temporada"] == 1.5
        assert r["subtotal"] == 900.0
        assert r["valor_total"] == 900.0

    def test_tarifa_global_da_rede_se_aplica(self, db_session, quarto):
        _tarifa(db_session, 1.2, date(2026, 3, 1), date(2026, 3, 31), hotel_id=None)

        r = calcular_preco(db_session, quarto.id, CHECKIN, CHECKOUT)

        assert r["multiplicador_temporada"] == 1.2
        assert r["subtotal"] == 720.0

    def test_usa_o_maior_multiplicador_quando_ha_mais_de_uma_tarifa(
        self, db_session, quarto
    ):
        _tarifa(db_session, 1.2, date(2026, 3, 1), date(2026, 3, 31), None, "Rede")
        _tarifa(db_session, 1.8, date(2026, 3, 1), date(2026, 3, 31), quarto.hotel_id)

        r = calcular_preco(db_session, quarto.id, CHECKIN, CHECKOUT)

        assert r["multiplicador_temporada"] == 1.8

    def test_tarifa_fora_do_periodo_e_ignorada(self, db_session, quarto):
        _tarifa(db_session, 2.0, date(2026, 12, 1), date(2026, 12, 31), quarto.hotel_id)

        r = calcular_preco(db_session, quarto.id, CHECKIN, CHECKOUT)

        assert r["multiplicador_temporada"] == 1.0

    def test_tarifa_de_outro_hotel_e_ignorada(self, db_session, quarto):
        outro = Hotel(nome="Outro", estrelas=3, cidade_id=quarto.hotel.cidade_id)
        db_session.add(outro)
        db_session.commit()
        _tarifa(db_session, 2.0, date(2026, 3, 1), date(2026, 3, 31), outro.id)

        r = calcular_preco(db_session, quarto.id, CHECKIN, CHECKOUT)

        assert r["multiplicador_temporada"] == 1.0

    def test_tarifa_considera_apenas_a_data_de_checkin(self, db_session, quarto):
        # Tarifa comeca depois do checkin: nao deve ser aplicada
        _tarifa(db_session, 2.0, date(2026, 3, 11), date(2026, 3, 31), quarto.hotel_id)

        r = calcular_preco(db_session, quarto.id, CHECKIN, CHECKOUT)

        assert r["multiplicador_temporada"] == 1.0


class TestOpcionaisEDescontos:
    def test_early_checkin_adiciona_15_por_cento(self, db_session, quarto):
        r = calcular_preco(db_session, quarto.id, CHECKIN, CHECKOUT, early_checkin=True)
        assert r["extras"] == 90.0
        assert r["valor_total"] == 690.0

    def test_late_checkout_adiciona_15_por_cento(self, db_session, quarto):
        r = calcular_preco(db_session, quarto.id, CHECKIN, CHECKOUT, late_checkout=True)
        assert r["extras"] == 90.0
        assert r["valor_total"] == 690.0

    def test_berco_cobra_30_por_diaria(self, db_session, quarto):
        r = calcular_preco(db_session, quarto.id, CHECKIN, CHECKOUT, berco=True)
        assert r["extras"] == 90.0  # 30 * 3
        assert r["valor_total"] == 690.0

    def test_todos_os_extras_combinados(self, db_session, quarto):
        r = calcular_preco(
            db_session,
            quarto.id,
            CHECKIN,
            CHECKOUT,
            early_checkin=True,
            late_checkout=True,
            berco=True,
        )
        assert r["extras"] == 90.0 + 90.0 + 90.0
        assert r["valor_total"] == 870.0

    def test_tarifa_nao_reembolsavel_da_10_por_cento_de_desconto(
        self, db_session, quarto
    ):
        r = calcular_preco(
            db_session, quarto.id, CHECKIN, CHECKOUT, tipo_tarifa="NAO_REEMBOLSAVEL"
        )
        assert r["desconto"] == 60.0
        assert r["valor_total"] == 540.0

    def test_tarifa_reembolsavel_nao_tem_desconto(self, db_session, quarto):
        r = calcular_preco(
            db_session, quarto.id, CHECKIN, CHECKOUT, tipo_tarifa="REEMBOLSAVEL"
        )
        assert r["desconto"] == 0.0

    def test_extras_incidem_sobre_subtotal_com_multiplicador(self, db_session, quarto):
        _tarifa(db_session, 1.5, date(2026, 3, 1), date(2026, 3, 31), quarto.hotel_id)
        r = calcular_preco(db_session, quarto.id, CHECKIN, CHECKOUT, early_checkin=True)
        assert r["subtotal"] == 900.0
        assert r["extras"] == 135.0  # 15% de 900
        assert r["valor_total"] == 1035.0


class TestServicosAdicionais:
    @pytest.fixture
    def servicos(self, db_session):
        itens = [
            ServicoAdicional(nome="Cafe da manha", preco=40.0),
            ServicoAdicional(nome="Estacionamento", preco=25.0),
            ServicoAdicional(nome="Pet", preco=60.0),
        ]
        db_session.add_all(itens)
        db_session.commit()
        return itens

    def test_servico_unico(self, db_session, quarto, servicos):
        cafe = servicos[0]
        r = calcular_preco(
            db_session, quarto.id, CHECKIN, CHECKOUT, servico_ids=[cafe.id]
        )
        assert r["valor_servicos"] == 40.0
        assert r["valor_total"] == 640.0

    def test_varios_servicos_somam(self, db_session, quarto, servicos):
        ids = [s.id for s in servicos]
        r = calcular_preco(db_session, quarto.id, CHECKIN, CHECKOUT, servico_ids=ids)
        assert r["valor_servicos"] == 125.0
        assert r["valor_total"] == 725.0

    def test_lista_vazia_ou_none_nao_cobra_servicos(self, db_session, quarto):
        r_none = calcular_preco(
            db_session, quarto.id, CHECKIN, CHECKOUT, servico_ids=None
        )
        r_vazia = calcular_preco(
            db_session, quarto.id, CHECKIN, CHECKOUT, servico_ids=[]
        )
        assert r_none["valor_servicos"] == 0.0
        assert r_vazia["valor_servicos"] == 0.0

    def test_id_de_servico_inexistente_e_ignorado(self, db_session, quarto, servicos):
        r = calcular_preco(
            db_session, quarto.id, CHECKIN, CHECKOUT, servico_ids=[servicos[1].id, 9999]
        )
        assert r["valor_servicos"] == 25.0

    def test_servicos_nao_sofrem_desconto_nem_multiplicador(
        self, db_session, quarto, servicos
    ):
        r = calcular_preco(
            db_session,
            quarto.id,
            CHECKIN,
            CHECKOUT,
            tipo_tarifa="NAO_REEMBOLSAVEL",
            servico_ids=[servicos[2].id],
        )
        assert r["valor_total"] == 600.0 - 60.0 + 60.0


class TestValidacoes:
    def test_quarto_inexistente_levanta_erro(self, db_session):
        with pytest.raises(ValueError, match="Quarto nao encontrado"):
            calcular_preco(db_session, 9999, CHECKIN, CHECKOUT)

    def test_checkout_anterior_ao_checkin(self, db_session, quarto):
        with pytest.raises(ValueError, match="posterior ao checkin"):
            calcular_preco(db_session, quarto.id, CHECKOUT, CHECKIN)

    def test_checkout_igual_ao_checkin(self, db_session, quarto):
        with pytest.raises(ValueError, match="posterior ao checkin"):
            calcular_preco(db_session, quarto.id, CHECKIN, CHECKIN)