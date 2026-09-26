import asyncio
import json
import logging
from datetime import datetime

import aio_pika
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings

logger = logging.getLogger("audit_worker")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            data = json.loads(message.body.decode("utf-8"))
            logger.info(f"[Worker] Evento de auditoria recebido: {data.get('evento', 'desconhecido')}")

            mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
            db = mongo_client[settings.MONGODB_DB]
            collection = db["logs_auditoria"]

            log_document = {
                **data,
                "timestamp": datetime.utcnow().isoformat(),
                "processado_em": datetime.utcnow().isoformat(),
            }
            await collection.insert_one(log_document)
            logger.info("[Worker] Log persistido com sucesso na coleção 'logs_auditoria' do MongoDB!")

        except Exception as e:
            logger.error(f"[Worker] Erro ao processar mensagem de auditoria: {str(e)}")


async def main():
    logger.info(f"[Worker] Conectando ao RabbitMQ: {settings.RABBITMQ_URL}")
    while True:
        try:
            connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
            async with connection:
                channel = await connection.channel()
                await channel.set_qos(prefetch_count=10)
                queue = await channel.declare_queue("audit.logs", durable=True)
                logger.info("[Worker] Aguardando mensagens na fila 'audit.logs'...")
                await queue.consume(process_message)
                await asyncio.Future()  # Mantém ativo
        except (aio_pika.exceptions.AMQPConnectionError, ConnectionRefusedError) as exc:
            logger.warning(f"[Worker] Falha de conexão com RabbitMQ ({exc}). Tentando novamente em 5s...")
            await asyncio.sleep(5)
        except asyncio.CancelledError:
            break
        except Exception as exc:
            logger.error(f"[Worker] Erro inesperado: {exc}. Reiniciando em 5s...")
            await asyncio.sleep(5)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("[Worker] Finalizado pelo usuário.")

