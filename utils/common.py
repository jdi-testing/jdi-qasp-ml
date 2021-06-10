
import os
import re
import io
import numpy as np
import pandas as pd
from IPython.display import HTML
from IPython.display import display as ipython_displpay

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from tqdm.auto import tqdm
import numba

from datetime import datetime

from time import sleep
import selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains

from .config import logger

TQDM_BAR_FORMAT = '{desc:25}{percentage:3.0f}%|{bar:50}{r_bar}'
MAX_PICT_SIZE_TRESHOLD = 128


@numba.jit
def iou_xywh(box_a, box_b):
    """ Compute Intersection over Union (IoU)
        a box should be a tuple (x, y, width, height)

        Example:
        >>>  assert round( \
                 iou_xywh( \
                     (10, 20, 30, 50), \
                     (30, 50, 50, 40)),6)==0.060606, \
            f"Expected: 0.060606, but {iou_xywh((10, 20, 30, 50), \
                                                (30, 50, 50, 40))} \
                                                    was returned"
    """

    x1, y1, w1, h1 = box_a
    x2, y2, w2, h2 = box_b

    if x1 + w1 <= x2:
        return 0.0
    if x2 + w2 <= x1:
        return 0.0
    if y1 + h1 <= y2:
        return 0.0
    if y2 + h2 <= y1:
        return 0.0

    if (w1 <= 0.0) or (w2 <= 0.0) or (h1 <= 0.0) or (h2 <= 0.0):
        return 0.0

    s1 = w1 * h1
    s2 = w2 * h2

    si = (min(x1 + w1, x2 + w2) - max(x1, x2)) * \
        (min(y1 + h1, y2 + h2) - max(y1, y2))

    return si / (s1 + s2 - si)


# Maximize window
def maximize_window(driver=None, extend_pix=0):
    def S(X):
        return driver.execute_script(
            'return document.body.parentNode.scroll' + X
        )
    driver.set_window_size(width=S('Width'), height=S('Height') + extend_pix)
    driver.find_element_by_tag_name('body')
    logger.info('Window maximized')


def draw_boxes(box_a, box_b):
    """
        box: tuple(x, y, width, height)
    """
    plt.figure(figsize=(4, 4))
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    axes = plt.gca()  # plt.gca()
    patch_a = Rectangle((box_a[0], box_a[1]), box_a[2],
                        box_a[3], color='red', alpha=.5)
    axes.add_patch(patch_a)
    patch_b = Rectangle((box_b[0], box_b[1]), box_b[2],
                        box_b[3], color='blue', alpha=.5)
    axes.add_patch(patch_b)
    plt.show()


def screenshot(driver=None, save_to_file: str = None, display: bool = False):
    """
        Takes a screenshot, returns numpy array
        and optionaly shows the screenshot

    """

    os.makedirs('tmp', exist_ok=True)

    if save_to_file is None:
        fn = 'tmp/' + str(datetime.now()) + ".png"
        fn = fn.replace(':', '_').replace(' ', "T")

    else:
        fn = re.sub('\\.png$', '', save_to_file) + '.png'

    if not driver.save_screenshot(fn):
        print('cannot save screenshot')

    img = plt.imread(fn)
    if display:
        plt.imshow(img)

    return img


def get_pict(web_element):
    """
        Returns web elements png as a nympy.ndarray

    """
    if web_element.is_displayed():
        print('displayed')
    else:
        print('hidden element')
        return None

    try:
        png = web_element.screenshot_as_png
    except Exception as ex:
        logger.info(f"Suppress exception: {ex}")
        logger.info('No png for element:', web_element)
        return None

    if png is None:
        return None

    with io.BytesIO(png) as f:
        img = plt.imread(f)

    return img


def get_grey_image(file_path: str) -> np.ndarray:
    img = plt.imread(file_path)
    img = (img[..., 0] + img[..., 1] + img[..., 2]) / 3.0
    return img


def load_gray_image(file_path: str) -> np.ndarray:
    img = plt.imread(file_path)
    img = (img[..., 0] + img[..., 1] + img[..., 2]) / 3.0
    return img


def grey_image(img) -> np.ndarray:
    return (img[..., 0] + img[..., 1] + img[..., 2]) / 3.0


def is_hover(e, driver, wait_time=.1):
    """
        Checks the element changes when mouse is hover
        returns tuple (bool, before, after):
                - bool: if it changes,
                and if element's size less then
                    (MAX_PICT_SIZE_TRESHOLD x MAX_PICT_SIZE_TRESHOLD) then
                - base64 png image before hover
                - base64 png image after

    """
    try:

        if not e.is_displayed():
            return (False, None, None)

        if min(e.size['width'], e.size['height']) > MAX_PICT_SIZE_TRESHOLD:
            return (False, None, None)

        if (e.rect['x'] < 1.0) or (e.rect['y'] < 1.0) or \
                (e.rect['width'] <= 1.0) or (e.rect['height'] <= 1.0):
            return (False, None, None)

        return_picts = True
        if max(e.size['width'], e.size['height']) > MAX_PICT_SIZE_TRESHOLD:
            return_picts = False

        try:
            ActionChains(driver)\
                .move_to_element(driver.find_element_by_xpath('//html'))\
                .perform()
        except Exception as ex:
            logger.warning(f'{ex}, element: {e.tag_name}, {e.id}, {e.rect}')

        sleep(wait_time)

        try:
            _before = e.screenshot_as_base64
            # print(_before)
            try:
                ActionChains(driver).move_to_element(e).perform()
            except Exception as ex:
                logger.warning(
                    f'{type(ex)}, element: {e.tag_name}, {e.id}, {e.rect}')

            # sleep(wait_time)
            _after = e.screenshot_as_base64
            # print(_after)
            _hover = _after != _before

            if return_picts is False:  # Drop big picts
                _before = None
                _after = None

            return (_hover, _before, _after)

        except Exception as ex:
            logger.info(f"Suppress exception: {type(ex)}")
            return (False, None, None)

    except Exception as ex:
        logger.warning(f'Suppressed :{ex}')
    return


def get_all_elements(driver=None):
    """ Get all web elemets for a current page
        returns pandas dataframe
    """

    elements_all = driver.find_elements_by_xpath('//*')
    logger.info(f'Number of discovered elements: {len(elements_all)}')

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

    for e in tqdm(elements_all, desc='Collecting web elements features'):
        try:
            txt = e.get_attribute('text')
            tag_class = e.get_attribute("class")
            tag_onclick = e.get_attribute("onclick")
            tag_type = e.get_attribute("type")
            tag_role = e.get_attribute("role")
            tag_id = e.get_attribute("id")
        except Exception as ex:
            logger.error(f"{ex}, {e.id}, {e.tag_name}, {e.rect}")

        hover, hover_before, hover_after = is_hover(e=e, driver=driver)

        try:
            parents = e.find_elements_by_xpath('./..')
            if len(parents) > 1:
                raise('More then one parent for element:', e)
            parent_id = parents[0].id
        except Exception as ex:
            logger.info(f'Suppress exception: {ex}')
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


GET_ALL_ATTRIBUTES_JS = """
    var items = {};
    for (index = 0; index < arguments[0].attributes.length; ++index) {
        items[arguments[0].attributes[index].name]=arguments[0].attributes[index].value
    };
    return items;
"""


def get_all_attributes(driver, web_element):
    try:
        attr_dict = driver.execute_script(GET_ALL_ATTRIBUTES_JS, web_element)
        return attr_dict
    except Exception as ex:
        logger.info(f'Suppress exception: {type(ex)}')
        return dict()


def build_tree_dict(df: pd.DataFrame) -> dict:
    """
        Builds tree dict for
        get_parents_list
        df:pd.DataFrame must have columns: 'parent_id', 'element_id'

    """
    # tree_dict = dict(zip(df.element_id.values, df.parent_id.values))  # old implementation
    tree_dict = {
        r.element_id: None if r.element_id == r.parent_id else r.parent_id
        for _, r in df[['element_id', 'parent_id']].iterrows()
    }

    return tree_dict


def build_elements_dict(df: pd.DataFrame):
    """
        df: must have fields ['element_id', 'x', 'y', 'width', 'height', 'tag_name', 'displayed', 'is_hidden']
    """
    elements_dict = {
        r.element_id: {'tag': r.tag_name, 'box': (r.x, r.y, r.width, r.height), 'd': r.displayed, 'h': r.is_hidden}
        for _, r in df.iterrows()
    }
    return elements_dict


def build_elements_dataset(driver=None):
    """ Get all web elemets for a current page
        returns pandas dataframe

    """

    elements_list = driver.find_elements_by_xpath('//*')
    logger.info(f'Number of discovered elements: {len(elements_list)}')

    logger.info('collect features: text')
    text = [e.text for e in elements_list]

    logger.info('collect features: parent_id')
    parent_id = [e.find_elements_by_xpath('./..')[0].id
                 if e.tag_name != 'html' else None for e in elements_list]

    logger.info('collect features: element_id')
    elements_id = [e.id for e in elements_list]

    logger.info('collect features: rect')
    rect = [e.rect for e in elements_list]

    logger.info('collect features: tag_name')
    tag_name = [e.tag_name for e in elements_list]

    logger.info('collect features: displayed')
    displayed = [e.is_displayed() for e in elements_list]

    logger.info('collect features: enabled')
    enabled = [e.is_enabled() for e in elements_list]

    logger.info('collect features: selected')
    selected = [e.is_selected() for e in elements_list]

    attributes_list = [
        get_all_attributes(driver=driver, web_element=e)
        for e in tqdm(elements_list, desc='Collecting attributes')
    ]

    return pd.DataFrame({
        'parent_id': parent_id,
        'element_id': elements_id,
        'tag_name': tag_name,
        'text': text,
        'x': [e['x'] for e in rect],
        'y': [e['y'] for e in rect],
        'width': [e['width'] for e in rect],
        'height': [e['height'] for e in rect],
        'displayed': displayed,
        'enabled': enabled,
        'selected': selected,
        'attributes': attributes_list
        # 'attr_class': attr_class,
        # 'attr_id': attr_id,
        # 'attr_role': attr_role,
        # 'attr_type': attr_type,
        # 'attr_onmouseover': attr_onmouseover,
        # 'attr_onclick': attr_onclick,
        # 'attr_ondblclick': attr_ondblclick,
        # 'hover': hover_list,
        # 'hover_before': hover_before_list,
        # 'hover_after': hover_after_list
    })


def setup_web_driver():

    SITE_ROOT = 'https://jdi-testing.github.io/jdi-light/'
    LOGIN = 'Roman'
    PASSWORD = 'Jdi1234'
    WAIT_TIME_SECONDS = 7
    HEADLESS = True  # False

    options = Options()
    if HEADLESS:
        options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    CHROME_DRIVER_PATH = os.path.join(os.getcwd(), 'chromedriver.exe')
    if os.path.exists(CHROME_DRIVER_PATH):
        driver = selenium.webdriver.Chrome(
            executable_path=CHROME_DRIVER_PATH, options=options)
        driver.get(SITE_ROOT)

    driver.find_element_by_id("user-icon").click()
    driver.find_element_by_id("name").send_keys(LOGIN)
    driver.find_element_by_id("password").send_keys(PASSWORD)
    driver.find_element_by_id("login-button").click()
    sleep(WAIT_TIME_SECONDS)

    return driver


def accuracy(df: pd.DataFrame, y_true: str = 'y_true_label', is_hidden: str = 'is_hidden',
             y_pred: str = 'y_pred_label', verbose: bool = True, dummy: str = 'n/a'):
    """
        Calculates accuracy on all elements which are not "n/a"
        Parameters: y_true, y_pred are column names
    """
    total_cnt = df.shape[0]
    df = df[[y_true, y_pred]][((df[y_true] != dummy) | (df[y_pred] != dummy)) & (df[is_hidden] == 0)]
    n = df.shape[0]

    if n != 0:
        true_cnt = df[df[y_true] == df[y_pred]].shape[0]
        acc = true_cnt / n
        if verbose:
            ipython_displpay(HTML(f'<H2>Accuracy: {acc} <H2>'))
            logger.info(
                f'Accuracy:  {true_cnt}/{n} = {acc}, for {total_cnt} elements')
        return acc

    else:
        ipython_displpay('<h1>Exception: No predictions<h1>')
        logger.info('<h1>Exception: No predictions<h1>')
        raise Exception('No predictions')

    return None


COLUMNS = ['element_id', 'x', 'y', 'width', 'height', 'displayed', 'is_hidden']


def rule_base_predict(df: pd.DataFrame):
    """
        Find controls using rules
    """

    with open('dataset/classes.txt', 'r') as f:
        controls_encoder = {l.strip(): i for i, l in enumerate(f.readlines())}
        # controls_decoder = {v:k for k, v in controls_encoder.items()}

    # Parquet does not support empty dictionaries, let's fix this
    df.attributes = df.attributes.apply(lambda x: {} if x is None else x)

    radio_df = df[(df.tag_name == 'INPUT') & df.attributes.apply(lambda x: x.get('type') == 'radio')][COLUMNS]
    logger.info(f'Num radio buttons found: {radio_df.shape[0]}')

    radio2_df = df[(df.tag_name == 'LABEL') & (              # noqa
        df.attributes.apply(lambda x: 'c-radio' in str(x.get('class'))))][COLUMNS]
    logger.info(f'Num radio2 buttons found: {radio2_df.shape[0]}')

    # checkbox_df = df[(df.tag_name == 'INPUT') & (            # noqa
    #     df.attributes.apply(lambda x: x.get('type')) == 'checkbox')][COLUMNS]
    # logger.info(f'Num checkboxes found: {checkbox_df.shape[0]}')

    checkbox_df = df[df.attributes.apply(lambda x: x.get('class') == 'checkbox')][COLUMNS]
    logger.info(f'Num checkboxes found: {checkbox_df.shape[0]}')


    combobox_df = df[(df.tag_name == 'INPUT')                                         # noqa
                      & (df.attributes.apply(lambda x: x.get('type')) == 'text')      # noqa
                      & (df.attributes.apply(lambda x: x.get('role')) == 'combobox')  # noqa
                    ][COLUMNS]  # noqa
    logger.info(f"Num comboboxes/dropdowns found: {combobox_df.shape[0]}")

    # checkbox2_df = df[(df.tag_name == 'LABEL') & (
    #     df.attributes.apply(lambda x: 'c-checkbox-withText' in str(x.get('class')))) & (
    #     df.attributes.apply(lambda x: x.get('data-value') is not None))][COLUMNS]
    # logger.info(f'Num checkbox2 buttons found: {checkbox2_df.shape[0]}')

    text_df = df[(df.tag_name == 'INPUT')                                            # noqa
                 & (df.attributes.apply(lambda x: x.get('type')) == 'text')          # noqa
                 # & (df.attributes.apply(lambda x: x.get('role')) != 'combobox')    # noqa
                ][COLUMNS]  # noqa
    logger.info(f"Num textfields found: {text_df.shape[0]}")

    textnumber_df = df[(df.tag_name == 'INPUT')                                      # noqa
                       & (df.attributes.apply(lambda x: x.get('type')) == 'number')  # noqa
                      ][COLUMNS]  # noqa
    logger.info(f"Num texfields for numbers found: {textnumber_df.shape[0]}")

    range_df = df[(df.tag_name == 'INPUT')                                           # noqa
                  & (df.attributes.apply(lambda x: x.get('type')) == 'range')        # noqa
                 ][COLUMNS]  # noqa
    logger.info(f"Num ranges found: {range_df.shape[0]}")

    inputtext_df = df[(df.tag_name == 'INPUT')                                       # noqa
                      & (df.attributes.apply(lambda x: x.get('type') == ''))         # noqa
                     ][COLUMNS]  # noqa
    logger.info(f"Num ordinary text inputs found: {inputtext_df.shape[0]}")

    button_df = df[(df.tag_name == 'BUTTON')][COLUMNS]                               # noqa
    logger.info(f"Num buttons found: {button_df.shape[0]}")

    button1_df = df[df.attributes.apply(lambda x: x.get('class') == 'icon-search')][COLUMNS]  # noqa
    # print('Button1: ', button1_df.element_id.values)

    logger.info(f"Num buttons1 found: {button1_df.shape[0]}")

    button2_df = df[(df.tag_name == 'DIV')                                           # noqa
                      & (df.attributes.apply(lambda x: x.get('role') == 'button'))   # noqa
                     ][COLUMNS]  # noqa
    logger.info(f"Num buttons2 (Material-UI) found: {button2_df.shape[0]}")

    # link_df = df[(df.tag_name == 'A') & (df.attributes.apply(                        # noqa
    #     lambda x: x.get('href') is not None))][COLUMNS]
    link_df = df[df.tag_name == 'A'][COLUMNS]
    logger.info(f"Num links found: {link_df.shape[0]}")

    radio_df['label'] = controls_encoder['radiobutton']
    radio2_df['label'] = controls_encoder['radiobutton']
    checkbox_df['label'] = controls_encoder['checkbox']
    combobox_df['label'] = controls_encoder['dropdown']           # combobox/dropdown
    text_df['label'] = controls_encoder['textfield']
    button_df['label'] = controls_encoder['button']
    button1_df['label'] = controls_encoder['button']
    button2_df['label'] = controls_encoder['button']
    link_df['label'] = controls_encoder['link']
    textnumber_df['label'] = controls_encoder['textfield']
    inputtext_df['label'] = controls_encoder['textfield']
    range_df['label'] = controls_encoder['range']

    df_list = [radio_df,
               radio2_df,
               checkbox_df,
               # checkbox2_df,
               combobox_df,
               text_df,
               button_df,
               button1_df,
               button2_df,
               link_df,
               textnumber_df,
               inputtext_df,
               range_df
               ]

    controls_df = pd.concat(df_list)
    controls_df = controls_df[controls_df.displayed & (controls_df.is_hidden == 0)].copy()
    controls_df = controls_df[(controls_df.x >= 0) & (controls_df.y >= 0)].copy()

    return controls_df


@numba.jit
def to_yolo(label: int, x: int, y: int, w: int, h: int, img_width: int, img_height: int):
    if x <= 0 and y <= 0 and w == 0 and h == 0:
        return [label, 0.0, 0.0, 0.0, 0.0]

    # There are some elements with (width, height) = (0, 0), let's fix it
    if w == 0:
        w += 20
        x -= 6

    if h == 0:
        h += 20
        y -= 10

    return [label,
            round((x + w / 2) / img_width, 6),
            round((y + h / 2) / img_height, 6),
            round(w / img_width, 6),
            round(h / img_height, 6)]


@numba.jit
def from_yolo(x: float, y: float, w: float, h: float, img_width, img_height):
    x = x - w / 2.0
    y = y - h / 2.0
    return (int(x * img_width), int(y * img_height), int(w * img_width), int(h * img_height))


logger.info('Module utils.common is loaded...')
