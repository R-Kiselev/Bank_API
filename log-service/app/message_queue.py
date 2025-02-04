import asyncio
from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from aio_pika.exceptions import AMQPError

from .config import settings
from .logging import logger

RABBITMQ_URL = str(settings.amqp_dsn)


async def on_message(message: AbstractIncomingMessage) -> None:
    try:
        decoded_message = message.body.decode()
        logger.info(f'Processed message content: {decoded_message}')

        await message.ack()
        logger.info('Message acknowledged')

    except Exception as e:
        logger.error(f'Error processing message: {e}')
        message.nack(requeue=True)
        logger.warning('Message nack with requeue')


async def listen() -> None:
    while True:
        try:
            logger.info('Connecting to RabbitMQ...')
            connection = await connect(RABBITMQ_URL)
            async with connection:
                channel = await connection.channel()
                queue = await channel.declare_queue('log-service', durable=True)

                logger.info('Waiting for messages.')
                await queue.consume(on_message, no_ack=False)

                await asyncio.Future()

        except AMQPError as e:
            logger.error(f'RabbitMQ connection error: {e}')
            logger.info('Reconnecting in 5 seconds...')
            await asyncio.sleep(5)
        except Exception as e:
            logger.error(f'Unexpected error in listen function: {e}')
            logger.info('Reconnecting in 5 seconds...')
            await asyncio.sleep(5)


async def start_message_listener():
    logger.info('Starting message listener in background...')
    asyncio.create_task(listen())
