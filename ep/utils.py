import logging
from contextlib import suppress
from socket import socket
from typing import Optional

import coloredlogs
from discord.http import HTTPClient

def codeblock(string: str, style: str = "") -> str:
    """Format a string into a code block, escapes any other backticks"""
    zwsp = "``\u200b"
    return f'```{style}\n{string.replace("``", zwsp)}```\n'

def probe(address: str, port: int) -> bool:
    """Probe a system port by attempting to connect to it."""
    sock = socket()

    try:
        sock.connect((address, port))
    except ConnectionRefusedError:
        return False
    else:
        return True
    finally:
        with suppress(Exception):
            sock.close()

async def http_probe(token: str, config: "ep.Config") -> bool:
    """Probe a discord socket channel for a presence."""
    channel_id: int = config["ep"]["socket_channel"]
    superusers: List[int] = config["ep"]["superusers"]

    http = HTTPClient()

    try:
        user = await http.static_login(token, bot=False)

        if int(user["id"]) not in superusers:
            return False

        channel = await http.get_channel(channel_id)

        if "topic" in channel:
            topic = channel["topic"]

            if topic is not None and topic == "alive":
                return True
    finally:
        await http.close()

def get_logger(
    name: str, level: str = "INFO", fmt: Optional[str] = None
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))

    fmt = fmt or (
        "[%(asctime)s] %(levelname)s - %(funcName)s:%(lineno)d - %(module)s - %(message)s"
    )
    coloredlogs.install(fmt=fmt, level=level, logger=logger)
    return logger