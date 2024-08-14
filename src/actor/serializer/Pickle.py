from pickle import dumps, loads, HIGHEST_PROTOCOL
from typing import Any

from src.actor.serializer.AbstractSerializer import AbstractSerializer


class Pickle(AbstractSerializer):
    """
    Pickle serializer implementation for decoding and encoding objects using Pickle format.

    Inherits ``AbstractSerializer`` class for implementing the ``decode()`` and ``encode()`` methods.
    """

    def __init__(self):

        # private
        # public

        pass

    def decode(
        self,
        data: bytes
    ) -> Any:

        return loads(data)

    def encode(
        self,
        obj: Any
    ) -> bytes:

        return dumps(obj=obj, protocol=HIGHEST_PROTOCOL)
