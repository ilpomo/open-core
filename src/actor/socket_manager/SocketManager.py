from asyncio import CancelledError, Queue, Task, create_task
from typing import Any, Literal

from zmq import Socket, SUBSCRIBE, UNSUBSCRIBE

Name = str
Method = str
Endpoint = str
Topic = bytes
Message = Any

INPROC, IPC, UDP, TCP, PGM, EPGM = 'inproc', 'ipc', 'udp', 'tcp', 'pgm', 'epgm'
BIND, UNBIND, CONNECT, DISCONNECT = 'bind', 'unbind', 'connect', 'disconnect'


class SocketManager:
    """
    A class representing a Socket Manager that handles different types of endpoints and socket operations.
    """

    @staticmethod
    def get_inproc_endpoint(reference: str) -> str:
        """
        Returns the INPROC endpoint based on the provided ``reference``.

        :param reference: The unique identifier used to construct the INPROC endpoint.
        :return: The constructed INPROC endpoint.
        """

        return f"{INPROC}://{reference}"

    @staticmethod
    def get_ipc_endpoint(reference: str) -> str:
        """
        Returns the IPC endpoint based on the provided ``reference``.

        :param reference: The unique identifier used to construct the IPC endpoint.
        :return: The constructed IPC endpoint.
        """

        return f"{IPC}:///tmp/{reference}.ipc"

    @staticmethod
    def get_udp_endpoint(ip_address: str, port: str) -> str:
        """
        Returns the UDP endpoint based on the provided ``ip_address`` and ``port``.

        :param ip_address: The IP address used to construct the UDP endpoint.
        :param port: The port number used to construct the UDP endpoint.
        :return: The constructed UDP endpoint.
        """

        return f"{UDP}://{ip_address}:{port}"

    @staticmethod
    def get_tcp_endpoint(ip_address: str, port: str) -> str:
        """
        Returns the TCP endpoint based on the provided ``ip_address`` and ``port``.

        :param ip_address: The IP address used to construct the TCP endpoint.
        :param port: The port number used to construct the TCP endpoint.
        :return: The constructed TCP endpoint.
        """

        return f"{TCP}://{ip_address}:{port}"

    @staticmethod
    def get_pgm_endpoint(ip_address: str, port: str) -> str:
        """
        Returns the PGM endpoint based on the provided ``ip_address`` and ``port``.

        :param ip_address: The IP address used to construct the PGM endpoint.
        :param port: The port number used to construct the PGM endpoint.
        :return: The constructed PGM endpoint.
        """

        return f"{PGM}://{ip_address};{port}"

    @staticmethod
    def get_epgm_endpoint(ip_address: str, port: str) -> str:
        """
        Returns the EPGM endpoint based on the provided ``ip_address`` and ``port``.

        :param ip_address: The IP address used to construct the EPGM endpoint.
        :param port: The port number used to construct the EPGM endpoint.
        :return: The constructed EPGM endpoint.
        """

        return f"{EPGM}://{ip_address};{port}"

    def __init__(
        self,
        name: Name,
        socket: Socket
    ):
        """
        Initializes a ``SocketManager`` object with the provided ``name`` and ``socket``.

        :param name: The name associated with the SocketManager.
        :param socket: The ZMQ socket object to be managed.
        """

        # private

        self._emit_queue = Queue()
        self._recv_queue = Queue()

        self._emit_task: Task | None = None
        self._recv_task: Task | None = None

        # public

        self.name = name

        self.socket = socket

        self.endpoints: dict[Method, set[Endpoint]] = {
            BIND: set(),
            CONNECT: set(),
            UNBIND: set(),
            DISCONNECT: set()
        }

        self.subscriptions: set[bytes] = set()

    def __str__(self):
        """
        Returns a string representation of the ``SocketManager`` object with its name.

        :return: A formatted string showing the object ``name``.
        """

        return f"{self.__class__.__name__}({self.name})"

    # private

    async def _background_emit(self) -> None:
        """
        Asynchronous method that continuously emits events from the ``self._emit_queue`` via the ``self.socket``.
        Will be used as a concurrent ``asyncio.Task`` to emit all pending messages asynchronously.
        Handles ``CancelledError`` properly for graceful shutdown and prints any other exceptions.

        :return: ``None``
        """

        try:
            while True:

                await self.socket.send_multipart(msg_parts=await self._emit_queue.get())

                self._emit_queue.task_done()

        except CancelledError:
            return None

        except Exception as error:
            print(error)

    async def _background_recv(self) -> None:
        """
        Asynchronous method that continuously receives events from the ``self.socket`` and puts them into the
        ``self._recv_queue``.
        Will be used as a concurrent ``asyncio.Task`` to receive all incoming messages asynchronously.
        Handles ``CancelledError`` for graceful shutdown and prints any other exceptions.

        :return: ``None``
        """

        try:
            while True:

                _, signal = await self.socket.recv_multipart()

                await self._recv_queue.put(item=signal)

        except CancelledError:
            return None

        except Exception as error:
            print(error)

    def _link(
        self,
        method: Literal['bind', 'connect'],
        endpoint: Endpoint
    ) -> None:
        """
        Links the ``self.socket`` to the provided ``endpoint`` using the given ``method``.

        :param method: The method to use for linking, either ``'bind'`` or ``'connect'``.
        :param endpoint: The endpoint to link the socket to.
        :return: ``None``
        """

        if endpoint not in self.endpoints[method]:
            getattr(self.socket, method)(addr=endpoint)

            # update
            self.endpoints[method].add(endpoint)
            self.endpoints[UNBIND if method == BIND else DISCONNECT].add(endpoint)

        else:
            raise ValueError(self, f"Can't {method} the socket multiple times to the endpoint {endpoint}.")

    def _unlink(
        self,
        method: Literal['unbind', 'disconnect'],
        endpoint: Endpoint
    ) -> None:
        """
        Unlinks the ``self.socket`` from the provided ``endpoint`` using the given ``method``.

        :param method: The method to use for unlinking, either ``'unbind'`` or ``'disconnect'``.
        :param endpoint: The endpoint to unlink the socket from.
        :return: ``None``
        """

        if endpoint in self.endpoints[BIND if method == UNBIND else CONNECT]:
            getattr(self.socket, method)(addr=endpoint)

            # update
            self.endpoints[method].remove(endpoint)

        else:
            raise ValueError(self, f"Can't {method} the socket multiple times to the endpoint {endpoint}.")

    # public

    def bind_via_inproc(
        self,
        reference: str
    ) -> None:
        """
        Links the socket to an ``INPROC`` endpoint using the ``'bind'`` method.

        :param reference: The unique identifier used to construct the ``INPROC`` endpoint.
        :return: ``None``
        """

        self._link(method='bind', endpoint=self.get_inproc_endpoint(reference=reference))

    def bind_via_ipc(
        self,
        reference: str
    ) -> None:
        """
        Links the socket to an ``IPC`` endpoint using the ``'bind'`` method.

        :param reference: The unique identifier used to construct the ``INPROC`` endpoint.
        :return: None
        """

        self._link(method='bind', endpoint=self.get_ipc_endpoint(reference=reference))

    def bind_via_udp(
        self,
        ip_address: str,
        port: str
    ) -> None:
        """
        Links the socket to a ``UDP`` endpoint using the ``'bind'`` method.

        :param ip_address: The IP address used to construct the ``UDP`` endpoint.
        :param port: The port number used to construct the ``UDP`` endpoint.
        :return: ``None``
        """

        self._link(method='bind', endpoint=self.get_udp_endpoint(ip_address=ip_address, port=port))

    def bind_via_tcp(
        self,
        ip_address: str,
        port: str
    ) -> None:
        """
        Links the socket to a ``TCP`` endpoint using the ``'bind'`` method.

        :param ip_address: The IP address used to construct the ``TCP`` endpoint.
        :param port: The port number used to construct the ``TCP`` endpoint.
        :return: None
        """

        self._link(method='bind', endpoint=self.get_tcp_endpoint(ip_address=ip_address, port=port))

    def bind_via_pgm(
        self,
        ip_address: str,
        port: str
    ) -> None:
        """
        Links the socket to a ``PGM`` endpoint using the ``'bind'`` method.

        :param ip_address: The IP address used to construct the ``PGM`` endpoint.
        :param port: The port number used to construct the ``PGM`` endpoint.
        :return: ``None``
        """

        self._link(method='bind', endpoint=self.get_pgm_endpoint(ip_address=ip_address, port=port))

    def bind_via_epgm(
        self,
        ip_address: str,
        port: str
    ) -> None:
        """
        Links the socket to an ``EPGM`` endpoint using the ``'bind'`` method.

        :param ip_address: The IP address used to construct the ``EPGM`` endpoint.
        :param port: The port number used to construct the ``EPGM`` endpoint.
        :return: ``None``
        """

        self._link(method='bind', endpoint=self.get_epgm_endpoint(ip_address=ip_address, port=port))

    def connect_via_inproc(
        self,
        reference: str
    ) -> None:
        """
        Links the socket to an ``INPROC`` endpoint using the ``'connect'`` method.

        :param reference: The unique identifier used to construct the ``INPROC`` endpoint.
        :return: ``None``
        """

        self._link(method='connect', endpoint=self.get_inproc_endpoint(reference=reference))

    def connect_via_ipc(
        self,
        reference: str
    ) -> None:
        """
        Links the socket to an ``IPC`` endpoint using the ``'connect'`` method.

        :param reference: The unique identifier used to construct the ``IPC`` endpoint.
        :return: ``None``
        """

        self._link(method='connect', endpoint=self.get_ipc_endpoint(reference=reference))

    def connect_via_udp(
        self,
        ip_address: str,
        port: str
    ) -> None:
        """
        Links the socket to a ``UDP`` endpoint using the ``'connect'`` method.

        :param ip_address: The IP address used to construct the ``UDP`` endpoint.
        :param port: The port number used to construct the ``UDP`` endpoint.
        :return: ``None``
        """

        self._link(method='connect', endpoint=self.get_udp_endpoint(ip_address=ip_address, port=port))

    def connect_via_tcp(
        self,
        ip_address: str,
        port: str
    ) -> None:
        """
        Links the socket to a ``TCP`` endpoint using the ``'connect'`` method.

        :param ip_address: The IP address used to construct the ``TCP`` endpoint.
        :param port: The port number used to construct the ``TCP`` endpoint.
        :return: ``None``
        """

        self._link(method='connect', endpoint=self.get_tcp_endpoint(ip_address=ip_address, port=port))

    def connect_via_pgm(
        self,
        ip_address: str,
        port: str
    ) -> None:
        """
        Links the socket to a ``PGM`` endpoint using the ``'connect'`` method.

        :param ip_address: The IP address used to construct the ``PGM`` endpoint.
        :param port: The port number used to construct the ``PGM`` endpoint.
        :return: ``None``
        """

        self._link(method='connect', endpoint=self.get_pgm_endpoint(ip_address=ip_address, port=port))

    def connect_via_epgm(
        self,
        ip_address: str,
        port: str
    ) -> None:
        """
        Links the socket to an ``EPGM`` endpoint using the ``'connect'`` method.

        :param ip_address: The IP address used to construct the ``EPGM`` endpoint.
        :param port: The port number used to construct the ``EPGM`` endpoint.
        :return: ``None``
        """

        self._link(method='connect', endpoint=self.get_epgm_endpoint(ip_address=ip_address, port=port))

    def unbind(
        self,
        endpoint: Endpoint
    ) -> None:
        """
        Unlinks the socket from the provided endpoint using the ``'unbind'`` method.

        :param endpoint: The endpoint to unbind the socket from.
        :return: ``None``
        """

        self._unlink(method='unbind', endpoint=endpoint)

    def disconnect(
        self,
        endpoint: Endpoint
    ) -> None:
        """
        Unlinks the socket from the provided endpoint using the ``'disconnect'`` method.

        :param endpoint: The endpoint to disconnect the socket from.
        :return: ``None``
        """

        self._unlink(method='disconnect', endpoint=endpoint)

    def subscribe(
        self,
        topic: bytes
    ) -> None:
        """
        Subscribe to a new ``topic`` by adding it to the ``self.subscriptions`` if not already subscribed.

        :param topic: The topic to subscribe to as bytes.
        :return: ``None``
        """

        if topic not in self.subscriptions:

            self.socket.setsockopt(SUBSCRIBE, topic)

            # update
            self.subscriptions.add(topic)

        else:
            print(self, f"Can't subscribe to the topic {topic}, already subscribed.")

    def unsubscribe(
        self,
        topic: bytes
    ) -> None:
        """
        Unsubscribes from a specified ``topic`` by removing it from the ``self.subscriptions`` if already subscribed.

        :param topic: The topic to unsubscribe from as bytes.
        :return: ``None``
        """

        if topic in self.subscriptions:

            self.socket.setsockopt(UNSUBSCRIBE, topic)

            # update
            self.subscriptions.remove(topic)

        else:
            print(self, f"Can't unsubscribe to the topic {topic}, not subscribed yet.")

    async def emit(
        self,
        event: tuple[bytes, bytes]
    ) -> None:
        """
        Asynchronously adds the provided event to the ``self._emit_queue`` for sending via the socket.

        :param event: A tuple of bytes - ``topic`` first, then the serialized ``message`` - representing the event to be
        emitted.
        :return: ``None``
        """

        await self._emit_queue.put(item=event)

    async def recv(self) -> bytes:
        """
        Asynchronously retrieves and returns an event's ``message`` from the ``self._recv_queue``.
        The event's ``topic`` has already been filtered out by the background receiver task.

        :return: The event's ``message`` retrieved from the queue as bytes.
        """

        r = await self._recv_queue.get()
        self._recv_queue.task_done()

        return r

    def is_emitting(self) -> bool:
        """
        Checks if the ``SocketManager`` is currently emitting events, which means that the background emitter task has
        been booted.

        :return: ``True`` if emitting events, ``False`` otherwise.
        """

        return self._emit_task is not None

    def is_receiving(self) -> bool:
        """
        Checks if the ``SocketManager`` is currently receiving events, which means that the background receiver task has
        been booted.

        :return: ``True`` if receiving events, ``False`` otherwise.
        """

        return self._recv_task is not None

    def is_bidirectional(self) -> bool:
        """
        Checks if the ``SocketManager`` is currently bidirectional, which means that both the background emitter task
        and the background receiver task have been booted.

        :return: ``True`` if bidirectional, ``False`` otherwise.
        """

        return self.is_emitting() and self.is_receiving()

    def boot(self) -> None:
        """
        Boots the ``SocketManager`` by starting both the background emitter and receiver tasks if not already running.
        Prints a message if any of them are already running.

        :return: ``None``
        """

        if self.endpoints[BIND]:
            if not self.is_emitting():
                self._emit_task = create_task(coro=self._background_emit())

            else:
                print(self, "The emitter is already running.")

        if self.endpoints[CONNECT]:
            if not self.is_receiving():
                self._recv_task = create_task(coro=self._background_recv())

            else:
                print(self, "The receiver is already running.")

    async def stop_emitting(self) -> None:
        """
        Stops the emission of events by canceling the background emitter task if it is currently running.
        If the task is canceled, sets the task to ``None``.

        :return: ``None``
        """

        if self.is_emitting():
            self._emit_task.cancel()

            try:
                await self._emit_task

            except CancelledError:
                pass

            finally:
                self._emit_task = None

    async def stop_receiving(self) -> None:
        """
        Stops the reception of events by canceling the background receiver task if it is currently running.
        If the task is canceled, sets the task to ``None``.

        :return: ``None``
        """

        if self.is_receiving():
            self._recv_task.cancel()

            try:
                await self._recv_task

            except CancelledError:
                pass

            finally:
                self._recv_task = None

    def empty_queues(self) -> None:
        """
        Empties the ``self._recv_queue`` and ``self._emit_queue`` by recreating them as new instances of
        ``asyncio.Queue``.

        :return: ``None``
        """

        del self._recv_queue
        del self._emit_queue

        self._recv_queue = Queue()
        self._emit_queue = Queue()

    async def stop(
        self,
        empty_queue: bool
    ) -> None:
        """
        Stops both the emission and reception of events by canceling their respective background tasks if running.
        If specified, empties the event queues by recreating them as new instances of ``asyncio.Queue``.

        :param empty_queue: A boolean indicating whether to empty the event queues.
        :return: ``None``
        """

        await self.stop_emitting()
        await self.stop_receiving()

        if empty_queue:
            self.empty_queues()

    async def reboot(self) -> None:
        """
        Stops both the emission and reception of events by canceling their respective background tasks if running.
        Empties the event queues by recreating them as new instances of ``asyncio.Queue``.
        Then, reboots the ``SocketManager`` by starting both the background emitter and receiver tasks.

        :return: ``None``
        """

        await self.stop(empty_queue=True)
        self.boot()

    async def terminate(self) -> None:
        """
        Terminates the ``SocketManager`` by stopping event emission and reception, unlinking all endpoints, and closing
        the socket.

        :return: ``None``
        """

        await self.stop(empty_queue=True)

        for method, endpoints in self.endpoints.items():
            for endpoint in endpoints:
                self._unlink(method='unbind' if method == BIND else 'disconnect', endpoint=endpoint)

            # init
            self.endpoints[method].clear()

        self.socket.close()
