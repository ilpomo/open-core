import sys
from asyncio import BaseEventLoop, run, set_event_loop_policy

from src.actor import AbstractActor


def setup_event_loop() -> None:
    """
    Sets up the event loop policy based on the platform.
    If the platform is not ``'win32'``, attempts to set ``uvloop`` as the event loop policy.
    If ``uvloop`` is not installed, falls back to the default asyncio event loop.

    :return: ``None``
    """

    if sys.platform != 'win32':

        try:
            from uvloop import EventLoopPolicy

            set_event_loop_policy(policy=EventLoopPolicy())

        except ImportError:
            # uvloop is not installed, fallback to default asyncio event loop
            pass


def start_actor(
    actor: AbstractActor,
    event_loop: BaseEventLoop | None,
    **kwargs
) -> None:
    """
    Starts the ``actor`` by running its ``start()`` method using the provided ``event_loop`` or setting up a new event
    loop if none is provided.
    If the ``actor`` is interrupted by a ``KeyboardInterrupt``, it is terminated.

    :param actor: The ``AbstractActor`` instance to start.
    :param event_loop: The ``event_loop`` to use for running the ``actor``'s ``start()`` method.
    :param kwargs: Additional keyword arguments to pass to the ``actor``'s ``start()`` method.
    :return: ``None``
    """

    try:
        if event_loop is not None:
            event_loop.run_until_complete(future=actor.start(**kwargs))

        else:
            setup_event_loop()

            run(main=actor.start(**kwargs))

            run(main=actor.terminate())

    except KeyboardInterrupt:
        run(main=actor.terminate())
