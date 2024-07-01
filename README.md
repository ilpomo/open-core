![`open-core` header image.](docs/header.jpg)

![Repo size](https://img.shields.io/github/repo-size/ilpomo/open-core?color=70e000)
![License](https://img.shields.io/github/license/ilpomo/open-core?color=70e000)

# open-core: neuron-based processing framework

> Code has to run like the human brain, trillions of individual neurons firing off messages to each other, a massively 
> parallel network with no central control, no single point of failure, yet able to solve immensely difficult problems. 
> And it’s no accident that the future of code looks like the human brain, because the endpoints of every network are, 
> at some level, human brains.
>  
> Pieter Hintjens

`open-core` is a neuron-based processing framework for Python software. It helps you build massively parallel, 
concurrent and asynchronous code that follows the [actor model](https://en.wikipedia.org/wiki/Actor_model) paradigm: 
multiple independent processes emitting and receiving signals to and from each other, asynchronously, without the need 
of a central broker or coordinator. Like neurons.

## Design

- Designed over [the actor model](https://en.wikipedia.org/wiki/Actor_model)
  - Parallelism through multi-processing for CPU bound tasks
  - Concurrency based on multi-threading for I/O bound tasks
  - Concurrency based on Asyncio for network-related tasks
  - Asynchronous [ZeroMQ](https://github.com/zeromq/pyzmq) sockets

## Installation

```sh
pip install open-core
```

## Dependencies

`open-core` will always try to reduce dependencies to the extreme minimum. The current dependencies are specified in 
the `requirements.txt` file::

- **PyZMQ**: Python bindings for ZeroMQ, a high-performance asynchronous messaging library.

Ensure you have the latest versions of these dependencies installed.

## Acknowledgments

To my family, for always supporting me.  
To my girlfriend, for also putting up with me.  
To my friends, for lightening my load during the heaviest moments.  
To the open-source community, for teaching me without asking for anything in return.  
E a Patato, che mi manca in ogni istante.
