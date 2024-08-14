from typing import Any

from msgspec.msgpack import Decoder
from msgspec.msgpack import Encoder

from src.actor.serializer.AbstractSerializer import AbstractSerializer


class MessagePack(AbstractSerializer):
    """
    MessagePack serializer implementation for decoding and encoding objects using MessagePack format.

    Inherits ``AbstractSerializer`` class for implementing the ``decode()`` and ``encode()`` methods.
    """

    def __init__(self):

        # private

        self._decoder = Decoder()
        self._encoder = Encoder()

        # public

    def decode(
        self,
        data: bytes
    ) -> Any:

        return self._decoder.decode(data)

    def encode(
        self,
        obj: Any
    ) -> bytes:

        return self._encoder.encode(obj)
