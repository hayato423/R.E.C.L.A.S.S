import configparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import chromedriver_binary
import datetime
import sqlite3


#config.iniの読み込み
config_ini = configparser.ConfigParser()
config_ini.read('config.ini',encoding='utf-8')

ID = config_ini['Scomb']['ID']
PASSWORD = config_ini['Scomb']['Password']



def get_timetable(id,password):
  lectures = []

  options = Options()
  options.add_argument('--headless')
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
    #basic認証
    basic_auth_url = 'https://' + id + '%40sic:' + password + '@' + trim_url
    driver.get(basic_auth_url)
    wait.until(EC.presence_of_all_elements_located)

    next_button = driver.find_element_by_id('continueButton')
    next_button.click()
    wait.until(EC.presence_of_all_elements_located)
    cur_url = driver.current_url
    #ログインできたか確認
    if cur_url == 'https://scomb.shibaura-it.ac.jp/portal/contents/home/':
      #lmsボタンをクリック
      lms_button = driver.find_element_by_id('navi-lms')
      lms_button.click()
      wait.until(EC.presence_of_all_elements_located)
      #時間割の表示をスケジュールに変更
      display_mode_button = driver.find_element_by_id('displayMode1')
      display_mode_button.click()
      #現在の曜日番号を取得
      day_num = datetime.date.today().weekday()
      for time in range(1,7+1):
        for day in range(1,7+1):
          lecture_name = driver.find_element_by_xpath("//tr[@class='classTitle'][{time}]/td[{day}]".format(time=time,day=day)).text
          lecture_detail = driver.find_element_by_xpath("//tr[@class='classDetail'][{time}]/td[{day}]".format(time=time,day=day)).text
          #文字列を整形
          teacher_name = lecture_detail.replace('【教室】','')
          teacher_name = teacher_name.replace('\u3000',' ')
          teacher_name = teacher_name.replace('\n','')
          lecture_data = {'lecture_name':lecture_name,'teacher_name':teacher_name,'day':day_num,'time':time-1}
          day_num += 1
          if day_num == 7:
            day_num = 0
          if lecture_name != ' ' and teacher_name != ' ':
            lectures.append(lecture_data)

      print(lectures)


  except TimeoutException as te:
      print(te)
  except Exception as e:
      print(e)

get_timetable(ID,PASSWORD)

