"""Script de Carga de Dados Realista para Demonstração da Banca Avaliadora (Seed Demo).

Projeto: StayFlow (Equipe Bravo - Estágio II 2026.2)
Executar via:
    python -m app.db.seed_demo
ou
    docker compose run --rm api python -m app.db.seed_demo
"""

import logging
from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.usuario import Usuario
from app.models.cidade import Cidade
from app.models.hotel import Hotel
from app.models.quarto import Quarto
from app.models.comodidade import Comodidade
from app.models.servico_adicional import ServicoAdicional
from app.models.tarifa_temporada import TarifaTemporada
from app.models.reserva import Reserva

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("seed_demo")


def seed_demo_data(db: Session):
    logger.info("Iniciando carga de dados realista para a banca avaliadora...")

    # 1. Usuários
    usuarios_data = [
        {"nome": "Prof. Ronildo (Avaliador)", "email": "ronildo@unicatolica.edu.br", "senha": "banca2026", "admin": True},
        {"nome": "Kelvin Barros (Líder)", "email": "kelvin@hotel.com", "senha": "kelvin123", "admin": True},
        {"nome": "Paula Mendes (Cliente)", "email": "paula@hotel.com", "senha": "paula123", "admin": False},
        {"nome": "Lucas Silveira (Hóspede)", "email": "lucas@cliente.com", "senha": "cliente123", "admin": False},
    ]

    usuarios_criados = {}
    for u in usuarios_data:
        usr = db.query(Usuario).filter(Usuario.email == u["email"]).first()
        if not usr:
            usr = Usuario(
                nome=u["nome"],
                email=u["email"],
                senha_hash=get_password_hash(u["senha"]),
                is_admin=u["admin"],
            )
            db.add(usr)
            db.commit()
            db.refresh(usr)
            logger.info(f"Usuário criado: {u['email']} (Admin: {u['admin']})")
        usuarios_criados[u["email"]] = usr

    # 2. Cidades do Ceará (foco acadêmico Unicatólica)
    cidades_data = [
        ("Quixadá", "CE"),
        ("Fortaleza", "CE"),
        ("Jericoacoara", "CE"),
        ("Guaramiranga", "CE"),
        ("Canoa Quebrada", "CE"),
    ]

    cidades_criadas = {}
    for nome, estado in cidades_data:
        cid = db.query(Cidade).filter(Cidade.nome == nome, Cidade.estado == estado).first()
        if not cid:
            cid = Cidade(nome=nome, estado=estado)
            db.add(cid)
            db.commit()
            db.refresh(cid)
            logger.info(f"Cidade criada: {nome}/{estado}")
        cidades_criadas[nome] = cid

    # 3. Comodidades
    comodidades_nomes = [
        "Wi-Fi de Alta Velocidade",
        "Piscina com Borda Infinita",
        "Café da Manhã Incluso",
        "Estacionamento Gratuito",
        "Spa & Massagem",
        "Vista Panorâmica para o Mar",
        "Ar-Condicionado Split",
        "Restaurante Internacional",
    ]
    comodidades_objs = []
    for nome_comod in comodidades_nomes:
        comod = db.query(Comodidade).filter(Comodidade.nome == nome_comod).first()
        if not comod:
            comod = Comodidade(nome=nome_comod, icone="check-circle")
            db.add(comod)
            db.commit()
            db.refresh(comod)
        comodidades_objs.append(comod)

    # 4. Hotéis com Imagens Realistas
    hoteis_dados = [
        {
            "nome": "Monólitos Resort & Spa",
            "cidade": "Quixadá",
            "estrelas": 5,
            "endereco": "Estrada dos Monólitos, Km 4 - Quixadá/CE",
            "descricao": "Resort integrado à paisagem mágica dos monólitos de Quixadá. Experiência de descanso, astronomia e alta gastronomia regional.",
            "capa": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=80",
            "quartos": [
                {"tipo": "SUITE_MASTER", "desc": "Suíte Imperial com Vista para a Pedra da Galinha Choca", "adultos": 2, "criancas": 2, "preco": 550.0},
                {"tipo": "LUXO", "desc": "Apartamento Luxo com Varanda e Banheira de Hidromassagem", "adultos": 2, "criancas": 1, "preco": 380.0},
            ],
        },
        {
            "nome": "Gran Mareiro Iracema Hotel",
            "cidade": "Fortaleza",
            "estrelas": 5,
            "endereco": "Av. Beira Mar, 2500 - Meireles, Fortaleza/CE",
            "descricao": "Hotel de luxo em frente à orla de Fortaleza, com piscina de borda infinita, restaurante de frutos do mar e acesso direto à praia.",
            "capa": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?auto=format&fit=crop&w=1200&q=80",
            "quartos": [
                {"tipo": "SUITE_PRESIDENCIAL", "desc": "Suíte Frente Mar com Jacuzzi Panorâmica", "adultos": 2, "criancas": 2, "preco": 850.0},
                {"tipo": "STANDARD", "desc": "Quarto Standard Executivo com Cama King", "adultos": 2, "criancas": 0, "preco": 320.0},
            ],
        },
        {
            "nome": "Pousada Vila das Dunas Jeri",
            "cidade": "Jericoacoara",
            "estrelas": 4,
            "endereco": "Rua do Forró, s/n - Jericoacoara/CE",
            "descricao": "Charme rústico pé na areia com pôr do sol inesquecível na Duna, café da manhã tropical e passeios de buggy.",
            "capa": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=1200&q=80",
            "quartos": [
                {"tipo": "BUNGALOW_DELUXE", "desc": "Bangalô Tropical com Rede na Varanda", "adultos": 2, "criancas": 1, "preco": 490.0},
            ],
        },
        {
            "nome": "Hotel Serra da Neblina",
            "cidade": "Guaramiranga",
            "estrelas": 4,
            "endereco": "Sítio Floresta, Guaramiranga/CE",
            "descricao": "Clima ameno da serra cearense, fondue à noite, lareira ecológica e trilhas pela mata atlântica nativa.",
            "capa": "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80",
            "quartos": [
                {"tipo": "CHALE_ROMANTICO", "desc": "Chalé Suíço com Lareira e Vista para a Serra", "adultos": 2, "criancas": 0, "preco": 420.0},
            ],
        },
    ]

    quartos_criados = []
    for h_data in hoteis_dados:
        cid = cidades_criadas[h_data["cidade"]]
        hotel = db.query(Hotel).filter(Hotel.nome == h_data["nome"]).first()
        if not hotel:
            hotel = Hotel(
                nome=h_data["nome"],
                descricao=h_data["descricao"],
                endereco=h_data["endereco"],
                cidade_id=cid.id,
                estrelas=h_data["estrelas"],
                foto_capa=h_data["capa"],
                fotos=[h_data["capa"]],
            )
            hotel.comodidades = comodidades_objs[:5]
            db.add(hotel)
            db.commit()
            db.refresh(hotel)
            logger.info(f"Hotel criado: {hotel.nome} em {cid.nome}")

        for q_data in h_data["quartos"]:
            quarto = db.query(Quarto).filter(Quarto.hotel_id == hotel.id, Quarto.tipo == q_data["tipo"]).first()
            if not quarto:
                quarto = Quarto(
                    hotel_id=hotel.id,
                    tipo=q_data["tipo"],
                    descricao=q_data["desc"],
                    capacidade_adultos=q_data["adultos"],
                    capacidade_criancas=q_data["criancas"],
                    preco_diaria=q_data["preco"],
                    quantidade_total=8,
                )
                db.add(quarto)
                db.commit()
                db.refresh(quarto)
                logger.info(f"Quarto criado: {quarto.tipo} (R$ {quarto.preco_diaria}/dia)")
            quartos_criados.append(quarto)

    # 5. Reservas Fictícias Demonstrativas
    cliente_paula = usuarios_criados["paula@hotel.com"]
    if quartos_criados:
        q1 = quartos_criados[0]
        checkin_futuro = date.today() + timedelta(days=15)
        checkout_futuro = date.today() + timedelta(days=18)

        res_existente = db.query(Reserva).filter(Reserva.usuario_id == cliente_paula.id).first()
        if not res_existente:
            reserva_demo = Reserva(
                usuario_id=cliente_paula.id,
                quarto_id=q1.id,
                checkin=checkin_futuro,
                checkout=checkout_futuro,
                quantidade_hospedes=2,
                status="CONFIRMADA",
                preco_total=float(q1.preco_diaria) * 3,
                tipo_tarifa="REEMBOLSAVEL",
            )
            db.add(reserva_demo)
            db.commit()
            db.refresh(reserva_demo)
            logger.info(f"Reserva demonstrativa criada para Paula Mendes (ID: {reserva_demo.id})")

    logger.info("✅ Carga de dados realista finalizada com 100% de sucesso!")


def main():
    db = SessionLocal()
    try:
        seed_demo_data(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
