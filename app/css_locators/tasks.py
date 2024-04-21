import logging
from pathlib import Path
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
@_replace_error_messages("Error generating CSS locator")
@_cache_calculations_results
def task_schedule_css_selector_generation(
        self, document_path: str, elements_ids: List[str]
) -> List[Dict[str, str]]:
    driver = get_webdriver()
    driver.get(f"file:///html/{Path(document_path).name}")

    result = []
    for element_id in elements_ids:
        result.append({
            "id": element_id,
            "result": driver.execute_script(
                f"""
                el = document.querySelector('[jdn-hash="{element_id}"]');
                return generateSelectorByElement(el);
                """
            ),
        })

    return result
