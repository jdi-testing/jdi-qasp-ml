from utils.api_utils import (
    get_element_id_from_xpath,
    get_xpath_from_id,
)


def test_get_xpath_from_id():
    assert get_xpath_from_id("any_string") == "//*[@jdn-hash='any_string']"


def test_get_element_id_from_xpath():
    assert get_element_id_from_xpath("//*[@jdn-hash='any_string']") == "any_string"
