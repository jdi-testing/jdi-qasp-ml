from fastapi.testclient import TestClient

from app.main import api


def test_websocket_invalid_message():

    client = TestClient(api)
    with client.websocket_connect("/ws") as websocket:
        websocket.send_json({"msg": "Hello"})
        data = websocket.receive_json()
        assert data == {"error": "Invalid message format."}


def test_ping():

    client = TestClient(api)
    with client.websocket_connect("/ws") as websocket:
        ping_message1 = {
            "action": "ping",
            "payload": {},
        }
        websocket.send_json(ping_message1)
        data = websocket.receive_json()
        assert data == {"pong": {}}

        ping_message2 = {
            "action": "ping",
            "payload": {"mock_data": "mock_data"},
        }
        websocket.send_json(ping_message2)
        data = websocket.receive_json()
        assert data == {"pong": {"mock_data": "mock_data"}}
