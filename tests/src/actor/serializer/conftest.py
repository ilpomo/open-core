import pytest

from src.actor.serializer import Json, MessagePack, Pickle


@pytest.fixture(params=[Json, MessagePack, Pickle])
def serializer(request) -> Json | MessagePack | Pickle:
    return request.param()


@pytest.fixture
def json_serializer() -> Json:
    return Json()


@pytest.fixture
def msgpack_serializer() -> MessagePack:
    return MessagePack()


@pytest.fixture
def pickle_serializer() -> Pickle:
    return Pickle()
