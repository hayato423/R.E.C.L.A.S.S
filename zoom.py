'''
disingner : 寺尾颯人
date      : 2020.06.23
purpose   : zoomのミーティングに参加する
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_binary
from time import sleep


def join_meeting(url):
  '''
  引数urlのzoomミーティングに参加する
  Args:
    url:参加するミーティングのurl
  Return:
    なし
  '''
  driver = webdriver.Chrome()
  wait = WebDriverWait(driver,20)
  #引数のurlにアクセス
  driver.get(url)
  wait.until(EC.invisibility_of_element_located)
  #launch meeting をクリック
  launch_meeting_button = driver.find_element_by_xpath("//div[@class='_2XjT-0pJ']/div/div[2]/h3/a[1]")
  launch_meeting_button.click()
  sleep(1)

