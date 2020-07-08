'''
disingner : 寺尾颯人
date      : 2020.06.23
purpose   : zoomのミーティングに参加する
'''
import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
#import chromedriver_binary
import os
import signal
from time import sleep
from get_timetable import resource_path


def join_meeting(url):
  '''
  引数urlのzoomミーティングに参加する
  Args:
    url:参加するミーティングのurl
  Return:
    なし
  '''
  try:
    driver = webdriver.Chrome(executable_path=resource_path('./driver/chromedriver.exe'))
    wait = WebDriverWait(driver,20)
    #引数のurlにアクセス
    driver.get(url)
    wait.until(EC.invisibility_of_element_located)
    #launch meeting をクリック
    launch_meeting_button = driver.find_element_by_xpath("//div[@class='_2XjT-0pJ']/div/div[2]/h3/a[1]")
    launch_meeting_button.click()
  except Exception as e:
    sg.popup("アクセスに失敗しました")
  finally:
    os.kill(driver.service.process.pid,signal.SIGTERM)
