from utils.api_utils import (
    convert_task_id_if_in_revoked,
    get_element_id_from_xpath,
    get_xpath_from_id,
    revoked_tasks_ids_set,
)


def test_get_xpath_from_id():
    assert get_xpath_from_id("any_string") == "//*[@jdn-hash='any_string']"


def test_get_element_id_from_xpath():
    assert get_element_id_from_xpath("//*[@jdn-hash='any_string']") == "any_string"


def test_convert_task_id_in_revoked():
    revoked_tasks_ids_set.add("123")
    assert convert_task_id_if_in_revoked("123") == "_123"


def test_do_not_convert_task_id_not_in_revoked():
    revoked_tasks_ids_set.clear()
    assert convert_task_id_if_in_revoked("12345") == "12345"
