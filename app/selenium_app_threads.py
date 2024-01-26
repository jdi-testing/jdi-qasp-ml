import functools
from typing import Optional, Iterable, Dict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import concurrent.futures
import threading
import cProfile
from pstats import SortKey, Stats

from app.logger import logger

JDNHash = Optional[str]
import random


def profiled(func):
    @functools.wraps(func)
    def _profiled(*args, **kwargs):
        profile = cProfile.Profile()
        profile.enable()

        result = func(*args, **kwargs)

        profile.disable()
        with open(f"{func.__name__}_profiled_{random.randint(1, 1000)}.txt", "w") as stats_file:
            Stats(profile, stream=stats_file).sort_stats(SortKey.CUMULATIVE).print_stats()

        return result

    return _profiled


@profiled
def get_elements_visibility(elements_hashes: Iterable[JDNHash], chrome_options, capabilities, dom) -> Dict[JDNHash, bool]:
    result = {}

    driver = getattr(threadLocal, 'driver', None)
    if driver is None:
        driver = webdriver.Remote(
            command_executor="http://selenoid:4444/wd/hub",
            desired_capabilities=capabilities, options=chrome_options)
        setattr(threadLocal, 'driver', driver)

    driver.execute_script("document.body.insertAdjacentHTML('beforeend', arguments[0]);", dom)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    all_elements = driver.find_elements(by=By.XPATH, value="//*")

    for element in all_elements:
        element_id = element.get_attribute("jdn-hash")
        if element_id in elements_hashes:
            is_shown = element.is_displayed()
            result[element_id] = is_shown
            # logger.info(f"Element with jdn-hash {element_id} {'Visible' if is_shown else 'Invisible'}")

    return result


def split_into_chunks(data, desired_chunks_amount):
    data_size = len(data)
    chunk_size = data_size // desired_chunks_amount

    for i in range(desired_chunks_amount):
        if i == (desired_chunks_amount - 1):
            yield data[i * chunk_size:]
        else:
            yield data[i * chunk_size:(i + 1) * chunk_size]


def get_chunks_boundaries(data, desired_chunks_amount):
    data_size = len(data)
    chunk_size = data_size // desired_chunks_amount

    for i in range(desired_chunks_amount):
        if i == (desired_chunks_amount - 1):
            yield i * chunk_size, data_size
        else:
            yield i * chunk_size, (i + 1) * chunk_size


threadLocal = threading.local()


def t_get_element_id_to_is_displayed_mapping(page_content_str):
    import gc
    gc.collect()
    dom = str(page_content_str).encode('utf-8').decode('unicode_escape')

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
        command_executor="http://selenoid:4444/wd/hub",
        desired_capabilities=capabilities, options=chrome_options)

    driver.execute_script("document.body.insertAdjacentHTML('beforeend', arguments[0]);", dom)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    all_elements = driver.find_elements(by=By.XPATH, value="//*")

    jdn_hashes = [e.get_attribute("jdn-hash") for e in all_elements]
    max_threads = 4
    split_jdn_hashes = split_into_chunks(jdn_hashes, max_threads * 2)

    result = {}

    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Start the load operations and mark each future with its URL
        future_to_visibility_map = {
            executor.submit(get_elements_visibility, jdn_hashes_chunk, chrome_options, capabilities, dom):
                " ".join(str(jdn_hashes_chunk))
            for jdn_hashes_chunk in split_jdn_hashes
        }
        for future in concurrent.futures.as_completed(future_to_visibility_map):
            hashes_calculated = future_to_visibility_map[future]
            try:
                result.update(future.result())
            except Exception as exc:
                print('%r generated an exception: %s' % (hashes_calculated, exc))

    driver.quit()
    return result
