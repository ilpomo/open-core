![`open-core` header image.](asset/header.jpg)

![Repo size](https://img.shields.io/github/repo-size/ilpomo/open-core?color=70e000)
![License](https://img.shields.io/github/license/ilpomo/open-core?color=70e000)

# open-core: neuron-based processing framework

> Code has to run like the human brain, trillions of individual neurons firing off messages to each other, a massively 
> parallel network with no central control, no single point of failure, yet able to solve immensely difficult problems. 
> And it’s no accident that the future of code looks like the human brain, because the endpoints of every network are, 
> at some level, human brains.
>  
> Pieter Hintjens

`open-core` is an event-based processing framework for Python software.
It helps build massively parallel, concurrent, and asynchronous code that follows the [actor model](https://en.wikipedia.org/wiki/Actor_model) paradigm: 
multiple independent asynchronous process services emitting and receiving events to and from each other, without the 
need of a central broker or coordinator.
It tries to achieve this in the most intuitive, simple, and straightforward possible way.

## Design

- Designed over [the actor model](https://en.wikipedia.org/wiki/Actor_model)
  - Parallelism through multi-processing for CPU bound tasks
  - Concurrency based on multi-threading for I/O bound tasks
  - Concurrency based on Asyncio for network-related tasks
  - Asynchronous [ZeroMQ](https://github.com/zeromq/pyzmq) contexts and sockets

## Installation

```sh
pip install open-core
```

## Dependencies

`open-core` will always try to reduce dependencies to the extreme minimum. The current dependencies are specified in 
the `requirements.txt` file::

- [msgspec](https://github.com/jcrist/msgspec): A fast serialization and validation library, with builtin support for JSON, MessagePack, YAML, and TOML.
- [PyZMQ](https://github.com/zeromq/pyzmq): Python bindings for ZeroMQ.
- [Pytest](https://github.com/pytest-dev/pytest): The pytest framework makes it easy to write small tests, yet scales to support complex functional testing.

### Installing dependencies through the requirements.txt file

```sh
pip install -r requirements.txt
```

## Acknowledgments

To my family, for always supporting me.  
To my girlfriend, for also putting up with me.  
To my friends, for lightening my load during the heaviest moments.  
To the open-source community, for teaching me without asking for anything in return.  
E a Patato, che mi manca in ogni istante.
