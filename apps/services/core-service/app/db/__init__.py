"""Script de seed — popula o banco PostgreSQL com dados de demonstracao.

Insere: admin, cidades brasileiras, hoteis, quartos, comodidades, servicos e tarifas.
Executar via: python -m app.db.seed
"""

import logging
from datetime import date

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.cidade import Cidade
from app.models.comodidade import Comodidade
from app.models.hotel import Hotel
from app.models.quarto import Quarto
from app.models.servico_adicional import ServicoAdicional
from app.models.tarifa_temporada import TarifaTemporada
from app.models.usuario import Usuario

logger = logging.getLogger(__name__)

# Constantes de comodidades para evitar repetição de strings literais
COMOD_WIFI = "Wi-Fi Gratuito"
COMOD_PISCINA = "Piscina"
COMOD_ACADEMIA = "Academia"
COMOD_ESTACIONAMENTO = "Estacionamento"
COMOD_RESTAURANTE = "Restaurante"
COMOD_SPA = "SPA"
COMOD_BAR = "Bar"
COMOD_ROOM_SERVICE = "Room Service"
COMOD_AR_CONDICIONADO = "Ar Condicionado"
COMOD_LAVANDERIA = "Lavanderia"


def _seed_usuarios(db: Session) -> None:
    """Insere usuarios padrao (admin e cliente de teste)."""
    if not db.query(Usuario).filter(Usuario.email == "admin@hotel.com").first():
        admin = Usuario(
            nome="Administrador StayFlow",
            email="admin@hotel.com",
            senha_hash=get_password_hash("admin123"),
            is_admin=True,
        )
        db.add(admin)
        logger.info("Seed: Usuario admin criado.")

    if not db.query(Usuario).filter(Usuario.email == "cliente@hotel.com").first():
        cliente = Usuario(
            nome="Maria Santos",
            email="cliente@hotel.com",
            senha_hash=get_password_hash("cliente123"),
            is_admin=False,
        )
        db.add(cliente)
        logger.info("Seed: Usuario cliente criado.")

    db.flush()


def _seed_cidades(db: Session) -> dict[str, Cidade]:
    """Insere cidades de demonstracao e retorna mapa por nome."""
    cidades_data = [
        ("Fortaleza", "CE"),
        ("São Paulo", "SP"),
        ("Rio de Janeiro", "RJ"),
        ("Salvador", "BA"),
        ("Gramado", "RS"),
        ("Florianópolis", "SC"),
        ("Natal", "RN"),
        ("Recife", "PE"),
        ("Belo Horizonte", "MG"),
        ("Curitiba", "PR"),
    ]
    cidades = {}
    for nome, estado in cidades_data:
        cidade = db.query(Cidade).filter(Cidade.nome == nome).first()
        if not cidade:
            cidade = Cidade(nome=nome, estado=estado)
            db.add(cidade)
            db.flush()
        cidades[nome] = cidade
    logger.info(f"Seed: {len(cidades)} cidades.")
    return cidades


def _seed_comodidades(db: Session) -> dict[str, Comodidade]:
    """Insere comodidades padrao e retorna mapa por nome."""
    comodidades_data = [
        (COMOD_WIFI, "wifi"),
        (COMOD_PISCINA, "waves"),
        (COMOD_ACADEMIA, "dumbbell"),
        (COMOD_ESTACIONAMENTO, "car"),
        (COMOD_RESTAURANTE, "utensils"),
        (COMOD_SPA, "sparkles"),
        (COMOD_BAR, "wine"),
        (COMOD_ROOM_SERVICE, "concierge-bell"),
        (COMOD_AR_CONDICIONADO, "snowflake"),
        (COMOD_LAVANDERIA, "shirt"),
    ]
    comodidades = {}
    for nome, icone in comodidades_data:
        comod = db.query(Comodidade).filter(Comodidade.nome == nome).first()
        if not comod:
            comod = Comodidade(nome=nome, icone=icone)
            db.add(comod)
            db.flush()
        comodidades[nome] = comod
    logger.info(f"Seed: {len(comodidades)} comodidades.")
    return comodidades


def _seed_servicos_adicionais(db: Session) -> None:
    """Insere servicos adicionais disponiveis para reserva."""
    servicos_data = [
        ("Café da Manhã Premium", 30.0, "Buffet completo com opções gourmet"),
        ("Translado Aeroporto", 120.0, "Transfer ida e volta do aeroporto"),
        ("Pacote Spa & Bem-estar", 200.0, "Massagem relaxante + sauna + jacuzzi"),
        ("Passeio Turístico", 150.0, "City tour guiado pelos principais pontos"),
    ]
    for nome, preco, desc in servicos_data:
        if not db.query(ServicoAdicional).filter(ServicoAdicional.nome == nome).first():
            db.add(ServicoAdicional(nome=nome, preco=preco, descricao=desc))
    db.flush()
    logger.info("Seed: Servicos adicionais.")


def _criar_quartos_do_hotel(db: Session, hotel_id: int, estrelas: int) -> None:
    """Cria os quartos tipicos para um hotel com base nas estrelas."""
    quartos = [
        ("Simples", 1, 0, 180.0 * estrelas / 3),
        ("Casal Luxo", 2, 0, 280.0 * estrelas / 3),
        ("Família Premium", 2, 2, 380.0 * estrelas / 3),
        ("Suíte Master", 2, 1, 520.0 * estrelas / 3),
    ]
    for tipo, adultos, criancas, preco in quartos:
        quarto = Quarto(
            hotel_id=hotel_id,
            tipo=tipo,
            capacidade_adultos=adultos,
            capacidade_criancas=criancas,
            preco_diaria=round(preco, 2),
        )
        db.add(quarto)


def _seed_hoteis_e_quartos(
    db: Session, cidades: dict[str, Cidade], comodidades: dict[str, Comodidade]
) -> None:
    """Insere catalogo de hoteis com suas comodidades e quartos."""
    hoteis_data = [
        ("Hotel Beira-Mar Fortaleza", 5, "Fortaleza", "Resort de luxo na Praia do Meireles com vista para o mar.", [
            COMOD_WIFI, COMOD_PISCINA, COMOD_ACADEMIA, COMOD_RESTAURANTE, COMOD_SPA, COMOD_BAR, COMOD_ROOM_SERVICE, COMOD_AR_CONDICIONADO,
        ]),
        ("Pousada Jericoacoara", 4, "Fortaleza", "Pousada aconchegante em Jericoacoara com clima rústico e sofisticado.", [
            COMOD_WIFI, COMOD_PISCINA, COMOD_RESTAURANTE, COMOD_BAR, COMOD_AR_CONDICIONADO,
        ]),
        ("Grand São Paulo Hotel", 5, "São Paulo", "Hotel de negócios e lazer na Avenida Paulista.", [
            COMOD_WIFI, COMOD_ACADEMIA, COMOD_RESTAURANTE, COMOD_BAR, COMOD_ROOM_SERVICE, COMOD_AR_CONDICIONADO, COMOD_LAVANDERIA,
        ]),
        ("Copacabana Palace Inn", 5, "Rio de Janeiro", "Experiência premium na orla de Copacabana.", [
            COMOD_WIFI, COMOD_PISCINA, COMOD_ACADEMIA, COMOD_RESTAURANTE, COMOD_SPA, COMOD_BAR, COMOD_ROOM_SERVICE, COMOD_ESTACIONAMENTO, COMOD_AR_CONDICIONADO,
        ]),
        ("Pousada do Pelourinho", 3, "Salvador", "Charme histórico no coração do Pelourinho.", [
            COMOD_WIFI, COMOD_RESTAURANTE, COMOD_BAR, COMOD_AR_CONDICIONADO,
        ]),
        ("Serra Gaúcha Resort", 4, "Gramado", "Refúgio nas montanhas com lareira e fondue.", [
            COMOD_WIFI, COMOD_RESTAURANTE, COMOD_SPA, COMOD_BAR, COMOD_ROOM_SERVICE, COMOD_ESTACIONAMENTO,
        ]),
        ("Floripa Beach Hotel", 4, "Florianópolis", "Hotel moderno próximo às praias de Florianópolis.", [
            COMOD_WIFI, COMOD_PISCINA, COMOD_ACADEMIA, COMOD_RESTAURANTE, COMOD_ESTACIONAMENTO, COMOD_AR_CONDICIONADO,
        ]),
        ("Hotel Ponta Negra", 3, "Natal", "Hotel aconchegante na Praia de Ponta Negra.", [
            COMOD_WIFI, COMOD_PISCINA, COMOD_RESTAURANTE, COMOD_AR_CONDICIONADO,
        ]),
    ]

    for nome_hotel, estrelas, cidade_nome, desc, amenidades in hoteis_data:
        hotel = db.query(Hotel).filter(Hotel.nome == nome_hotel).first()
        if hotel:
            continue

        cidade = cidades.get(cidade_nome)
        cidade_id = cidade.id if cidade else None

        hotel = Hotel(
            nome=nome_hotel,
            estrelas=estrelas,
            cidade_id=cidade_id,
            descricao=desc,
        )
        for amenidade_nome in amenidades:
            if amenidade_nome in comodidades:
                hotel.comodidades.append(comodidades[amenidade_nome])
        db.add(hotel)
        db.flush()

        _criar_quartos_do_hotel(db, hotel.id, estrelas)

    db.flush()
    logger.info("Seed: Hoteis e quartos.")


def _seed_tarifas(db: Session) -> None:
    """Insere tarifas sazonais configuradas."""
    tarifas_data = [
        ("Alta Temporada - Verão", date(2027, 1, 1), date(2027, 3, 1), 1.3),
        ("Réveillon", date(2026, 12, 20), date(2027, 1, 5), 1.5),
        ("Carnaval 2027", date(2027, 2, 25), date(2027, 3, 5), 1.4),
    ]
    for nome, inicio, fim, mult in tarifas_data:
        if not db.query(TarifaTemporada).filter(TarifaTemporada.nome == nome).first():
            db.add(TarifaTemporada(
                nome=nome, data_inicio=inicio, data_fim=fim, multiplicador=mult
            ))
    logger.info("Seed: Tarifas de temporada.")


def seed_database(db: Session) -> None:
    """Popula o banco com dados iniciais de demonstracao."""
    _seed_usuarios(db)
    cidades = _seed_cidades(db)
    comodidades = _seed_comodidades(db)
    _seed_servicos_adicionais(db)
    _seed_hoteis_e_quartos(db, cidades, comodidades)
    _seed_tarifas(db)
    db.commit()
    logger.info("Seed completo!")


def main():
    logging.basicConfig(level=logging.INFO)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
