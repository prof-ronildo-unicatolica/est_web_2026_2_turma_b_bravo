"""Testes unitarios do TutorialService."""

import asyncio
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from app.models.tutorial import (
    Disciplina,
    Linguagem,
    Professor,
    ProfessorDetail,
    Stack,
    Tecnologia,
)
from app.services.tutorial_service import TutorialService


@pytest.fixture
def service(db_session):
    return TutorialService(db_session)


class TestGetSobreData:
    def test_sem_dados_retorna_estrutura_vazia(self, service):
        r = service.get_sobre_data()
        assert r["equipe"] == "Alpha"
        assert r["ano"] == 2026
        assert r["semestre"] == 2
        assert r["professor"] is None
        assert r["disciplinas"] == []
        assert r["stacks"] == []

    def test_com_professor_disciplina_e_stack(self, db_session, service):
        prof = Professor(nome="Prof X", email="x@test.com")
        prof.detalhe = ProfessorDetail(
            sala="Sala 1", biografia="Bio", biografia_mapa={"lat": 1}
        )
        disc = Disciplina(nome="Web", ano=2026, semestre=2)
        tech = Tecnologia(nome="FastAPI")
        tech.linguagens.append(Linguagem(nome="Python"))
        disc.tecnologias.append(tech)
        prof.disciplinas.append(disc)
        stack = Stack(nome="Backend")
        stack.tecnologias.append(tech)
        db_session.add_all([prof, stack])
        db_session.commit()

        r = service.get_sobre_data()

        assert r["professor"]["nome"] == "Prof X"
        assert r["professor"]["sala"] == "Sala 1"
        assert r["professor"]["biografia_mapa"] == {"lat": 1}
        assert r["disciplinas"][0]["nome"] == "Web"
        assert r["disciplinas"][0]["tecnologias"] == ["FastAPI"]
        assert r["stacks"][0]["nome"] == "Backend"
        assert r["stacks"][0]["tecnologias"][0]["linguagens"] == ["Python"]

    def test_professor_sem_detalhe_usa_valores_padrao(self, db_session, service):
        db_session.add(Professor(nome="Sem Detalhe", email="sd@test.com"))
        db_session.commit()

        r = service.get_sobre_data()

        assert r["professor"]["sala"] == ""
        assert r["professor"]["biografia"] == ""
        assert r["professor"]["biografia_mapa"] is None


class TestProfessor:
    def test_create_e_get_professor_by_id(self, service):
        payload = SimpleNamespace(
            nome="Prof Y",
            email="y@test.com",
            sala="Sala 2",
            biografia="Bio Y",
            biografia_mapa=None,
        )
        criado = service.create_professor(payload)

        encontrado = service.get_professor_by_id(criado.id)

        assert encontrado.id == criado.id
        assert encontrado.detalhe.sala == "Sala 2"

    def test_get_professor_inexistente_retorna_none(self, service):
        assert service.get_professor_by_id(uuid.uuid4()) is None


class TestCreateDisciplina:
    def test_cria_disciplina_e_publica_evento(self, db_session, service):
        prof = Professor(nome="P", email="p@test.com")
        db_session.add(prof)
        db_session.commit()
        payload = SimpleNamespace(
            nome="BD", ano=2026, semestre=2, professor_id=str(prof.id)
        )

        with patch(
            "app.services.tutorial_service.publish_event", new_callable=AsyncMock
        ) as publish:
            disciplina = asyncio.run(service.create_disciplina(payload))

        assert disciplina.nome == "BD"
        publish.assert_awaited_once()
        fila, evento = publish.await_args.args
        assert fila == "audit.logs"
        assert evento["evento"] == "disciplina.criada"
        assert evento["nome"] == "BD"
        assert evento["professor_id"] == str(prof.id)