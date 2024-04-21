import logging
from pathlib import Path
from typing import List, Dict

from app.celery_app import celery_app
from app.selenium_app import get_webdriver


logger = logging.getLogger(__name__)


@celery_app.task(bind=True)
def task_schedule_css_locator_generation(
        self, document_path: str, elements_ids: List[str]
) -> List[Dict[str, str]]:
    driver = get_webdriver()

    driver.get(f"file:///html/{Path(document_path).name}")

    result = []

    # noinspection PyBroadException
    try:
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
    except Exception as exc:
        logger.exception("Error generating CSS locator")
        raise RuntimeError("Error generating CSS locator") from exc

    return result
