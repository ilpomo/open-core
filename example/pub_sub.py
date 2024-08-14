from asyncio import sleep
from datetime import datetime
from multiprocessing import Process, set_start_method

from src.actor import AbstractActor, start_actor


# How to create two independent asynchronous Python processes services exchanging events to each other using the
# PUB/SUB pattern?

# First, create two different AbstractActor implementations:
# 1) The first one representing the publisher actor that will live in the publisher process service.
# 2) The second one representing the subscriber actor that will live in the subscriber process service.


class PubActor(AbstractActor):

    # Inherit from AbstractActor to create an implementation. The behavior of the implementation will be determined by
    # what it will do in its start() method.
    # Since this implementation has been called PubActor, one should expect that inside the start() method there will
    # be some code related to events emission (publication).

    async def start(
        self,
        throttle: int | float
    ) -> None:

        # The following super().start() call ensures that the background emitter asyncio Task will be properly booted.

        await super().start()

        # A good practice with ZeroMQ sockets is to await a little bit to ensure that the receiving side - in this case
        # the SUB socket of the SubActor defined below - will be ready to receive the emitted events; otherwise it may
        # happen that some events may be lost if the connection is not established fast enough.

        await sleep(delay=5)

        # 10 simple events will be asynchronously emitted.
        # One may be wondering why an apparently random 'pub' SocketManager has been chosen for emitting these events.
        # The reason is that in the 'pub_service0 implementation below -
        # the function where the PubActor is going to live (and die) - a SocketManager named 'pub' has been created and
        # bound to a proper IPC endpoint.

        topic = b''

        for i in range(10):

            message = i

            # Choose the preferred serialization method between JSON, MessagePack, or Pickle.

            print(datetime.now(), self, f"Emitting the event ({topic}, {message}).")

            await self.emit_pickle(name='pub', topic=topic, message=message)

            # Throttle simulates a little delay between each event emission caused by some required computation.

            await sleep(delay=throttle)

        # Emits an event to inform the SubActor - defined below - that it can interrupt its execution and stop.

        print(datetime.now(), self, f"Emitting the termination event ({topic}, 'terminate').")

        await self.emit_pickle(name='pub', topic=topic, message='terminate')

        # Again, simulates some computation required before exiting the current method.

        print(datetime.now(), self, "Simulating closing computations for 5 seconds.")

        await sleep(delay=5)

        print(datetime.now(), self, "Bye.")


class SubActor(AbstractActor):

    # Inherit from AbstractActor to create an implementation. The behavior of the implementation will be determined by
    # what it will do in its start() method.
    # Since this implementation has been called SubActor, one should expect that inside the start() method there will
    # be some code related to events reception (subscription).

    async def start(self, *args, **kwargs) -> None:

        # The following super().start() call ensures that the background emitter asyncio Task will be properly booted.

        await super().start()

        # A good practice with ZeroMQ sockets is to await a little bit to ensure that the receiving side - in this case
        # the current SubActor 'sub' socket defined below - will be ready to receive the emitted events; otherwise it
        # may happen that some events may be lost if the connection is not established fast enough.
        # That is the reason why here it is not awaiting anything.

        while True:

            # The Pickle deserialization method has been chosen since it is known that the PubActor will emit events
            # using the same method for serialization.

            msg = await self.recv_pickle(name='sub')

            print(datetime.now(), self, f"Received the event's message '{msg}'.")

            # No explanation needed here, right?

            if msg == 'terminate':
                break

        # Again, simulates some computation required before exiting the current method.

        print(datetime.now(), self, "Simulating closing computations for 5 seconds.")

        await sleep(delay=5)

        print(datetime.now(), self, "Bye.")


# So far two AbstractActor implementations have been defined - PubActor and SubActor - but where and how are they gone
# to be run?
# The goal is to have two independent asynchronous process services exchange events to each other using the PUB/SUB
# pattern; the 'PUB/SUB pattern' part seems to been solved by implementing the PubActor and SubActor, but what about
# the rest?
# How can everything - actors, services, and processes - be put together? Think about this:
# 1) A Python multiprocessing.Process class requires a target function as an argument, otherwise it cannot be started.
# 2) An Actor instance requires a place to exist to do the tasks it has been designed for.
# Two functions will now be defined below that will both be passed to two multiprocessing.Process as targets.
# Inside each one, the respective Actor will be instantiated and its start() method will be called.
# These two functions run as independent asynchronous processes are going to be the so-called services.


def pub_service() -> None:

    # Step 1: actor instantiation.

    actor = PubActor(name='PubActor')

    # Step 2: SocketManager creation.

    actor.create_pub_socket_manager(name='pub')

    # Step 3: SocketManager link using the ZeroMQ 'bind' method since it is a PUB type socket.

    actor['pub'].bind_via_ipc(reference='a_unique_identifier_name')

    # Step 4: start the Actor without caring about anything else.

    start_actor(actor=actor, event_loop=None, throttle=0.05)

    # Done. Pretty easy, right?


def sub_service() -> None:

    # Step 1: actor instantiation.

    actor = SubActor(name='SubActor')

    # Step 2: SocketManager creation.

    actor.create_sub_socket_manager(name='sub')

    # Step 3: Subscribe the SocketManager to a generic b'' topic.

    actor['sub'].subscribe(topic=b'')

    # Step 4: SocketManager link using the ZeroMQ 'connect' method since it is a SUB type socket.

    actor['sub'].connect_via_ipc(reference='a_unique_identifier_name')

    # Step 5: start the Actor without caring about anything else.

    start_actor(actor=actor, event_loop=None)

    # Done. Pretty easy, right?


# Two actors with specific behavior have been defined: PubActor and SubActor.
# Two services with specific behaviors have also been defined: pub_service and sub_service.
# How to run them?


if __name__ == '__main__':

    set_start_method(method="spawn")

    # Define the multiprocess.Process that will run the pub_service target function hosting the PubActor.

    pub = Process(target=pub_service)

    # Define the multiprocess.Process that will run the pub_service target function hosting the PubActor.

    sub = Process(target=sub_service)

    # Finally, start the two independent asynchronous process services.

    pub.start()
    sub.start()

    # Wait for their completion.

    pub.join()
    sub.join()

    # Enjoy.
