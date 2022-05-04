from selenium import webdriver
import json
from pytz import timezone
import time
import datetime

option = webdriver.ChromeOptions()
option.add_argument(
    "user-agent='Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'")
option.add_argument('window-size=390,760')

option.add_experimental_option(
    "excludeSwitches", ['enable-automation', 'enable-logging'])
option.add_argument('--hide-scrollbars')  # seems invalid
option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('--disable-gpu')
option.add_argument('--disable-dev-shm-usage')


def get_xcm_img(phone, date=None):
    if date is None:
        date = datetime.datetime.now(
            timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S")
    browser = webdriver.Chrome(
        executable_path='./driver/chromedriver', options=option)
    # browser = webdriver.Chrome(
    #     executable_path='./driver/chromedriver.exe', options=option) # for Windows
    res_msg = {"status": "1", "code": "00", "errorDesc": "请求成功", "result": {"color": "green", "phone": phone[:3]+"****"+phone[-4:], "time": date, "message": "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"}, "queryId": ""}
    browser.get('https://xc.caict.ac.cn/#/result')
    browser.execute_script('localStorage.setItem("loginkey", "1");')
    browser.execute_script(
        f'localStorage.setItem("resMsg",\'{json.dumps(res_msg)}\');')
    browser.get('https://xc.caict.ac.cn/#/result')
    browser.refresh()
    browser.execute_script('document.body.style.overflow="hidden";')
    time.sleep(5)
    binary_content = browser.get_screenshot_as_png()
    browser.quit()
    return binary_content


def get_skm_img(token):
    url = f'https://jsstm.jszwfw.gov.cn/jkmIndex.html?token={token}'
    browser = webdriver.Chrome(
        executable_path='./driver/chromedriver', options=option)
    # browser = webdriver.Chrome(
    #     executable_path='./driver/chromedriver.exe', options=option) # for Windows
    browser.get(url)
    browser.execute_script('document.body.style.overflow="hidden";')
    time.sleep(5)
    binary_content = browser.get_screenshot_as_png()
    browser.quit()
    return binary_content
