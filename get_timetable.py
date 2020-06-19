from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import chromedriver_binary

driver = webdriver.Chrome()
wait = WebDriverWait(driver,20)

ID = 'al18080'
PASSWORD = '3490WaRaSu!9745'

error_flg = False

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

except Exception as e:
  error_flg = True
  print(e)
