import logging
from typing import List, Dict

from app.celery_app import celery_app
from app.redis_app import redis_app

from .utils import ExistingRemoteSession


logger = logging.getLogger(__name__)


CSS_SELECTOR_GEN_TASK_PREFIX = "css-selectors-gen-"


def _replace_error_messages(new_message: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                raise RuntimeError(new_message) from exc
        return wrapper
    return decorator


def _cache_calculations_results(func):
    def wrapper(*args, **kwargs):
        element_id = kwargs["element_id"]
        redis_key = f"css-selector-{element_id}"
        cached_selector = redis_app.get(redis_key)

        if cached_selector:
            logger.info(f"Using cached selector for element {element_id}")
            result = [{"id": element_id, "result": cached_selector.decode("utf-8")}]
        else:
            result = func(*args, **kwargs)
            redis_app.set(redis_key, result[0]["result"], ex=60*60*24)
        return result

    return wrapper


@celery_app.task(bind=True)
@_replace_error_messages("Error generating CSS selectors")
@_cache_calculations_results
def task_schedule_css_selector_generation(self, session_id: str, element_id: str) -> List[Dict[str, str]]:
    """Get CSS selector for element using passed Selenium session.

    :param session_id: Selenium session id
    :param element_id: Value of jdn-hash attribute of element for which the CSS selector should be generated

    :returns: List with result dictionary. List is used just to keep compatibility with old API.
    """
    driver = ExistingRemoteSession(command_executor="http://selenoid:4444/wd/hub", desired_capabilities=None)
    driver.session_id = session_id

    return [{
        "id": element_id,
        "result": driver.execute_script(
            f"""
            el = document.querySelector('[jdn-hash="{element_id}"]');
            return generateSelectorByElement(el);
            """
        ),
    }]
