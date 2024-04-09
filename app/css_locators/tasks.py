from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from app.celery_app import celery_app
from app.selenium_app import get_webdriver


@celery_app.task(bind=True)
def task_schedule_css_locator_generation(self, element_id: int, document_uuid: str) -> str:
    driver = get_webdriver()

    driver.get(f"file:///html/{document_uuid}.html")
    WebDriverWait(driver, 10).until(
        expected_conditions.presence_of_element_located(
            (By.TAG_NAME, "body")
        )
    )

    return driver.execute_script(
        f"""
        el = document.querySelector('[jdn-hash="{element_id}"]');
        return generateSelectorByElement(el);
        """
    )
