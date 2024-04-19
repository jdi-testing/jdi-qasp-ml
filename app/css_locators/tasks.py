from pathlib import Path

from selenium.common.exceptions import WebDriverException

from app.celery_app import celery_app
from app.selenium_app import get_webdriver


@celery_app.task(bind=True)
def task_schedule_css_locator_generation(self, element_id: int, document_path: str) -> str:
    driver = get_webdriver()

    driver.get(f"file:///html/{Path(document_path).name}")
    result = None

    try:
        result = driver.execute_script(
            f"""
            el = document.querySelector('[jdn-hash="{element_id}"]');
            return generateSelectorByElement(el);
            """
        )
    except WebDriverException:
        pass
    finally:
        return result
