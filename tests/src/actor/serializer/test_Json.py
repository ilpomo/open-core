EMPTY = {}
EMPTY_DATA = b'{}'

INTEGER = 123
INTEGER_DATA = b'123'

STRING = "123"
STRING_DATA = b'"123"'

DICT = {'key': 'value'}
DICT_DATA = b'{"key":"value"}'

LIST = [1, 2, 3]
LIST_DATA = b'[1,2,3]'


def test_encode_simple_types(serializer):
    assert INTEGER == serializer.decode(data=serializer.encode(obj=INTEGER))
    assert STRING == serializer.decode(data=serializer.encode(obj=STRING))


def test_decode_simple_types(json_serializer):
    assert json_serializer.decode(data=INTEGER_DATA) == INTEGER
    assert json_serializer.decode(data=STRING_DATA) == STRING


def test_encode_complex_types(json_serializer):
    assert json_serializer.encode(obj=DICT) == DICT_DATA
    assert json_serializer.encode(obj=LIST) == LIST_DATA


def test_decode_complex_types(json_serializer):
    assert json_serializer.decode(data=DICT_DATA) == DICT
    assert json_serializer.decode(data=LIST_DATA) == LIST


def test_decode_empty_bytes(json_serializer):
    assert json_serializer.decode(data=b'') is None


def test_encode_empty_object(json_serializer):
    assert json_serializer.encode(obj=EMPTY) == EMPTY_DATA == b'{}'


def test_encode_data_integrity(json_serializer):
    assert json_serializer.encode(obj={'key': 'value', 'list': [1, 2, 3]}) == b'{"key":"value","list":[1,2,3]}'


def test_decode_data_integrity(json_serializer):
    assert json_serializer.decode(data=b'{"key":"value","list":[1,2,3]}') == {'key': 'value', 'list': [1, 2, 3]}
