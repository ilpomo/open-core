import pytest

from src.actor import AbstractActor


@pytest.fixture
def actor() -> AbstractActor:

    class Actor(AbstractActor):

        async def start(self, *args, **kwargs) -> None:
            # basic abc implementation
            pass

    return Actor()
