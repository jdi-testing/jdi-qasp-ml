from typing import Iterable, Sized, Tuple, Dict, List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import concurrent.futures

from app.logger import logger
from utils import config


def get_webdriver() -> webdriver.Remote:
    """Returns a remote Chrome webdriver instance"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")

    if config.IS_DEV_SHM_USAGE_DISABLED:
        chrome_options.add_argument("--disable-dev-shm-usage")

    capabilities = {
        "browserName": "chrome",
        "browserVersion": "118.0",
        "selenoid:options": {
            "enableVideo": False
        }
    }

    return webdriver.Remote(
        command_executor="http://selenoid:4444/wd/hub",
        desired_capabilities=capabilities,
        options=chrome_options,
    )


def inject_html(driver: webdriver.Remote, html: str) -> None:
    driver.execute_script(
        "document.write(arguments[0]);",
        html,
    )
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))


def get_page_elements(driver: webdriver.Remote, page_content: str) -> List[WebElement]:
    """Returns a list of all elements contained in page_content"""
    driver.execute_script(
        "document.body.insertAdjacentHTML('beforeend', arguments[0]);",
        page_content,
    )
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    return driver.find_elements(by=By.XPATH, value="//*")


def get_elements_visibility(page_content: str, starting_element_idx: int, ending_element_idx: int) -> Dict[str, bool]:
    """Returns a visibility of portion of elements contained in page_content

    starting_element_idx and ending_element_idx are referring to the starting
    and ending indexes for slice of page_content elements returned by
    get_page_elements() function.
    """
    driver = get_webdriver()
    all_elements = get_page_elements(driver, page_content)

    result = {}

    for element in all_elements[starting_element_idx:ending_element_idx]:
        element_jdn_hash = element.get_attribute("jdn-hash")
        is_shown = element.is_displayed()
        result[element_jdn_hash] = is_shown
        logger.info(f"Element with jdn-hash {element_jdn_hash} {'Visible' if is_shown else 'Invisible'}")

    driver.quit()

    return result


def get_chunks_boundaries(data: Sized, desired_chunks_amount: int) -> Iterable[Tuple[int, int]]:
    """Returns split indexes for a list, enabling easy partitioning into desired chunks"""
    data_size = len(data)
    chunk_size = data_size // desired_chunks_amount

    for i in range(desired_chunks_amount):
        if i < (desired_chunks_amount - 1):
            yield i * chunk_size, (i + 1) * chunk_size
        else:
            yield i * chunk_size, data_size


def get_element_id_to_is_displayed_mapping(page_content: str) -> Dict[str, bool]:
    """Returns visibility status of all elements in the page

    Returned dictionary uses elements' jdn-hash property value as keys
    """
    escaped_page_content = str(page_content).encode('utf-8').decode('unicode_escape')

    driver = get_webdriver()
    all_elements = get_page_elements(driver, escaped_page_content)
    driver.quit()

    num_of_workers = config.SELENOID_PARALLEL_SESSIONS_COUNT
    jobs_chunks = get_chunks_boundaries(all_elements, num_of_workers)
    result = {}

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_of_workers) as executor:
        futures = [
            executor.submit(get_elements_visibility, escaped_page_content, s, e)
            for s, e in jobs_chunks
        ]
        for future in concurrent.futures.as_completed(futures):
            result.update(future.result())

    return result
