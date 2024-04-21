import logging
from pathlib import Path
from typing import List, Dict

from app.celery_app import celery_app
from app.selenium_app import get_webdriver


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


@celery_app.task(bind=True)
@_replace_error_messages("Error generating CSS locator")
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
