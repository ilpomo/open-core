![`open-core` header image.](asset/header.jpg)

<p align="center">
   <a href="https://github.com/ilpomo/open-core/actions/workflows/python-app.yml">
      <img src="https://github.com/ilpomo/open-core/actions/workflows/python-app.yml/badge.svg">
   </a>
   <a href="https://github.com/ilpomo/open-core/">
      <img src="https://img.shields.io/github/repo-size/ilpomo/open-core?color=70e000">
   </a>
   <a href="https://github.com/ilpomo/open-core/blob/main/LICENSE">
      <img src="https://img.shields.io/github/license/ilpomo/open-core?color=70e000">
   </a>
</p>

# open-core: event-based processing framework

> Code has to run like the human brain, trillions of individual neurons firing off messages to each other, a massively 
> parallel network with no central control, no single point of failure, yet able to solve immensely difficult problems.
> \
> And it’s no accident that the future of code looks like the human brain, because the endpoints of every network are, 
> at some level, human brains.
> \
> \
> Pieter Hintjens

`open-core` is a Python framework to easily build **massively parallel**, **concurrent**, and **asynchronous 
event-based** code that follows [**the actor model**](https://en.wikipedia.org/wiki/Actor_model):
multiple independent asynchronous process services hosting actors that exchanges events between them, without the need 
of a central broker or coordinator.
It tries to achieve this in the most intuitive, simple, and straightforward possible way.

### What is it all about in really simple terms?

`open-core` is a Python framework containing ready-to-use building blocks to develop **high-performance** Python code.
Writing high-performance Python code is complex and requires a good knowledge of many different low-level concepts and 
tools:
[Global Interpreter Lock (GIL)](https://wiki.python.org/moin/GlobalInterpreterLock), 
[multiprocessing](https://docs.python.org/3/library/multiprocessing.html), 
[threading](https://docs.python.org/3/library/threading.html),
[asyncio](https://docs.python.org/3/library/asyncio.html),
[concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html) and many others.

Choosing the right combination of tools may be complex, confusing, and time-consuming for a lot of developers.

`open-core` aims to simplify this complexity by providing just enough functionalities out of the box so developers can 
focus on what they do best – writing great software instead of reinventing the wheel every time.
It is based on the [Python Standard Library](https://docs.python.org/3/library/index.html) and some other great 
third-party libraries, like [msgspec](https://github.com/jcrist/msgspec), [PyZMQ](https://github.com/zeromq/pyzmq), and
[uvloop](https://github.com/MagicStack/uvloop).

## How-To

### Step 0: think about the *_who_* and the *_how_*

Deconstruct the problem into its smaller parts.
Think about the responsibilities: who should take care of each part? 
Think about the information flow: how the data is moving between each part?
Think about the blocking computation: how can these parts be scaled if necessary?

### Step 1: define the *_actors_*

Create an actor implementation by simply inheriting from the `AbstractActor` class.
Define its `start(...)` abstract coroutine that represent what the actor will do once it is up and running.

### Step 2: define the *_services_*

For each actor implementation, create a function and inside this function:
1. Create an instance of the actor;
2. Define how the actor will exchange events with the other actors in the network:
   1. Create one or more `SocketManager` instances;
   2. Bind or connect all `SocketManager` instances depending on the chosen [ZeroMQ pattern](https://zguide.zeromq.org/docs/chapter1/); 
3. Start the actor by using the built-in `start_actor(...)` utility function.

These functions hosting a living actor will be the services.

### Step 3: define the *_processes_*

To run each service independently of each other, pass each one of them to a dedicated `multiprocessing.Process()` as a
target function.
Run the processes and enjoy.

### Step 4: improve the *_architecture_*

Test it and redesign it accordingly.
Designing an optimized software architecture is a work of Art and labor limae,
but no matter what, in the end this is one will be achieved thanks to `open-core`:
- An architecture based on [the actor model](https://en.wikipedia.org/wiki/Actor_model);
- Services with a single, well-defined responsibility;
- Parallelism based on multiprocessing for all services, no matter if CPU-bound or not;
- Concurrency based on threading for I/O-bound tasks inside each service;
- Concurrency based on asyncio for network-related tasks;

## Installation

`open-core` ~~is listed~~ in The Python Package Index (PyPI), so ~~it is~~ possible to get it using `pip`, 
but the tests folder is not included in the default package.
To run the tests, it is necessary to clone this repository.

### Using pip (without tests):

```sh
pip install open-core
```

### Using the full repository (with tests):

```commandline
git clone https://github.com/ilpomo/open-core.git
```

## Dependencies

`open-core` will always reduce dependencies to the extreme minimum.

For end users, the dependencies are specified in the `requirements.txt` file:

- [msgspec](https://github.com/jcrist/msgspec): A fast serialization and validation library, with builtin support for 
JSON, MessagePack, YAML, and TOML.
- [PyZMQ](https://github.com/zeromq/pyzmq): Python bindings for ZeroMQ.
- [uvloop](https://github.com/MagicStack/uvloop): Ultra fast asyncio event loop.

For contributors, the extra dependencies for testing are specified in the `requirements-dev.txt` file.

- [pytest](https://github.com/pytest-dev/pytest): The pytest framework makes it easy to write small tests, yet scales 
to support complex functional testing.
- [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio): Asyncio support for pytest.
- [pytest-mock](https://github.com/pytest-dev/pytest-mock): Thin-wrapper around the mock package for easier use with pytest
- [setuptools](https://github.com/pypa/setuptools): The Setuptools build system.

### Installing dependencies through the requirements.txt file

```sh
pip install -r requirements.txt  # for end users
pip install -r requirements-dev.txt  # also necessary for contributors
```

## Acknowledgments

To my family, for always supporting me.  
To my girlfriend, for also putting up with me.  
To my friends, for lightening my load during the heaviest moments.  
To the open-source community, for teaching me without asking for anything in return.  
E a Patato, che mi manca in ogni istante.