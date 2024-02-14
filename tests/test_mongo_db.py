from app.mongodb import client, get_session_id


def test_mongodb_connected():
    assert client.jdn.name


def test_get_session_id():
    result1 = get_session_id()
    result2 = get_session_id()
    result3 = get_session_id()
    assert result2 - result1 == 1
    assert result3 - result2 == 1
