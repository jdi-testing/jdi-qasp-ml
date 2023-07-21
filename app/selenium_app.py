from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_element_id_to_is_displayed_mapping(page_content_str):

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("about:blank")

    driver.execute_script("document.write(arguments[0]);", page_content_str)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    all_elements = driver.find_elements(by=By.XPATH, value='//*')

    result = {element.get_attribute('jdn-hash'): element.is_displayed() for element in all_elements}

    # result = []
    #
    # for element in all_elements:
    #     element_info = {
    #         "element_id": element.get_attribute('jdn-hash'),
    #         "is_shown": element.is_displayed()
    #     }
    #     result.append(element_info)

    driver.quit()
    return result


