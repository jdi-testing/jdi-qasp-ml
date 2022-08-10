from fastapi.testclient import TestClient

from app.main import api
from tests.additional_materials import mock_document1


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


def test_schedule_multiple_xpath_generation():

    client = TestClient(api)
    with client.websocket_connect("/ws") as websocket:
        mock_message = {
            "action": "schedule_multiple_xpath_generations",
            "payload": {
                "document": mock_document1,
                "id": ["7437302889559760668635644354"],
                "config": {
                    "maximum_generation_time": 10,
                    "allow_indexes_at_the_beginning": False,
                    "allow_indexes_in_the_middle": False,
                    "allow_indexes_at_the_end": False,
                },
            },
        }

        websocket.send_json(mock_message)
        data = websocket.receive_json()
        assert data["action"] == "result_ready"
        assert data["payload"]["result"]


def test_revoke_tasks():
    client = TestClient(api)
    with client.websocket_connect("/ws") as websocket:
        ids = [
            "7437302889559760668635644354",
            "0804855189559760662416741793",
            "5214925616559760665036205317",
            "3982843610559760669157146287",
            "9365965576559760663932210658",
            "3913738650559760668611004189",
            "9418105228559760663122499447",
            "9854853464559760668730991390",
            "6862050948559760666430680549",
            "9493188821559760669875391327",
            "7520781528559760661906321107",
            "3189676561559760661294561923",
        ]
        scheduling_message = {
            "action": "schedule_multiple_xpath_generations",
            "payload": {
                "document": mock_document1,
                "id": ids,
                "config": {
                    "maximum_generation_time": 10,
                    "allow_indexes_at_the_beginning": False,
                    "allow_indexes_in_the_middle": False,
                    "allow_indexes_at_the_end": False,
                },
            },
        }

        websocket.send_json(scheduling_message)
        revoking_message = {
            "action": "revoke_tasks",
            "payload": {"id": ["3189676561559760661294561923"]},
        }
        websocket.send_json(revoking_message)

        data1 = websocket.receive_json()
        assert data1["action"] == "tasks_revoked"
        assert data1["payload"]["id"] == ["3189676561559760661294561923"]


def test_get_task_status():
    client = TestClient(api)
    with client.websocket_connect("/ws") as websocket:
        scheduling_message = {
            "action": "schedule_multiple_xpath_generations",
            "payload": {
                "document": mock_document1,
                "id": ["0496233594559760661051207166"],
                "config": {
                    "maximum_generation_time": 10,
                    "allow_indexes_at_the_beginning": False,
                    "allow_indexes_in_the_middle": False,
                    "allow_indexes_at_the_end": False,
                },
            },
        }

        websocket.send_json(scheduling_message)

        data = websocket.receive_json()
        assert data["action"] == "result_ready"

        websocket.send_json(
            {
                "action": "get_task_status",
                "payload": {"id": "0496233594559760661051207166"},
            }
        )
        data = websocket.receive_json()
        assert data == {"id": "0496233594559760661051207166", "status": "SUCCESS"}


def test_get_task_statuses():
    client = TestClient(api)
    with client.websocket_connect("/ws") as websocket:
        el_ids = ["0112389422559760667916905668", "0486422498559760669553972716"]
        scheduling_message = {
            "action": "schedule_multiple_xpath_generations",
            "payload": {
                "document": mock_document1,
                "id": el_ids,
                "config": {
                    "maximum_generation_time": 10,
                    "allow_indexes_at_the_beginning": False,
                    "allow_indexes_in_the_middle": False,
                    "allow_indexes_at_the_end": False,
                },
            },
        }

        websocket.send_json(scheduling_message)

        for el_id in el_ids:
            websocket.receive_json()

        websocket.send_json({"action": "get_tasks_statuses", "payload": {"id": el_ids}})
        data = websocket.receive_json()
        assert data == [
            {"id": "0112389422559760667916905668", "status": "SUCCESS"},
            {"id": "0486422498559760669553972716", "status": "SUCCESS"},
        ]


def test_get_task_result():
    client = TestClient(api)
    with client.websocket_connect("/ws") as websocket:
        scheduling_message = {
            "action": "schedule_multiple_xpath_generations",
            "payload": {
                "document": mock_document1,
                "id": ["3463068754559760667310543167"],
                "config": {
                    "maximum_generation_time": 10,
                    "allow_indexes_at_the_beginning": False,
                    "allow_indexes_in_the_middle": False,
                    "allow_indexes_at_the_end": False,
                },
            },
        }

        websocket.send_json(scheduling_message)

        data = websocket.receive_json()
        assert data["action"] == "result_ready"

        websocket.send_json(
            {
                "action": "get_task_result",
                "payload": {"id": "3463068754559760667310543167"},
            }
        )
        data = websocket.receive_json()
        assert data == {
            "id": "3463068754559760667310543167",
            "result": "//*[contains(text(), 'Еще один')]",
        }


def test_get_task_results():
    client = TestClient(api)
    with client.websocket_connect("/ws") as websocket:
        el_ids = ["0112389422559760667916905668", "0486422498559760669553972716"]
        scheduling_message = {
            "action": "schedule_multiple_xpath_generations",
            "payload": {
                "document": mock_document1,
                "id": el_ids,
                "config": {
                    "maximum_generation_time": 10,
                    "allow_indexes_at_the_beginning": False,
                    "allow_indexes_in_the_middle": False,
                    "allow_indexes_at_the_end": False,
                },
            },
        }

        websocket.send_json(scheduling_message)

        for el_id in el_ids:
            websocket.receive_json()

        websocket.send_json({"action": "get_task_results", "payload": {"id": el_ids}})
        data1 = websocket.receive_json()
        assert data1 == [
            {
                "id": "0112389422559760667916905668",
                "result": "//*[contains(text(), 'Просто заголовок')]",
            },
            {
                "id": "0486422498559760669553972716",
                "result": "//*[contains(text(), 'Какой-то контент')]",
            },
        ]
