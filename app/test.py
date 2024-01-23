import random
from typing import Optional
import time

import uvicorn
from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import concurrent.futures
from app.selenium_app_threads import split_into_chunks, profiled
import logging

app = FastAPI()

_log_format = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
_datefmt = "%d-%b-%y %H:%M:%S"

logging.basicConfig(level=logging.INFO, format=_log_format, datefmt=_datefmt)


def get_html_page(url: str) -> Optional[str]:
    try:
        with open(f"app/test_doms/{url}.html") as f:
            html = f.read()
    except FileNotFoundError:
        return None

    return html


# threadLocal = threading.local()

def get_webdriver():
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

    return webdriver.Remote(
        command_executor="http://jdi-qasp-ml-selenoid:4444/wd/hub",
        desired_capabilities=capabilities,
        options=chrome_options,
    )


def get_page_elements(driver, dom):
    driver.execute_script("document.body.insertAdjacentHTML('beforeend', arguments[0]);", dom)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    return driver.find_elements(by=By.XPATH, value="//*")


@profiled
def get_element_id_to_is_displayed_mapping(dom, elements_hashes):
    logger = logging.getLogger(f"{random.randint(100000, 999999)}")
    # driver_ = getattr(threadLocal, 'driver_', None)
    # if driver_ is None:
    driver = get_webdriver()
    # setattr(threadLocal, 'driver_', driver_)

    all_elements = get_page_elements(driver, dom)

    result = {}

    for element in all_elements:
        element_id = element.get_attribute("jdn-hash")
        if element_id in elements_hashes:
            is_shown = element.is_displayed()
            result[element_id] = is_shown
            logger.info(f"Element {element_id} visibility: {is_shown}")

    driver.quit()
    return result


@app.get("/visibility/{url}")
def calculate_visibility(url: str):
    print(f"Processing request for url {url}")
    dom = get_html_page(url)

    if dom is None:
        raise HTTPException(status_code=404, detail="Page not found")

    result = {}

    t1 = time.perf_counter(), time.process_time()

    driver = get_webdriver()
    all_elements = get_page_elements(driver, dom)

    for element in all_elements:
        element_id = element.get_attribute("jdn-hash")
        is_shown = element.is_displayed()
        result[element_id] = is_shown

    driver.quit()

    t2 = time.perf_counter(), time.process_time()

    return {
        "time": {
            "seconds_real": f"{t2[0] - t1[0]:.2f}",
            "seconds_cpu": f"{t2[1] - t1[1]:.2f}",
        },
        "result": result,
    }


@app.get("/visibility-mt/{url}")
def calculate_visibility_mt(url: str, threads: int = 4, chunks: int = 8, use_processes: bool = False):
    print(f"Processing multi threaded request for url {url}")
    dom = get_html_page(url)

    if dom is None:
        raise HTTPException(status_code=404, detail="Page not found")

    result = {}

    t1 = time.perf_counter(), time.process_time()

    driver = get_webdriver()
    all_elements = get_page_elements(driver, dom)
    jdn_hashes = [e.get_attribute("jdn-hash") for e in all_elements]
    driver.quit()

    jobs_chunks = split_into_chunks(jdn_hashes, chunks)

    if not use_processes:
        executor_ = concurrent.futures.ThreadPoolExecutor
    else:
        executor_ = concurrent.futures.ProcessPoolExecutor

    with executor_(max_workers=threads) as executor:
        futures = [
            executor.submit(get_element_id_to_is_displayed_mapping, dom, jdn_hashes_chunk)
            for jdn_hashes_chunk in jobs_chunks
        ]
        for future in concurrent.futures.as_completed(futures):
            result.update(future.result())
            pass

    t2 = time.perf_counter(), time.process_time()

    return {
        "time": {
            "seconds_real": f"{t2[0] - t1[0]:.2f}",
            "seconds_cpu": f"{t2[1] - t1[1]:.2f}",
        },
        "result": result,
    }


if __name__ == '__main__':
    uvicorn.run("app.test:api", host="0.0.0.0", port=8000, log_level="info", reload=True)
