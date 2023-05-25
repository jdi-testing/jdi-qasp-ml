import time

from fastapi.testclient import TestClient

from app.celery_app import celery_app
from app.main import api

client = TestClient(api)


def test_websocket_invalid_message():

    with client.websocket_connect("/ws") as websocket:
        websocket.send_json({"msg": "Hello"})
        data = websocket.receive_json()
        assert data == {"error": "Invalid message format."}


def test_ping():
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


def test_schedule_multiple_xpath_generations(mock_simple_page):
    with client.websocket_connect("/ws") as websocket:
        mock_message = {
            "action": "schedule_multiple_xpath_generations",
            "payload": {
                "document": mock_simple_page,
                "id": ["3454558281842394677212548221"],
                "config": {
                    "maximum_generation_time": 1,
                    "allow_indexes_at_the_beginning": False,
                    "allow_indexes_in_the_middle": False,
                    "allow_indexes_at_the_end": False,
                },
            },
            "logging_info": {
                "session_id": 332,
                "page_object_creation": "AVerySimpleWebpage",
                "element_library": "HTML5",
                "website_url": "https://web.ics.purdue.edu/~gchopra/class/public/pages/webdesign/05_simple.html",
            },
        }
        websocket.send_json(mock_message)
        data3 = websocket.receive_json()
        assert data3["action"] == "result_ready"
        assert data3["payload"]["result"]


def test_revoke_tasks(mock_simple_page):
    with client.websocket_connect("/ws") as websocket:
        mock_message = {
            "action": "schedule_multiple_xpath_generations",
            "payload": {
                "document": mock_simple_page,
                "id": [
                    "6491321822842394671263543627",
                    "9772922236842394671549553513",
                    "5806303415842394670029439121",
                    "9693930545842394683885892445",
                    "4193993466842394678988767466",
                ],
                "config": {
                    "maximum_generation_time": 1,
                    "allow_indexes_at_the_beginning": False,
                    "allow_indexes_in_the_middle": False,
                    "allow_indexes_at_the_end": False,
                },
            },
            "logging_info": {
                "session_id": 333,
                "page_object_creation": "AVerySimpleWebpage1",
                "element_library": "HTML5",
                "website_url": "https://web.ics.purdue.edu/~gchopra/class/public/pages/webdesign/05_simple_1.html",
            },
        }
        websocket.send_json(mock_message)
        websocket.send_json(
            {
                "action": "revoke_tasks",
                "payload": {"id": ["4193993466842394678988767466"]},
            }
        )

        data = websocket.receive_json()
        assert data["action"] == "tasks_revoked"


def test_revoke_task_and_rerun(mock_simple_page):
    with client.websocket_connect("/ws") as websocket:

        # Run tasks:
        mock_message = {
            "action": "schedule_multiple_xpath_generations",
            "payload": {
                "document": mock_simple_page,
                "id": [
                    "5610175704842394682912827557",
                    "9552011587842394678546958439",
                    "6509829360842394679374579325",
                    "6141640202842394676845507677",
                    "6034232264842394689263545313",
                    "5721291098842394672262179535",
                    "2062873048842394684036507809",
                    "5572629157842394676934206880",
                    "4056348058842394686575005676",
                    "3363615764842394670921018049",
                    "2124540623842394679666778990",
                    "7583721053842394674210958853",
                    "0103848358842394684976681594",
                ],
                "config": {
                    "maximum_generation_time": 1,
                    "allow_indexes_at_the_beginning": False,
                    "allow_indexes_in_the_middle": False,
                    "allow_indexes_at_the_end": False,
                },
            },
            "logging_info": {
                "session_id": 334,
                "page_object_creation": "AVerySimpleWebpage1",
                "element_library": "HTML5",
                "website_url": "https://web.ics.purdue.edu/~gchopra/class/public/pages/webdesign/05_simple_1.html",
            },
        }
        websocket.send_json(mock_message)

        # Revoke specific task:
        websocket.send_json(
            {
                "action": "revoke_tasks",
                "payload": {"id": ["0103848358842394684976681594"]},
            }
        )

        data = websocket.receive_json()
        assert data["action"] == "tasks_revoked"
        time.sleep(7)
        task_instance = celery_app.AsyncResult("0103848358842394684976681594")
        task_status = task_instance.status
        assert task_status == "REVOKED"

        # Rerun specific task
        new_message = {
            "action": "schedule_multiple_xpath_generations",
            "payload": {
                "document": mock_simple_page,
                "id": ["0103848358842394684976681594"],
                "config": {
                    "maximum_generation_time": 1,
                    "allow_indexes_at_the_beginning": False,
                    "allow_indexes_in_the_middle": False,
                    "allow_indexes_at_the_end": False,
                },
            },
            "logging_info": {
                "session_id": 334,
                "page_object_creation": "AVerySimpleWebpage1",
                "element_library": "HTML5",
                "website_url": "https://web.ics.purdue.edu/~gchopra/class/public/pages/webdesign/05_simple_1.html",
            },
        }
        websocket.send_json(new_message)

        time.sleep(2)
        task_instance1 = celery_app.AsyncResult(
            "_0103848358842394684976681594"
        )
        task_status = task_instance1.status
        assert task_status == "SUCCESS"


def test_deep_calculation(mock_simple_page):
    with client.websocket_connect("/ws") as websocket:
        # Run task as usual
        mock_message = {
            "action": "schedule_multiple_xpath_generations",
            "payload": {
                "document": mock_simple_page,
                "id": [
                    "3027183088842394682894924777",
                ],
                "config": {
                    "maximum_generation_time": 1,
                    "allow_indexes_at_the_beginning": False,
                    "allow_indexes_in_the_middle": False,
                    "allow_indexes_at_the_end": False,
                },
            },
            "logging_info": {
                "session_id": 335,
                "page_object_creation": "AVerySimpleWebpage2",
                "element_library": "HTML5",
                "website_url": "https://web.ics.purdue.edu/~gchopra/class/public/pages/webdesign/05_simple_2.html",
            },
        }
        websocket.send_json(mock_message)

        time.sleep(5)
        task_instance = celery_app.AsyncResult("3027183088842394682894924777")
        assert task_instance.status == "SUCCESS"

        # Rerun task with higher maximum_generation_time
        new_message = {
            "action": "schedule_multiple_xpath_generations",
            "payload": {
                "document": mock_simple_page,
                "id": [
                    "3027183088842394682894924777",
                ],
                "config": {
                    "maximum_generation_time": 10,
                    "allow_indexes_at_the_beginning": False,
                    "allow_indexes_in_the_middle": False,
                    "allow_indexes_at_the_end": False,
                    "advanced_calculation": True,
                },
            },
            "logging_info": {
                "session_id": 335,
                "page_object_creation": "AVerySimpleWebpage2",
                "element_library": "HTML5",
                "website_url": "https://web.ics.purdue.edu/~gchopra/class/public/pages/webdesign/05_simple_2.html",
            },
        }
        websocket.send_json(new_message)
        time.sleep(20)

        task_instance = celery_app.AsyncResult("_3027183088842394682894924777")
        assert task_instance.status == "SUCCESS"
