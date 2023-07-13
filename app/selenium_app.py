import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")
response = requests.get('https://meduza.io')
page_content = response.content
page_content_str = page_content.decode()
driver = webdriver.Chrome(options=chrome_options)
driver.get('about:blank')
driver.execute_script("document.write(arguments[0]);", page_content_str)
invisible_elements = driver.execute_script("""
    var elements = document.querySelectorAll('*');
    var invisibleElements = [];

    for (var i = 0; i < elements.length; i++) {
        var element = elements[i];
        var style = window.getComputedStyle(element);
        var display = style.getPropertyValue('display');
        var visibility = style.getPropertyValue('visibility');

        if (display === 'none' || visibility === 'hidden') {
            invisibleElements.push(element);
        }
    }

    return invisibleElements;
""")
for element in invisible_elements:
    print(element)
