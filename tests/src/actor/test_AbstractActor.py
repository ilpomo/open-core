import pytest
from zmq import TYPE, PAIR, PUB, SUB, REQ, REP, DEALER, ROUTER, PUSH, PULL

NAME = 'sm'

SOCKET_TYPES = (PAIR, PUB, SUB, REQ, REP, DEALER, ROUTER, PUSH, PULL,)
TO_BIND_SOCKET_TYPES = (PAIR, PUB, REP, ROUTER, PULL,)
TO_CONNECT_SOCKET_TYPES = (PAIR, SUB, REQ, DEALER, PUSH,)

BIND, CONNECT, UNBIND, DISCONNECT = 'bind', 'connect', 'unbind', 'disconnect'
REFERENCE, IP_ADDRESS, PORT = 'reference', '127.0.0.1', '5555'


def test_create_pair_socket_manager(actor):

    actor.create_pair_socket_manager(name=NAME)

    assert NAME in actor.socket_managers


def test_create_pub_socket_manager(actor):

    actor.create_pub_socket_manager(name=NAME)

    assert NAME in actor.socket_managers


def test_create_sub_socket_manager(actor):

    actor.create_sub_socket_manager(name=NAME)

    assert NAME in actor.socket_managers


def test_create_req_socket_manager(actor):

    actor.create_req_socket_manager(name=NAME)

    assert NAME in actor.socket_managers


def test_create_rep_socket_manager(actor):

    actor.create_rep_socket_manager(name=NAME)

    assert NAME in actor.socket_managers


def test_create_dealer_socket_manager(actor):

    actor.create_dealer_socket_manager(name=NAME)

    assert NAME in actor.socket_managers


def test_create_router_socket_manager(actor):

    actor.create_router_socket_manager(name=NAME)

    assert NAME in actor.socket_managers


def test_create_push_socket_manager(actor):

    actor.create_push_socket_manager(name=NAME)

    assert NAME in actor.socket_managers


def test_create_pull_socket_manager(actor):

    actor.create_pull_socket_manager(name=NAME)

    assert NAME in actor.socket_managers


@pytest.mark.parametrize('socket_type', SOCKET_TYPES)
def test_create_socket_manager(actor, socket_type):

    actor.create_socket_manager(name=NAME, socket_type=socket_type)

    assert actor[NAME].socket.getsockopt(option=TYPE) == socket_type


def test_create_socket_manager_duplicate_name(actor):

    actor.create_pair_socket_manager(name=NAME)

    with pytest.raises(ValueError):
        actor.create_pair_socket_manager(name=NAME)


def test_create_socket_manager_invalid_type(actor):

    with pytest.raises(ValueError):
        actor.create_socket_manager(name=NAME, socket_type=9999)


@pytest.mark.asyncio
async def test_emit_uninitialized_socket_manager(actor):

    with pytest.raises(KeyError):
        await actor.emit_json(name=NAME, topic=b"topic", message={'key': 'value'})


@pytest.mark.asyncio
async def test_recv_uninitialized_socket_manager(actor):

    with pytest.raises(KeyError):
        await actor.recv_json(name=NAME)


@pytest.mark.asyncio
async def test_remove_socket_manager(actor):

    actor.create_pub_socket_manager(name=NAME)

    assert NAME in actor.socket_managers

    await actor.remove_socket_manager(name=NAME)

    assert NAME not in actor.socket_managers


@pytest.mark.parametrize('socket_type', TO_BIND_SOCKET_TYPES)
def test_bind_socket_manager_via_inproc(actor, socket_type, mocker):

    actor.create_socket_manager(name=NAME, socket_type=PUB)

    mock_link = mocker.patch.object(actor[NAME], '_link')

    actor[NAME].bind_via_inproc(reference=REFERENCE)

    mock_link.assert_called_once_with(method=BIND, endpoint=actor[NAME].get_inproc_endpoint(reference=REFERENCE))


@pytest.mark.parametrize('socket_type', TO_BIND_SOCKET_TYPES)
def test_bind_socket_manager_via_ipc(actor, socket_type, mocker):

    actor.create_socket_manager(name=NAME, socket_type=socket_type)

    mock_link = mocker.patch.object(actor[NAME], '_link')

    actor[NAME].bind_via_ipc(reference=REFERENCE)

    mock_link.assert_called_once_with(method=BIND, endpoint=actor[NAME].get_ipc_endpoint(reference=REFERENCE))


@pytest.mark.parametrize('socket_type', TO_BIND_SOCKET_TYPES)
def test_bind_socket_manager_via_udp(actor, socket_type, mocker):

    actor.create_socket_manager(name=NAME, socket_type=socket_type)

    mock_link = mocker.patch.object(actor[NAME], '_link')

    actor[NAME].bind_via_udp(ip_address=IP_ADDRESS, port=PORT)

    mock_link.assert_called_once_with(method=BIND, endpoint=actor[NAME].get_udp_endpoint(ip_address=IP_ADDRESS, port=PORT))


@pytest.mark.parametrize('socket_type', TO_BIND_SOCKET_TYPES)
def test_bind_socket_manager_via_tcp(actor, socket_type, mocker):

    actor.create_socket_manager(name=NAME, socket_type=socket_type)

    mock_link = mocker.patch.object(actor[NAME], '_link')

    actor[NAME].bind_via_tcp(ip_address=IP_ADDRESS, port=PORT)

    mock_link.assert_called_once_with(method=BIND, endpoint=actor[NAME].get_tcp_endpoint(ip_address=IP_ADDRESS, port=PORT))


@pytest.mark.parametrize('socket_type', TO_BIND_SOCKET_TYPES)
def test_bind_socket_manager_via_pgm(actor, socket_type, mocker):

    actor.create_socket_manager(name=NAME, socket_type=socket_type)

    mock_link = mocker.patch.object(actor[NAME], '_link')

    actor[NAME].bind_via_pgm(ip_address=IP_ADDRESS, port=PORT)

    mock_link.assert_called_once_with(method=BIND, endpoint=actor[NAME].get_pgm_endpoint(ip_address=IP_ADDRESS, port=PORT))


@pytest.mark.parametrize('socket_type', TO_BIND_SOCKET_TYPES)
def test_bind_socket_manager_via_epgm(actor, socket_type, mocker):

    actor.create_socket_manager(name=NAME, socket_type=socket_type)

    mock_link = mocker.patch.object(actor[NAME], '_link')

    actor[NAME].bind_via_epgm(ip_address=IP_ADDRESS, port=PORT)

    mock_link.assert_called_once_with(method=BIND, endpoint=actor[NAME].get_epgm_endpoint(ip_address=IP_ADDRESS, port=PORT))


@pytest.mark.parametrize('socket_type', TO_CONNECT_SOCKET_TYPES)
def test_connect_socket_manager_via_inproc(actor, socket_type, mocker):

    actor.create_socket_manager(name=NAME, socket_type=socket_type)

    mock_link = mocker.patch.object(actor[NAME], '_link')

    actor[NAME].connect_via_inproc(reference=REFERENCE)

    mock_link.assert_called_once_with(method=CONNECT, endpoint=actor[NAME].get_inproc_endpoint(reference=REFERENCE))


@pytest.mark.parametrize('socket_type', TO_CONNECT_SOCKET_TYPES)
def test_connect_socket_manager_via_ipc(actor, socket_type, mocker):

    actor.create_socket_manager(name=NAME, socket_type=socket_type)

    mock_link = mocker.patch.object(actor[NAME], '_link')

    actor[NAME].connect_via_ipc(reference=REFERENCE)

    mock_link.assert_called_once_with(method=CONNECT, endpoint=actor[NAME].get_ipc_endpoint(reference=REFERENCE))


@pytest.mark.parametrize('socket_type', TO_CONNECT_SOCKET_TYPES)
def test_connect_socket_manager_via_udp(actor, socket_type, mocker):

    actor.create_socket_manager(name=NAME, socket_type=socket_type)

    mock_link = mocker.patch.object(actor[NAME], '_link')

    actor[NAME].connect_via_udp(ip_address=IP_ADDRESS, port=PORT)

    mock_link.assert_called_once_with(method=CONNECT, endpoint=actor[NAME].get_udp_endpoint(ip_address=IP_ADDRESS, port=PORT))


@pytest.mark.parametrize('socket_type', TO_CONNECT_SOCKET_TYPES)
def test_connect_socket_manager_via_tcp(actor, socket_type, mocker):

    actor.create_socket_manager(name=NAME, socket_type=socket_type)

    mock_link = mocker.patch.object(actor[NAME], '_link')

    actor[NAME].connect_via_tcp(ip_address=IP_ADDRESS, port=PORT)

    mock_link.assert_called_once_with(method=CONNECT, endpoint=actor[NAME].get_tcp_endpoint(ip_address=IP_ADDRESS, port=PORT))


@pytest.mark.parametrize('socket_type', TO_CONNECT_SOCKET_TYPES)
def test_connect_socket_manager_via_pgm(actor, socket_type, mocker):

    actor.create_socket_manager(name=NAME, socket_type=socket_type)

    mock_link = mocker.patch.object(actor[NAME], '_link')

    actor[NAME].connect_via_pgm(ip_address=IP_ADDRESS, port=PORT)

    mock_link.assert_called_once_with(method=CONNECT, endpoint=actor[NAME].get_pgm_endpoint(ip_address=IP_ADDRESS, port=PORT))


@pytest.mark.parametrize('socket_type', TO_CONNECT_SOCKET_TYPES)
def test_connect_socket_manager_via_epgm(actor, socket_type, mocker):

    actor.create_socket_manager(name=NAME, socket_type=socket_type)

    mock_link = mocker.patch.object(actor[NAME], '_link')

    actor[NAME].connect_via_epgm(ip_address=IP_ADDRESS, port=PORT)

    mock_link.assert_called_once_with(method=CONNECT, endpoint=actor[NAME].get_epgm_endpoint(ip_address=IP_ADDRESS, port=PORT))


@pytest.mark.parametrize('socket_type', TO_CONNECT_SOCKET_TYPES)
def test_unbind_socket_manager(actor, socket_type, mocker):

    actor.create_socket_manager(name=NAME, socket_type=socket_type)

    mock_bind = mocker.patch.object(actor[NAME], '_link')
    mock_unbind = mocker.patch.object(actor[NAME], '_unlink')

    endpoint = actor[NAME].get_inproc_endpoint(reference=REFERENCE)

    actor[NAME].bind_via_inproc(reference=REFERENCE)
    actor[NAME].unbind(endpoint=endpoint)

    mock_bind.assert_called_once_with(method=BIND, endpoint=endpoint)
    mock_unbind.assert_called_once_with(method=UNBIND, endpoint=endpoint)

    assert endpoint not in actor[NAME].endpoints[BIND]


@pytest.mark.parametrize('socket_type', TO_CONNECT_SOCKET_TYPES)
def test_disconnect_socket_manager(actor, socket_type, mocker):

    actor.create_socket_manager(name=NAME, socket_type=socket_type)

    mock_connect = mocker.patch.object(actor[NAME], '_link')
    mock_disconnect = mocker.patch.object(actor[NAME], '_unlink')

    endpoint = actor[NAME].get_inproc_endpoint(reference=REFERENCE)

    actor[NAME].connect_via_inproc(reference=REFERENCE)
    actor[NAME].disconnect(endpoint=endpoint)

    mock_connect.assert_called_once_with(method=CONNECT, endpoint=endpoint)
    mock_disconnect.assert_called_once_with(method=DISCONNECT, endpoint=endpoint)

    assert endpoint not in actor[NAME].endpoints[DISCONNECT]


def test_subscribe_socket_manager(actor):

    actor.create_sub_socket_manager(name=NAME)

    actor[NAME].subscribe(topic=b'')

    assert b'' in actor[NAME].subscriptions


def test_unsubscribe_socket_manager(actor):

    actor.create_sub_socket_manager(name=NAME)

    actor[NAME].subscribe(topic=b'')
    actor[NAME].unsubscribe(topic=b'')

    assert b'' not in actor[NAME].subscriptions


@pytest.mark.asyncio
@pytest.mark.parametrize('socket_type', TO_BIND_SOCKET_TYPES)
async def test_emit_signals_with_serializers(actor, socket_type, mocker):

    actor.create_socket_manager(name=NAME, socket_type=socket_type)

    actor[NAME].bind_via_inproc(reference=REFERENCE)

    actor.boot_socket_managers()

    assert actor[NAME].is_emitting()

    mock = mocker.patch.object(actor, '_emit')

    topic, signal = b'', {}

    await actor.emit_json(name=NAME, topic=topic, message=signal)
    await actor.emit_msgpack(name=NAME, topic=topic, message=signal)
    await actor.emit_pickle(name=NAME, topic=topic, message=signal)

    await actor.terminate()

    assert mock.call_count == 3


@pytest.mark.asyncio
async def test_recv_signals_with_serializers(actor, mocker):

    mocker.patch.object(actor, '_recv', return_value={'key': 'value'})

    result_json = await actor.recv_json(name=NAME)
    result_msgpack = await actor.recv_msgpack(name=NAME)
    result_pickle = await actor.recv_pickle(name=NAME)

    assert result_json == {'key': 'value'}
    assert result_msgpack == {'key': 'value'}
    assert result_pickle == {'key': 'value'}


@pytest.mark.asyncio
async def test_boot_socket_managers(actor):

    actor.create_socket_manager(name=NAME, socket_type=PAIR)

    actor[NAME].bind_via_inproc(reference=REFERENCE)

    actor.boot_socket_managers()

    assert actor[NAME].is_emitting()

    await actor.terminate_socket_managers()


@pytest.mark.asyncio
async def test_stop_socket_managers(actor):

    actor.create_socket_manager(name=NAME, socket_type=PAIR)

    actor[NAME].bind_via_inproc(reference=REFERENCE)

    actor.boot_socket_managers()

    assert actor[NAME].is_emitting()

    await actor.stop_socket_managers()

    assert not actor[NAME].is_emitting()


@pytest.mark.asyncio
async def test_actor_terminate(actor):

    actor.create_socket_manager(name=NAME, socket_type=PAIR)

    actor[NAME].bind_via_inproc(reference=REFERENCE)

    actor.boot_socket_managers()

    assert actor[NAME].is_emitting()

    await actor.terminate()

    assert actor.socket_managers == {}
