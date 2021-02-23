
import os, sys, re, io
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from tqdm.auto import tqdm
import numba

from datetime import datetime

from time import sleep
from tqdm.auto import tqdm

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox, ActionChains

import matplotlib.pyplot as plt
import matplotlib.patches as patches

@numba.jit
def iou_xywh(box_a, box_b):

    """
        Compute Intersection over Union (IoU)
        a box should be a tuple (x, y, width, height)

        Example:
        >>>  assert round( iou_xywh((10, 20, 30, 50), (30, 50, 50, 40)), 6) == 0.060606, f"Expected: 0.060606, but {iou_xywh((10, 20, 30, 50), (30, 50, 50, 40))} was returned"
    """
    
    x1, y1, w1, h1 = box_a
    x2, y2, w2, h2 = box_b
    
    if x1+w1 <= x2:
        return 0.0
    if x2+w2 <= x1:
        return 0.0
    if y1+h1 <= y2:
        return 0.0
    if y2+h2 <= y1:
        return 0.0
    
    if (w1<=0.0) or (w2<=0.0) or (h1<=0.0) or (h2<=0.0):
        return None
    
    s1 = w1*h1
    s2 = w2*h2
    
    si = (min(x1+w1,x2+w2)- max(x1,x2)) * (min(y1+h1,y2+h2)- max(y1,y2))
    
    return si/(s1+s2-si)



def draw_boxes(box_a, box_b):
    """
        box: tuple(x, y, width, height)
    """
    plt.figure(figsize=(4,4))
    plt.xlim(0,100)
    plt.ylim(0,100)
    axes = plt.gca() #plt.gca()
    patch_a = Rectangle((box_a[0], box_a[1]), box_a[2], box_a[3], color='red', alpha=.5)
    axes.add_patch(patch_a)
    patch_b = Rectangle((box_b[0], box_b[1]), box_b[2], box_b[3], color='blue', alpha=.5)
    axes.add_patch(patch_b)
    plt.show()


# Maximize window
def maximize_window(driver=None):
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X )
    driver.set_window_size(S('Width'), S('Height'))
    driver.find_element_by_tag_name('body')
    print('Window maximized')



def screenshot(driver=None, save_to_file:str=None, display:bool = False):
    """
        take a screenshot, returns numpy array
        and optionaly shows the screenshot 
    """

    os.makedirs('tmp', exist_ok=True)
    
    if save_to_file is None:
        fn = 'tmp/'+str(datetime.now())+".png"
        fn = fn.replace(':','_').replace(' ',"T")
    else:
        fn = re.sub('\.png$', '', save_to_file) + '.png'
    
    if not driver.save_screenshot(fn):
        print('cannot save screenshot')
    
    img = plt.imread(fn)
    if display:
        plt.imshow(img)
        
    return img


def get_pict(web_element):
    """
	    returns web elements png as a nympy.ndarray 
    """
    if web_element.is_displayed():
        print('displayed')
    else:
        print('hidden element')
        return None
        
    try:
        png = web_element.screenshot_as_png
    except:
        print('No png for element:', web_element)
        return None

    if png is None:
        return  None

    with io.BytesIO(png) as f:
        img = plt.imread(f)

    return img



MAX_PICT_SIZE_TRESHOLD = 228

def is_hover(e, driver, wait_time=.1):

    """
        Checks the element changes when mouse is hover
        returns tuple (bool, before, after):
                - bool: if it changes, 
                and if element's size less then (MAX_PICT_SIZE_TRESHOLD x MAX_PICT_SIZE_TRESHOLD) then
                - base64 png image before hover
                - base64 png image after        
    """

    if not e.is_displayed():
        return (False, None, None)

    if (e.rect['x'] < 0) or (e.rect['y'] < 0) or (e.rect['width'] <= 0) or (e.rect['height'] <=0 ):
        return (False, None, None)
    
    return_picts = True
    
    if max(e.size['width'], e.size['height']) > MAX_PICT_SIZE_TRESHOLD:
        return_picts = False
    
    try:
        ActionChains(driver)\
            .move_to_element(driver.find_element_by_xpath('//html'))\
            .perform()
    except Exception as ex:
        print('Warning:', ex, 'element:', e.tag_name, e)
    
    sleep(wait_time)
    
    try:
    
        _before = e.screenshot_as_base64

        # print(_before)
        try:
            ActionChains(driver).move_to_element(e).perform()
        except:
            driver.executeScript("arguments[0].scrollIntoView(true);", e)
            ActionChains(driver).move_to_element(e).perform()

        sleep(wait_time)
        _after = e.screenshot_as_base64
        # print(_after)
        _hover = _after!=_before
        
        if return_picts == False: # Drop big picts
            _before = None
            _after = None

        return (_hover, _before, _after)        
    
    except:
        
        return (False, None, None)



def get_all_elements(driver=None):

    """
        get all web elemets for a current page
        returns pandas dataframe
    """
    
    elements_all = driver.find_elements_by_xpath('//*')
    print(f'Number of discovered elements: {len(elements_all)}')
    # maximize_window(driver=driver)
    
    columns = [
        'parent_id',
        'element_id',
        'tag_name',
        'x',
        'y',
        'height',
        'width',
        'displayed',
        'enabled',
        'selected',
        'text',
        'is_hover',
        'base64png_before_hover',
        'base64png_after_hover',
        'attr_class',
        'attr_onclick',
        'attr_type',
        'attr_role',
        'attr_id'
    ]

    elements_a = []

    for e in tqdm(elements_all):
        
        txt = e.get_attribute('text')
        tag_class = e.get_attribute("class")
        tag_onclick = e.get_attribute("onclick")
        tag_type = e.get_attribute("type")
        tag_role = e.get_attribute("role")
        tag_id = e.get_attribute("id")
        hover, hover_before, hover_after = is_hover(e=e, driver=driver)
        
        try:
            parents = e.find_elements_by_xpath('./..')
            if len(parents) > 1:
                raise('More then one parent for element:', e)
            parent_id = parents[0].id
        except:
            parent_id = None
        
        elements_a.append([
            parent_id,
            e.id,
            e.tag_name,
            e.location['x'],
            e.location['y'],
            e.size['height'],
            e.size['width'],
            e.is_displayed(),
            e.is_enabled(),
            e.is_selected(),
            txt,
            hover,
            hover_before,
            hover_after,
            tag_class,
            tag_onclick,
            tag_type,
            tag_role,
            tag_id
        ])

    e_df = pd.DataFrame(elements_a)
    e_df.columns = columns
    return e_df


def setup_web_driver():

    SITE_ROOT = 'https://jdi-testing.github.io/jdi-light/'
    LOGIN = 'Roman'
    PASSWORD = 'Jdi1234'
    WAIT_TIME_SECONDS = 7
    HEADLESS = True #False

    options = Options()
    if HEADLESS:
        options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    CHROME_DRIVER_PATH = os.path.join(os.getcwd(), 'chromedriver.exe')
    if os.path.exists(CHROME_DRIVER_PATH):
        driver = selenium.webdriver.Chrome(executable_path=CHROME_DRIVER_PATH, options=options)
        driver.get(SITE_ROOT)
    
    driver.find_element_by_id("user-icon").click()
    driver.find_element_by_id("name").send_keys(LOGIN)
    driver.find_element_by_id("password").send_keys(PASSWORD)
    driver.find_element_by_id("login-button").click()
    sleep(WAIT_TIME_SECONDS)
        
    return driver


if __name__ == "__main__":

    with setup_web_driver() as driver:
              
        driver.find_element_by_link_text("Elements packs").click()
        driver.find_element_by_link_text("Angular").click()
        maximize_window(driver=driver)
        sleep(3.0)
        
        plt.imshow(screenshot(driver, save_to_file='dataset/images/angular.png'))
        elements_df = get_all_elements(driver=driver)
        elements_df.to_parquet('dataset/df/angular.parquet')

