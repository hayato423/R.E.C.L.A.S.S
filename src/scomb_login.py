from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import chromedriver_binary




def login_confirm(ID,PASSWORD):
  msg = ''
  can_login = False
  options = Options()
  #options.add_argument('--headless')
  driver = webdriver.Chrome(chrome_options=options)
  wait = WebDriverWait(driver,20)
  scomb_url = 'https://scomb.shibaura-it.ac.jp/portal/index'
  driver.get(scomb_url)
  wait.until(EC.presence_of_all_elements_located)

  try:
    login_button = driver.find_element_by_id("loginField")
    login_button.click()
    wait.until(EC.presence_of_all_elements_located)
    cur_url = driver.current_url
    trim_url = str(cur_url).replace('https://','')
    basic_auth_url = 'https://' + ID + '%40sic:' + PASSWORD + '@' + trim_url
    driver.get(basic_auth_url)
    wait.until(EC.presence_of_all_elements_located)
    next_button = driver.find_element_by_id('continueButton')
    next_button.click()
    wait.until(EC.presence_of_all_elements_located)
    cur_url = driver.current_url
    if cur_url == 'https://scomb.shibaura-it.ac.jp/portal/contents/home/':
      msg = 'ログインに成功しました'
      can_login = True
      return can_login , msg
  except TimeoutException as te:
    msg = 'タイムアウトしました'
    can_login = False
    return can_login, msg
  except Exception as e:
    msg = '例外が発生しました'
    print(e)
    can_login = False
    return can_login, msg