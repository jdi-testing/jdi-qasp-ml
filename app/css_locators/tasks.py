import logging
from pathlib import Path

from app.celery_app import celery_app
from app.selenium_app import get_webdriver


logger = logging.getLogger(__name__)


@celery_app.task(bind=True)
def task_schedule_css_locator_generation(self, element_id: int, document_path: str) -> str:
    driver = get_webdriver()

    driver.get(f"file:///html/{Path(document_path).name}")

    # noinspection PyBroadException
    try:
        result = driver.execute_script(
            f"""
            el = document.querySelector('[jdn-hash="{element_id}"]');
            return generateSelectorByElement(el);
            """
        )
    except Exception as exc:
        logger.exception("Error generating CSS locator")
        raise RuntimeError("Error generating CSS locator") from exc

    return result
