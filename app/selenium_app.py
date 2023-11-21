from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.logger import logger


def get_element_id_to_is_displayed_mapping(page_content_str):
    dom = str(page_content_str).encode('utf-8').decode('unicode_escape')

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(
        executable_path="/usr/local/bin/chromedriver-linux64/chromedriver", options=chrome_options)

    driver.execute_script("document.body.insertAdjacentHTML('beforeend', arguments[0]);", dom)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    all_elements = driver.find_elements(by=By.XPATH, value="//*")

    result = {}

    for element in all_elements:
        element_id = element.get_attribute("jdn-hash")
        is_shown = element.is_displayed()
        result[element_id] = is_shown
        logger.info(f"Element with jdn-hash {element_id} {'Visible' if is_shown else 'Invisible'}")

    driver.quit()
    return result
