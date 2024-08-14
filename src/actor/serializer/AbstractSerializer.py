from abc import ABC, abstractmethod
from typing import Any


class AbstractSerializer(ABC):
    """
    ``AbstractSerializer`` class for decoding and encoding events to be emitted and received.
    Each ``AbstractSerializer`` implementation must override and implement the ``decode()`` and ``encode()`` methods.
    """

    @abstractmethod
    def decode(
        self,
        data: bytes
    ) -> Any:
        """
        Decode the input data and return the corresponding deserialized object.

        :param data: The data to be decoded.
        :return: The deserialized object.
        """

        ...

    @abstractmethod
    def encode(
        self,
        obj: Any
    ) -> bytes:
        """
        Encode the input object and return the corresponding serialized data.

        :param obj: The object to be encoded.
        :return: The serialized data.
        """

        ...
