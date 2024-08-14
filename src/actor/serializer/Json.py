from typing import Any

from msgspec import DecodeError
from msgspec.json import Decoder, Encoder

from src.actor.serializer.AbstractSerializer import AbstractSerializer


class Json(AbstractSerializer):
    """
    JSON serializer implementation for decoding and encoding objects using JSON format.

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

        try:
            return self._decoder.decode(data)

        except DecodeError:
            return None

    def encode(
        self,
        obj: Any
    ) -> bytes:

        return self._encoder.encode(obj)
