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


def seed_database(db: Session):
    """Popula o banco com dados iniciais de demonstracao."""

    # --- 1. Usuario Admin ---
    if not db.query(Usuario).filter(Usuario.email == "admin@hotel.com").first():
        admin = Usuario(
            nome="Administrador StayFlow",
            email="admin@hotel.com",
            senha_hash=get_password_hash("admin123"),
            is_admin=True,
        )
        db.add(admin)
        logger.info("Seed: Usuario admin criado.")

    # --- Usuario Cliente de teste ---
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

    # --- 2. Cidades ---
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

    # --- 3. Comodidades ---
    comodidades_data = [
        ("Wi-Fi Gratuito", "wifi"),
        ("Piscina", "waves"),
        ("Academia", "dumbbell"),
        ("Estacionamento", "car"),
        ("Restaurante", "utensils"),
        ("SPA", "sparkles"),
        ("Bar", "wine"),
        ("Room Service", "concierge-bell"),
        ("Ar Condicionado", "snowflake"),
        ("Lavanderia", "shirt"),
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

    # --- 4. Servicos Adicionais ---
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

    # --- 5. Hoteis ---
    hoteis_data = [
        ("Hotel Beira-Mar Fortaleza", 5, "Fortaleza", "Resort de luxo na Praia do Meireles com vista para o mar.", [
            "Wi-Fi Gratuito", "Piscina", "Academia", "Restaurante", "SPA", "Bar", "Room Service", "Ar Condicionado",
        ]),
        ("Pousada Jericoacoara", 4, "Fortaleza", "Pousada aconchegante em Jericoacoara com clima rústico e sofisticado.", [
            "Wi-Fi Gratuito", "Piscina", "Restaurante", "Bar", "Ar Condicionado",
        ]),
        ("Grand São Paulo Hotel", 5, "São Paulo", "Hotel de negócios e lazer na Avenida Paulista.", [
            "Wi-Fi Gratuito", "Academia", "Restaurante", "Bar", "Room Service", "Ar Condicionado", "Lavanderia",
        ]),
        ("Copacabana Palace Inn", 5, "Rio de Janeiro", "Experiência premium na orla de Copacabana.", [
            "Wi-Fi Gratuito", "Piscina", "Academia", "Restaurante", "SPA", "Bar", "Room Service", "Estacionamento", "Ar Condicionado",
        ]),
        ("Pousada do Pelourinho", 3, "Salvador", "Charme histórico no coração do Pelourinho.", [
            "Wi-Fi Gratuito", "Restaurante", "Bar", "Ar Condicionado",
        ]),
        ("Serra Gaúcha Resort", 4, "Gramado", "Refúgio nas montanhas com lareira e fondue.", [
            "Wi-Fi Gratuito", "Restaurante", "SPA", "Bar", "Room Service", "Estacionamento",
        ]),
        ("Floripa Beach Hotel", 4, "Florianópolis", "Hotel moderno próximo às praias de Florianópolis.", [
            "Wi-Fi Gratuito", "Piscina", "Academia", "Restaurante", "Estacionamento", "Ar Condicionado",
        ]),
        ("Hotel Ponta Negra", 3, "Natal", "Hotel aconchegante na Praia de Ponta Negra.", [
            "Wi-Fi Gratuito", "Piscina", "Restaurante", "Ar Condicionado",
        ]),
    ]

    for nome_hotel, estrelas, cidade_nome, desc, amenidades in hoteis_data:
        hotel = db.query(Hotel).filter(Hotel.nome == nome_hotel).first()
        if not hotel:
            hotel = Hotel(
                nome=nome_hotel,
                estrelas=estrelas,
                cidade_id=cidades[cidade_nome].id,
                descricao=desc,
            )
            for amenidade_nome in amenidades:
                if amenidade_nome in comodidades:
                    hotel.comodidades.append(comodidades[amenidade_nome])
            db.add(hotel)
            db.flush()

            # Quartos para cada hotel
            quartos = [
                ("Simples", 1, 0, 180.0 * estrelas / 3),
                ("Casal Luxo", 2, 0, 280.0 * estrelas / 3),
                ("Família Premium", 2, 2, 380.0 * estrelas / 3),
                ("Suíte Master", 2, 1, 520.0 * estrelas / 3),
            ]
            for tipo, adultos, criancas, preco in quartos:
                quarto = Quarto(
                    hotel_id=hotel.id,
                    tipo=tipo,
                    capacidade_adultos=adultos,
                    capacidade_criancas=criancas,
                    preco_diaria=round(preco, 2),
                )
                db.add(quarto)

    db.flush()
    logger.info("Seed: Hoteis e quartos.")

    # --- 6. Tarifas de Temporada ---
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
