from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import chromedriver_binary

driver = webdriver.Chrome()
wait = WebDriverWait(driver,10)

ID = 'al18080@sic'
PASSWORD = '3490WaRaSu!9745'

error_flg = False

scomb_url = 'https://scomb.shibaura-it.ac.jp/portal/index'

driver.get(scomb_url)
wait.until(EC.presence_of_all_elements_located)
try:
  login_button = driver.find_element_by_id("loginField")
  login_button.click()
  wait.until(EC.alert_is_present())
  Alert(driver).send_keys(ID + Keys.TAB + PASSWORD)
  Alert(driver).accept()
  wait.until(EC.presence_of_all_elements_located)
  driver.find_element_by_id('continueButton').click()
  wait.until(EC.presence_of_all_elements_located)
except Exception as e:
  error_flg = True
  print(e)
