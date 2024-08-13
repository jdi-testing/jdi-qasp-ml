import logging
from typing import List, Dict

from app.celery_app import celery_app
from app.selenium_app import get_webdriver
from app.redis_app import redis_app


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
        elements_ids = kwargs["elements_ids"]
        redis_keys = [f"css-selector-{e}" for e in elements_ids]
        cached_selectors = redis_app.mget(redis_keys)

        result = []
        not_cached_elements_ids = []

        for element_id, selector in zip(elements_ids, cached_selectors):
            if selector is None:
                not_cached_elements_ids.append(element_id)
            else:
                logger.info(f"Using cached selector for element {element_id}")
                result.append({"id": element_id, "result": selector.decode("utf-8")})

        if not_cached_elements_ids:
            new_kwargs = kwargs.copy()
            new_kwargs["elements_ids"] = not_cached_elements_ids

            new_results = func(*args, **new_kwargs)

            result.extend(new_results)

            for new_result in new_results:
                redis_app.set(f"css-selector-{new_result['id']}", new_result["result"], ex=60*60*24)
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
    driver = get_webdriver()
    # Closing the browser, attaching to the shared Selenium session
    driver.quit()
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
