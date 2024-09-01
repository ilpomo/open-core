![`open-core` header image.](asset/header.jpg)

[![Build](https://github.com/ilpomo/open-core/actions/workflows/build.yml/badge.svg)]()
[![Tests](https://github.com/ilpomo/open-core/actions/workflows/tests.yml/badge.svg)]()
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ilpomo_open-core&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ilpomo_open-core)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=ilpomo_open-core&metric=bugs)](https://sonarcloud.io/summary/new_code?id=ilpomo_open-core)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=ilpomo_open-core&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=ilpomo_open-core)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=ilpomo_open-core&metric=coverage)](https://sonarcloud.io/summary/new_code?id=ilpomo_open-core)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=ilpomo_open-core&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=ilpomo_open-core)

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

### Step 0: think about the *who* and the *how*

Deconstruct the problem into its smaller parts.
Think about the responsibilities: who should take care of each part? 
Think about the information flow: how the data is moving between each part?
Think about the blocking computation: how can these parts be scaled if necessary?

### Step 1: define the *actors*

Create an actor implementation by simply inheriting from the `AbstractActor` class.
Define its `start(...)` abstract coroutine that represent what the actor will do once it is up and running.

### Step 2: define the *services*

For each actor implementation, create a function and inside this function:
1. Create an instance of the actor;
2. Define how the actor will exchange events with the other actors in the network:
   1. Create one or more `SocketManager` instances;
   2. Bind or connect all `SocketManager` instances depending on the chosen [ZeroMQ pattern](https://zguide.zeromq.org/docs/chapter1/); 
3. Start the actor by using the built-in `start_actor(...)` utility function.

These functions hosting a living actor will be the services.

### Step 3: define the *processes*

To run each service independently of each other, pass each one of them to a dedicated `multiprocessing.Process()` as a
target function.
Run the processes and enjoy.

### Step 4: improve the *architecture*

Test it and redesign it accordingly.
Designing an optimized software architecture is a work of Art and labor limae,
but no matter what, in the end this is one will be achieved thanks to `open-core`:
- An architecture based on [the actor model](https://en.wikipedia.org/wiki/Actor_model);
- Services with a single, well-defined responsibility;
- Parallelism based on multiprocessing for all services, no matter if CPU-bound or not;
- Concurrency based on threading for I/O-bound tasks inside each service;
- Concurrency based on asyncio for network-related tasks;

## Installation

### Installing from `main` branch

The latest version of `open-core` can be installed directly from the `main` branch on GitHub
using the following command:

```shell
pip install git+https://github.com/ilpomo/open-core.git
```

### Installing from `vX.X.Z` release version

To install a specific release version of `open-core`, just edit `vX.Y.Z` with the desired release's tag:

```shell
pip install https://github.com/ilpomo/open-core/archive/refs/tags/vX.Y.Z.tar.gz
```

### Installing for Contributors (with tests and development dependencies)

Contributors need to install the project with the tests folder and additional development dependencies by following 
these steps:

#### Clone the repository:

First, clone the repository to the local machine:

```shell
git clone https://github.com/ilpomo/open-core.git
```

#### Install the package with development dependencies:

Navigate to the cloned repository directory and install the package with the development dependencies:

```shell
pip install -e .[dev]
```

This command installs the package in editable mode (-e) along with the dependencies listed under the [dev] extras in 
the `pyproject.toml` file.

#### Run the tests:

Run the tests to ensure everything is set up correctly:

```shell
pytest
```

## Dependencies

### Standard Dependencies

- [msgspec](https://github.com/jcrist/msgspec): A fast serialization and validation library, with builtin support for 
JSON, MessagePack, YAML, and TOML.
- [PyZMQ](https://github.com/zeromq/pyzmq): Python bindings for ZeroMQ.
- [uvloop](https://github.com/MagicStack/uvloop): Ultra fast asyncio event loop.
  <sub>(**NOTE**: not available on Windows, fallback to Python default asyncio event loop.)</sub>

### Development Dependencies

- [pytest](https://github.com/pytest-dev/pytest): The pytest framework makes it easy to write small tests, yet scales 
to support complex functional testing.
- [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio): Asyncio support for pytest.
- [pytest-cov](https://github.com/pytest-dev/pytest-cov): Pytest plugin for measuring coverage.
- [pytest-mock](https://github.com/pytest-dev/pytest-mock): Thin-wrapper around the mock package for easier use with 
pytest.
- [ruff](https://github.com/charliermarsh/ruff): An extremely fast Python linter.

## Acknowledgments

To my family, for always supporting me.  
To my girlfriend, for also putting up with me.  
To my friends, for lightening my load during the heaviest moments.  
To the open-source community, for teaching me without asking for anything in return.  
E a Patato, che mi manca in ogni istante.