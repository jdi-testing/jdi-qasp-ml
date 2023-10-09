import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def get_element_id_to_is_displayed_mapping(page_content_str):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")

    chrome_driver_path = os.path.join(os.getcwd(), "chromedriver")
    if os.path.exists(chrome_driver_path):
        driver = webdriver.Chrome(
            executable_path=chrome_driver_path, options=chrome_options
        )

        driver.execute_script("document.write(arguments[0]);", page_content_str)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        all_elements = driver.find_elements(by=By.XPATH, value='//*')

        result = {}

        for element in all_elements:
            element_id = element.get_attribute('jdn-hash')  # got this format \"0000000000000000000000000000\"
            element_id = str(element_id).replace('\\"', '')  # need to remove \"
            is_shown = element.is_displayed()
            result[element_id] = is_shown

        driver.quit()
        return result

    else:
        raise FileNotFoundError(f"chromedriver  {os.getcwd()}")
