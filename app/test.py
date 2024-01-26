import random
import threading
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
from app.selenium_app_threads import split_into_chunks, profiled, get_chunks_boundaries
import logging
import re

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


# leftover_ids = []
# leftover_ids_lock = threading.Lock()


def get_element_id_to_is_displayed_mapping(dom, starting_idx, ending_idx):
    logger = logging.getLogger(f"{random.randint(100000, 999999)}")
    driver = get_webdriver()

    logger.info(f"Getting {starting_idx} to {ending_idx}")

    all_elements = get_page_elements(driver, dom)

    result = {}

    for element in all_elements[starting_idx:ending_idx]:
        element_jdn_hash = element.get_attribute("jdn-hash")
        is_shown = element.is_displayed()
        result[element_jdn_hash] = is_shown

    # with leftover_ids_lock:
    #     global leftover_ids
    #     leftover_ids += ids
    #     logger.info(leftover_ids)
    #
    # leftovers_barrier.wait()
    #
    # logger.info(leftover_ids)

    # with leftover_ids_lock:
    #     for element_id in leftover_ids.copy():
    #         element = id_to_element_map.get(element_id)
    #
    #         if element is None:
    #             continue
    #
    #         leftover_ids.pop(leftover_ids.index(element_id))
    #         element_jdn_hash = element.get_attribute("jdn-hash")
    #         if element_jdn_hash in result:
    #             logger.info(f'Element {element_id} is already in the result')
    #             continue
    #         is_shown = element.is_displayed()
    #         result[element_jdn_hash] = is_shown
    #         logger.info(f"{element_id}, {element_jdn_hash}: {is_shown}")
    #
    # logger.info(leftover_ids)

    driver.quit()

    logger.info(f"Thread returns {len(result)} elements")

    return result


# @profiled
def single_thread_visibility(dom):
    logger = logging.getLogger(f"{random.randint(100000, 999999)}")
    result = {}
    driver = get_webdriver()
    all_elements = get_page_elements(driver, dom)

    for element in all_elements:
        element_id = element.get_attribute("jdn-hash")
        is_shown = element.is_displayed()
        result[element_id] = is_shown
        logger.info(f"Element {element_id} visibility: {is_shown}")

    driver.quit()

    return result


@app.get("/visibility/{url}")
def calculate_visibility(url: str):
    logger = logging.getLogger(f"single-thread")
    logger.info(f"Processing request for url {url}")
    dom = get_html_page(url)

    if dom is None:
        raise HTTPException(status_code=404, detail="Page not found")

    t1 = time.perf_counter(), time.process_time()

    result = single_thread_visibility(dom)

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
    logger = logging.getLogger(f"multi-thread")
    logger.info(f"Processing multi threaded request for url {url}")
    dom = get_html_page(url)

    if dom is None:
        raise HTTPException(status_code=404, detail="Page not found")

    result = {}

    t1 = time.perf_counter(), time.process_time()

    driver = get_webdriver()
    all_elements = get_page_elements(driver, dom)
    driver.quit()

    jobs_chunks = get_chunks_boundaries(all_elements, chunks)

    if not use_processes:
        executor_ = concurrent.futures.ThreadPoolExecutor
    else:
        executor_ = concurrent.futures.ProcessPoolExecutor

    # leftovers_barrier = threading.Barrier(threads)

    with executor_(max_workers=threads) as executor:
        futures = [
            executor.submit(get_element_id_to_is_displayed_mapping, dom, s, e)
            for s, e in jobs_chunks
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
