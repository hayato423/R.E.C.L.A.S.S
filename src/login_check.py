"""
designer : 坂下直樹
date : 編集日(2020.06.23)
purpose : scombのログイン確認をする
"""
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from get_timetable import resource_path
#import chromedriver_binary


def login(USER, PASS):
    '''引数のデータでscombにログインできるか判定する.
      Args:
        USER(str): 学籍番号
        PASS(str): パスワード
      Returns:
        judge:判定結果
      '''
    options = Options()
    options.add_argument('--headless')
    # options.add_experimental_option('excludeSwitches',['enable-logging'])
    browser = webdriver.Chrome(executable_path=resource_path(
        '../driver/chromedriver.exe'), chrome_options=options)
    wait = WebDriverWait(browser, 20)
    url_login = "https://scomb.shibaura-it.ac.jp/portal/index"
    browser.get(url_login)
    time.sleep(1)
    try:
        login_button = browser.find_element_by_id("loginField")
        login_button.click()
        wait.until(EC.presence_of_all_elements_located)
        cur_url = browser.current_url
        trim_url = str(cur_url).replace('https://', '')
        basic_auth_url = 'https://' + USER + '%40sic:' + PASS + '@' + trim_url
        browser.get(basic_auth_url)
        wait.until(EC.presence_of_all_elements_located)
        next_button = browser.find_element_by_id('continueButton')
        next_button.click()
        wait.until(EC.presence_of_all_elements_located)
        cur_url = browser.current_url
        judge = 0
        if cur_url == 'https://scomb.shibaura-it.ac.jp/portal/contents/home/':
            judge = 1
            return judge
    except TimeoutException as te:
        judge = 2
        return judge
    except Exception as e:
        judge = 3
        return judge
    finally:
        browser.quit()
