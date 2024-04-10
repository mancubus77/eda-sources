"""amq.py.

An ansible-rulebook event source plugin for receiving events via a AMQP topic.

Arguments:
---------
    host:      The host where the AMQP topic is hosted
    port:      The port where the AMQP server is listening
    encoding:  Message encoding scheme. Default to utf-8
    channel:   The AMQP channel
    username:  Username for broker auth
    password:  Password for broker auth
"""

import asyncio
import logging
from typing import Any

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage


async def main(  # pylint: disable=R0914
    queue: asyncio.Queue,
    args: dict[str, Any],
) -> None:

    async def on_message(message: AbstractIncomingMessage) -> None:
        """
        Callback function to process received message
        """
        print("[x] Received message %r" % message)
        print("Message body is: %r" % message.body)
        await queue.put({"body": message.body.decode(encoding)})

    """Receive events via a AMQP topic."""
    logger = logging.getLogger()

    channel_name = args.get("channel")
    host = args.get("host")
    port = args.get("port")
    username = args.get("username")
    password = args.get("password")
    encoding = args.get("encoding", "utf-8")

    connection = await connect(f"amqp://{username}:{password}@{host}:{port}/")

    async with connection:
        # Creating a channel
        channel = await connection.channel()
        amq_queue = await channel.declare_queue(channel_name)
        await amq_queue.consume(on_message, no_ack=True)
        await asyncio.Future()


if __name__ == "__main__":
    """MockQueue if running directly."""

    class MockQueue:
        """A fake queue."""

        async def put(self: "MockQueue", event: dict) -> None:
            """Print the event."""
            print(event)  # noqa: T201

    asyncio.run(
        main(
            MockQueue(),
            {
                "channel": "hello",
                "host": "localhost",
                "port": "9092",
                "username": "test",
                "password": "test",
            },
        ),
    )
