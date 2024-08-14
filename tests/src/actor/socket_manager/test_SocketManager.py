import pytest
from zmq import SUBSCRIBE, UNSUBSCRIBE

from src.actor.socket_manager import SocketManager

NAME = 'sm'


def test_create_endpoints():

    assert SocketManager.get_inproc_endpoint(reference='ref') == 'inproc://ref'
    assert SocketManager.get_ipc_endpoint(reference='ref') == 'ipc:///tmp/ref.ipc'
    assert SocketManager.get_udp_endpoint(ip_address='127.0.0.1', port='8080') == 'udp://127.0.0.1:8080'
    assert SocketManager.get_tcp_endpoint(ip_address='127.0.0.1', port='8080') == 'tcp://127.0.0.1:8080'
    assert SocketManager.get_pgm_endpoint(ip_address='127.0.0.1', port='8080') == 'pgm://127.0.0.1;8080'
    assert SocketManager.get_epgm_endpoint(ip_address='127.0.0.1', port='8080') == 'epgm://127.0.0.1;8080'


def test_bind_and_connect_endpoints(mocker):

    socket = mocker.Mock()
    manager = SocketManager(name=NAME, socket=socket)

    manager.bind_via_inproc(reference='ref')
    socket.bind.assert_called_with(addr=manager.get_inproc_endpoint(reference='ref'))

    manager.connect_via_inproc(reference='ref')
    socket.connect.assert_called_with(addr=manager.get_inproc_endpoint(reference='ref'))


def test_subscribe_and_unsubscribe(mocker):

    socket = mocker.Mock()
    manager = SocketManager(name=NAME, socket=socket)

    topic = b"topic"
    manager.subscribe(topic=topic)
    socket.setsockopt.assert_called_with(SUBSCRIBE, topic)

    manager.unsubscribe(topic=topic)
    socket.setsockopt.assert_called_with(UNSUBSCRIBE, topic)


@pytest.mark.asyncio
async def test_emit_and_receive_messages(mocker):

    socket = mocker.Mock()
    manager = SocketManager(name=NAME, socket=socket)

    await manager.emit(event=b"message")
    assert not manager._emit_queue.empty()

    await manager._recv_queue.put(item=b"response")
    response = await manager.recv()
    assert response == b"response"


@pytest.mark.asyncio
async def test_start_and_stop_background_tasks(mocker):

    socket = mocker.Mock()
    manager = SocketManager(name=NAME, socket=socket)

    manager.bind_via_inproc(reference='ref_0')
    manager.connect_via_inproc(reference='ref_0')

    manager.boot()

    assert manager.is_bidirectional()

    await manager.stop_emitting()
    assert not manager.is_emitting()

    await manager.stop_receiving()
    assert not manager.is_receiving()

    assert not manager.is_bidirectional()
