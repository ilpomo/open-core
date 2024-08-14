from abc import ABC, abstractmethod
from typing import Any

from zmq import PAIR, PUB, SUB, REQ, REP, DEALER, ROUTER, PUSH, PULL
from zmq.asyncio import Context

from src.actor.serializer import Json, MessagePack, Pickle
from src.actor.socket_manager.SocketManager import SocketManager

INPROC, IPC, UDP, TCP, PGM, EPGM = 'inproc', 'ipc', 'udp', 'tcp', 'pgm', 'epgm'

Name = str
SocketType = int
Endpoint = str
Topic = bytes
Message = Any

Serializer = Json | MessagePack | Pickle


class AbstractActor(ABC):
    """
    ``AbstractActor`` class for managing different types of ``SocketManager``.
    Each ``AbstractActor`` has built-in serializers - currently ``JSON``, ``MessagePack``, and ``Pickle`` - for
    serializing messages before emitting them over the network to other ``AbstractActor`` implementations.
    """

    SOCKET_TYPES = (PAIR, PUB, SUB, REQ, REP, DEALER, ROUTER, PUSH, PULL)

    def __init__(
        self,
        name: str
    ):
        """
        Initializes the ``AbstractActor`` class with private attributes for ZeroMQ Context, ``JSON``, ``MessagePack``,
        and ``Pickle`` serializers, as well as sets for binding and connecting endpoints.
        Publicly initializes it with the provided ``name`` and a dictionary of ``SocketManager``.

        :param name: The ``name`` associated with the AbstractActor.
        """

        # private

        self._context = Context(io_threads=1)

        self._json_serializer = Json()
        self._msgpack_serializer = MessagePack()
        self._pickle_serializer = Pickle()

        self._bind: set[str] = set()
        self._connect: set[str] = set()

        # public

        self.name = name
        self.socket_managers: dict[Name, SocketManager] = {}

    def __str__(self):
        """
        Returns a string representation of the ``AbstractActor`` object with its name.

        :return: A formatted string showing the object ``name``.
        """

        return f"{self.__class__.__name__}({self.name})"

    def __getitem__(
        self,
        name: Name
    ) -> SocketManager:
        """
        Gets the ``SocketManager`` instance associated with the given ``name``.

        :param name: The ``name`` of the ``SocketManager`` to retrieve.
        :return: The ``SocketManager`` associated with the given ``name``.
        :raise KeyError: If no such ``SocketManager`` is found in this ``AbstractActor``.
        """

        return self.socket_managers[name]

    # private

    def _name_is_available(
        self,
        name: Name
    ) -> bool:
        """
        Checks if a given ``name`` is available in the ``self.socket_managers``.

        :param name: The ``name`` to check availability for.
        :return: ``True`` if the ``name`` is not in the ``self.socket_managers``, ``False`` otherwise.
        """

        return name not in self.socket_managers

    def _socket_type_is_available(
        self,
        socket_type: SocketType
    ) -> bool:
        """
        Checks if a given ``socket_type`` is available in the predefined class ``SOCKET_TYPES``.

        :param socket_type: The ``socket_type`` to check availability for.
        :return: ``True`` if the socket type is in ``SOCKET_TYPES``, ``False`` otherwise.
        """

        return socket_type in self.SOCKET_TYPES

    def _create_socket_manager(
        self,
        name: Name,
        socket_type: SocketType
    ) -> None:
        """
        Creates a new ``SocketManager`` with the given ``name`` and ``socket_type`` if both are available.

        :param name: The ``name`` for the new ``SocketManager``.
        :param socket_type: The ``socket_type`` for the new ``SocketManager``.
        :return: ``None``
        :raises ValueError: If the ``name`` or ``socket_type`` is unavailable.
        """

        if not self._name_is_available(name=name):
            raise ValueError(f"The name {name} is unavailable.")

        if not self._socket_type_is_available(socket_type=socket_type):
            raise ValueError(f"The socket_type {socket_type} is unavailable.")

        self.socket_managers[name] = SocketManager(name=name, socket=self._context.socket(socket_type=socket_type))

    async def _emit(
        self,
        name: Name,
        topic: Topic,
        message: Message,
        serializer: Serializer
    ) -> None:
        """
        Emits an event about a ``topic`` through the associated ``SocketManager`` using the given ``serializer``.
        An event is a tuple containing the ``topic`` and the encoded ``message``.

        :param name: The ``name`` of the ``SocketManager`` used for emitting the event.
        :param topic: The ``topic`` under which the event will be emitted.
        :param message: The ``message`` to be emitted.
        :param serializer: The ``serializer`` used to encode the message.
        :return: ``None``
        """

        await self.socket_managers[name].emit(event=(topic, serializer.encode(obj=message)))

    async def _recv(
        self,
        name: Name,
        serializer: Serializer
    ) -> object:
        """
        Decodes the event's ``message`` received by the specified ``SocketManager`` using the given ``serializer``.
        The event's ``topic`` has already been filtered out by the ``SocketManager``.

        :param name: The ``name`` of the ``SocketManager`` used for receiving the event.
        :param serializer: The ``serializer`` used to decode the ``message``.
        :return: The decoded ``message``.
        """

        return serializer.decode(data=await self.socket_managers[name].recv())

    # public

    def create_pair_socket_manager(
        self,
        name: Name
    ) -> None:
        """
        Creates a ``SocketManager`` of type ``PAIR`` with the given ``name``.

        :param name: The ``name`` for the new ``SocketManager``.
        :return: ``None``
        """

        self._create_socket_manager(name=name, socket_type=PAIR)

    def create_pub_socket_manager(
        self,
        name: Name
    ) -> None:
        """
        Creates a ``SocketManager`` of type ``PUB`` with the given ``name``.

        :param name: The ``name`` for the new ``SocketManager``.
        :return: ``None``
        """

        self._create_socket_manager(name=name, socket_type=PUB)

    def create_sub_socket_manager(
        self,
        name: Name
    ) -> None:
        """
        Creates a ``SocketManager`` of type ``SUB`` with the given ``name``.

        :param name: The ``name`` for the new ``SocketManager``.
        :return: ``None``
        """

        self._create_socket_manager(name=name, socket_type=SUB)

    def create_req_socket_manager(
        self,
        name: Name
    ) -> None:
        """
        Creates a ``SocketManager`` of type ``REQ`` with the given ``name``.

        :param name: The ``name`` for the new ``SocketManager``.
        :return: ``None``
        """

        self._create_socket_manager(name=name, socket_type=REQ)

    def create_rep_socket_manager(
        self,
        name: Name
    ) -> None:
        """
        Creates a ``SocketManager`` of type ``REP`` with the given ``name``.

        :param name: The ``name`` for the new ``SocketManager``.
        :return: ``None``
        """

        self._create_socket_manager(name=name, socket_type=REP)

    def create_dealer_socket_manager(
        self,
        name: Name
    ) -> None:
        """
        Creates a ``SocketManager`` of type ``DEALER`` with the given ``name``.

        :param name: The ``name`` for the new ``SocketManager``.
        :return: ``None``
        """

        self._create_socket_manager(name=name, socket_type=DEALER)

    def create_router_socket_manager(
        self,
        name: Name
    ) -> None:
        """
        Creates a ``SocketManager`` of type ``ROUTER`` with the given ``name``.

        :param name: The ``name`` for the new ``SocketManager``.
        :return: ``None``
        """

        self._create_socket_manager(name=name, socket_type=ROUTER)

    def create_push_socket_manager(
        self,
        name: Name
    ) -> None:
        """
        Creates a ``SocketManager`` of type ``PUSH`` with the given ``name``.

        :param name: The ``name`` for the new ``SocketManager``.
        :return: ``None``
        """

        self._create_socket_manager(name=name, socket_type=PUSH)

    def create_pull_socket_manager(
        self,
        name: Name
    ) -> None:
        """
        Creates a ``SocketManager`` of type ``PULL`` with the given ``name``.

        :param name: The ``name`` for the new ``SocketManager``.
        :return: ``None``
        """

        self._create_socket_manager(name=name, socket_type=PULL)

    def create_socket_manager(
        self,
        name: Name,
        socket_type: SocketType
    ) -> None:
        """
        Creates a new ``SocketManager`` with the given ``name`` and ``socket_type`` if available.

        :param name: The ``name`` for the new ``SocketManager``.
        :param socket_type: The ``socket_type`` for the new ``SocketManager``.
        :return: ``None``
        :raises ValueError: If the ``name`` or ``socket_type`` is unavailable.
        """

        self._create_socket_manager(name=name, socket_type=socket_type)

    async def remove_socket_manager(
        self,
        name: Name
    ) -> None:
        """
        Removes a ``SocketManager`` by terminating it and deleting it from the ``self.socket_managers`` dictionary.

        :param name: The ``name`` of the ``SocketManager`` to be removed.
        :return: ``None``
        """

        await self.socket_managers[name].terminate()

        del self.socket_managers[name]

    async def emit_bytes(
        self,
        name: Name,
        topic: Topic,
        message: Message
    ) -> None:
        """
        Emits an event composed of a ``topic`` and a ``message`` through the specified ``SocketManager``.

        :param name: The ``name`` of the ``SocketManager`` to emit the event through.
        :param topic: The ``topic`` under which the event will be emitted.
        :param message: The ``message`` to be emitted.
        :return: ``None``
        """

        await self.socket_managers[name].emit(event=(topic, bytes(message)))

    async def emit_json(
        self,
        name: Name,
        topic: Topic,
        message: Message
    ) -> None:
        """
        Emits an event composed of a ``topic`` and a ``message`` through the specified ``SocketManager``.
        The ``message`` will be encoded with the ``JSON`` serializer.

        :param name: The ``name`` of the ``SocketManager`` to emit the event through.
        :param topic: The ``topic`` under which the event will be emitted.
        :param message: The ``message`` to be emitted.
        :return: ``None``
        """

        await self._emit(name=name, topic=topic, message=message, serializer=self._json_serializer)

    async def emit_msgpack(
        self,
        name: Name,
        topic: Topic,
        message: Message
    ) -> None:
        """
        Emits an event composed of a ``topic`` and a ``message`` through the specified ``SocketManager``.
        The ``message`` will be encoded with the ``MessagePack`` serializer.

        :param name: The ``name`` of the ``SocketManager`` to emit the event through.
        :param topic: The ``topic`` under which the event will be emitted.
        :param message: The ``message`` to be emitted.
        :return: ``None``
        """

        await self._emit(name=name, topic=topic, message=message, serializer=self._msgpack_serializer)

    async def emit_pickle(
        self,
        name: Name,
        topic: Topic,
        message: Message
    ) -> None:
        """
        Emits an event composed of a ``topic`` and a ``message`` through the specified ``SocketManager``.
        The ``message`` will be encoded with the ``Pickle`` serializer.

        :param name: The ``name`` of the ``SocketManager`` to emit the event through.
        :param topic: The ``topic`` under which the event will be emitted.
        :param message: The ``message`` to be emitted.
        :return: ``None``
        """
        await self._emit(name=name, topic=topic, message=message, serializer=self._pickle_serializer)

    async def recv_bytes(
        self,
        name: Name
    ) -> Message:
        """
        Receives an event's ``message`` bytes from the specified ``SocketManager``.

        :param name: The ``name`` of the ``SocketManager`` to receive the event from.
        :return: The received ``message``.
        """

        return await self.socket_managers[name].recv()

    async def recv_json(
        self,
        name: Name
    ) -> Message:
        """
        Receives an event's ``message`` decoded with the ``JSON`` serializer from the specified ``SocketManager``.

        :param name: The ``name`` of the ``SocketManager`` to receive the event from.
        :return: The received ``JSON`` decoded ``message``.
        """

        return await self._recv(name=name, serializer=self._json_serializer)

    async def recv_msgpack(
        self,
        name: Name
    ) -> Message:
        """
        Receives an event's ``message`` decoded with the ``MessagePack`` serializer from the specified ``SocketManager``.

        :param name: The ``name`` of the ``SocketManager`` to receive the event from.
        :return: The received ``MessagePack`` decoded ``message``.
        """

        return await self._recv(name=name, serializer=self._msgpack_serializer)

    async def recv_pickle(
        self,
        name: Name
    ) -> Message:
        """
        Receives an event's ``message`` decoded with the ``Pickle`` serializer from the specified ``SocketManager``.

        :param name: The ``name`` of the ``SocketManager`` to receive the event from.
        :return: The received ``Pickle`` decoded ``message``.
        """

        return await self._recv(name=name, serializer=self._pickle_serializer)

    def boot_socket_managers(self) -> None:
        """
        Boots all ``SocketManager`` associated with this ``AbstractActor`` instance.
        Each ``SocketManager`` is started by calling its ``boot()`` method.

        :return: ``None``
        """

        for name, socket_manager in self.socket_managers.items():
            socket_manager.boot()

    async def stop_socket_managers(self) -> None:
        """
        Stops all ``SocketManager`` associated with this ``AbstractActor`` instance.
        Each ``SocketManager`` is stopped by calling its ``stop()`` method.

        This method iterates over all ``SocketManager`` and stops them without emptying their queues.

        :return: ``None``
        """

        for name, socket_manager in self.socket_managers.items():
            await socket_manager.stop(empty_queue=False)

    async def reboot_socket_managers(self) -> None:
        """
        Reboots all ``SocketManagers`` associated with this ``AbstractActor`` instance.
        Each ``SocketManager`` is rebooted by calling its ``reboot()`` method asynchronously.

        :return: ``None``
        """

        for name, socket_manager in self.socket_managers.items():
            await socket_manager.reboot()

    async def terminate_socket_managers(self) -> None:
        """
        Terminates all ``SocketManager`` associated with this ``AbstractActor`` instance.
        Each ``SocketManager`` is terminated by calling its ``terminate()`` method asynchronously.

        :return: ``None``
        """

        for name, socket_manager in self.socket_managers.items():
            await socket_manager.terminate()

    @abstractmethod
    async def start(self, *args, **kwargs) -> None:
        """
        Starts the ``AbstractActor`` instance by booting all associated ``SocketManager``.
        Child ``AbstractActor``'s implementations must override this method and call ``super().start(*args, **kwargs)``
        to ensure that ``self.boot_socket_managers()`` is properly called before any other methods.

        :return: ``None``
        """

        self.boot_socket_managers()

    async def terminate(self) -> None:
        """
        Terminates the ``AbstractActor`` instance by terminating all associated ``SocketManager`` asynchronously and
        terminating the ZeroMQ Context.

        :return: ``None``
        """

        await self.terminate_socket_managers()

        self._context.term()

        # init
        self.socket_managers = {}
