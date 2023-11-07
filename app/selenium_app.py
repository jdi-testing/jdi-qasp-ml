import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.logger import logger


def get_element_id_to_is_displayed_mapping(page_content_str):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")

    capabilities = {
        "browserName": "chrome",
        "browserVersion": "118.0",
        "selenoid:options": {
            "enableVideo": False
        }
    }

    driver = webdriver.Remote(
        command_executor="http://jdi-qasp-ml-selenoid-1:4444/wd/hub",
        desired_capabilities=capabilities, options=chrome_options)

    driver.execute_script("document.write(arguments[0]);", page_content_str)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    all_elements = driver.find_elements(by=By.XPATH, value="//*")

    result = {}

    for element in all_elements:
        element_id = element.get_attribute("jdn-hash")  # got this format \"0000000000000000000000000000\"
        element_id = str(element_id).replace('\\"', '')  # need to remove \"
        is_shown = element.is_displayed()
        result[element_id] = is_shown
        print(f"{element}: {is_shown} {element.get_attribute('name')}")

    # for element in all_elements:
    #     element_id = element.get_attribute("jdn-hash")  # got this format \"0000000000000000000000000000\"
    #     element_id = str(element_id).replace('\\"', '')  # need to remove \"
    #     is_shown = element.is_displayed()
    #     result[element_id] = is_shown
    #     logger.info(f"Element with jdn-hash {element_id} {'Visible' if is_shown else 'Invisible'}")

    driver.quit()
    return result
