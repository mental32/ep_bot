"""Main client implementation."""
import asyncio
import os
import sys
import time
import inspect
import importlib
from pathlib import Path
from json import dumps as json_dumps
from time import time
from functools import partial
from typing import Union, Any, Optional
from traceback import print_exc

from discord import TextChannel

from ..config import Config
from ..utils import codeblock, infer_token
from .cog import Cog
from .base import BaseClient
from .websocket import WebsocketServer


class Client(BaseClient):
    r"""A hard client implementation used as default.

    Parameters
    ----------
    \*args : Any
        foo
    config : :class:`ep.Config`
        The config to use.
    disable : :class:`bool`
        disable the run method of the client instance, usefully for testing.
    \*\*kwargs : Any
        Any other keyword arguments are propagated into the :class:`ep.BaseClient`
    """
    _timestamp: int = int(time())

    def __init__(self, *args, config: Config, disable: bool = False, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.__socket_noloop = set()
        self._config = config

        if "cog_path" in self._config["ep"]:
            self.load_cogs(config.fp.parent.joinpath(self._config["ep"]["cog_path"]))

        if disable or "EP_DISABLED" in os.environ:
            self.run = lambda *_, **__: None
            return

        def close_http():
            self.loop.run_until_complete(self.http.close())

        self.run = partial(self.run, infer_token(cleanup=close_http))

        self._wss = wss = WebsocketServer(self)
        self.schedule_task(wss.serve())

    def __enter__(self):
        self._timestamp = int(time())
        return self

    def __exit__(self, *_, **__):
        self.logger.info(
            "Ran for %s seconds, Exiting...", int(time()) - self._timestamp
        )

    # Properties

    @property
    def ready(self):
        """ :class:`bool`- same as ``Client.is_ready()`` just as a property."""
        return self.is_ready()

    @property
    def config(self):
        """:class:`ep.Config` - The current client configuration."""
        return self._config

    @property
    def wss(self):
        """:class:`ep.WebsocketServer` - The current websocket server."""
        return self._wss

    @property
    def timestamp(self):
        """:class:`int` - The timestamp of when the client started or the timestamp of when the class was created."""
        return self._timestamp

    # Internals

    def _get_socket_channel(self) -> Optional[TextChannel]:
        """Return the :class:`discord.TextChannel` for a "socket_channel" id in the config."""
        try:
            channel_id = self._config["ep"]["socket_channel"]
        except KeyError:
            self.logger.warning("`socket_channel` option not present in configuration!")
            return None

        channel = self.get_channel(channel_id)

        if channel is None:
            self.logger.error(
                "`socket_channel` could not be found! %s", repr(channel_id)
            )
            return None

        return channel

    # Public

    def load_cogs(self, cog_path: Path) -> None:
        """Load cogs from a given :class:`pathlib.Path`.

        Parameters
        ----------
        cog_path : :class:`pathlib.Path`
            The path to load the cogs from.
        """
        if not isinstance(cog_path, Path):
            raise TypeError("`cog_path` must be an instance of pathlib.Path.")

        cogs = cog_path.resolve().absolute()

        if not cogs.exists():
            raise FileNotFoundError("Ru'roh the cogs directory doesn't seem to exist!")

        try:
            sys.path.append(str(cogs))

            for path in cogs.iterdir():
                path = path.resolve().absolute()

                if (is_file := path.is_file()) and path.name.endswith(".py"):
                    name = path.name[:-3]
                elif is_file:
                    continue
                else:
                    name = path.name

                module = importlib.import_module(name)
                module_all = getattr(module, "__all__", [])

                for obj in map(partial(getattr, module), module_all):
                    if (
                        isinstance(obj, type)
                        and issubclass(obj, Cog)
                        and getattr(obj, "__export__", False)
                    ):
                        self.add_cog(obj(self))
        finally:
            sys.path.remove(str(cogs))

    # Event handlers

    async def on_connect(self) -> None:  # pylint: disable=missing-function-docstring
        self.logger.info("Connected")

    async def on_ready(self) -> None:  # pylint: disable=missing-function-docstring
        self.logger.info("Ready")

        if (
            self._config["ep"]["socket_emit"]
            and (channel := self._get_socket_channel()) is not None
        ):
            await channel.edit(topic="alive")

    async def on_socket_response(
        self, message: Union[Any, bytes]
    ) -> None:  # pylint: disable=missing-function-docstring
        if (
            not self._config["ep"]["socket_emit"]
            or isinstance(message, bytes)
            or not self.is_ready()
        ):
            return

        await self.wss.broadcast(message)

        channel = self._get_socket_channel()

        if channel is None:
            return

        await asyncio.sleep(1)

        if (
            message["t"] == "MESSAGE_CREATE"
            and (message_id := int(message["d"]["id"])) in self.__socket_noloop
        ):
            self.__socket_noloop.remove(message_id)
            return

        data = json_dumps(message)

        if len(data) >= 1900:
            return  # TODO: Impl paging objects

        try:
            message = await channel.send(codeblock(data, style="json"))
        except Exception as err:
            self.logger.error(err)
            raise
        else:
            self.__socket_noloop.add(message.id)
