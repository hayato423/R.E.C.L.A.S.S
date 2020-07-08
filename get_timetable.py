'''
disingner : 寺尾颯人
date      : 2020.06.23
purpose   : scombから時間割を取得
'''

import configparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#import chromedriver_binary
import datetime
import sqlite3
import sys
import os

def resource_path(relative_path):
  try:
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.dirname(__file__)
  return os.path.join(base_path, relative_path)



def get_timetable(id,password):
  '''
  scombから時間割を取得する.
  Args:
    id(str): 学籍番号
    password(str):scombのパスワード
  Return:
    int:更新の状態 0:成功 -1:失敗
    str:終了メッセージ
  '''
  status = 0
  msg = ''
  lectures = []
  options = Options()
  options.add_argument('--headless')
  driver = webdriver.Chrome(executable_path=resource_path('./driver/chromedriver.exe'), chrome_options=options)
  wait = WebDriverWait(driver,20)
  scomb_url = 'https://scomb.shibaura-it.ac.jp/portal/index'
  driver.get(scomb_url)
  wait.until(EC.presence_of_all_elements_located)

  try:
    #ログインボタンをクリック
    login_button = driver.find_element_by_id("loginField")
    login_button.click()
    wait.until(EC.presence_of_all_elements_located)

    cur_url = driver.current_url
    trim_url = str(cur_url).replace('https://','')
    #basic認証
    basic_auth_url = 'https://' + id + '%40sic:' + password + '@' + trim_url
    driver.get(basic_auth_url)
    wait.until(EC.presence_of_all_elements_located)

    #次へボタンをクリック
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
          lecture_data = [lecture_name,teacher_name,day_num,time-1]
          #曜日番号を更新
          day_num += 1
          if day_num == 7:
            day_num = 0
          #授業の情報があるならlecturesに追加
          if lecture_name != ' ' and teacher_name != ' ':
            lectures.append(lecture_data)

      #データベースを更新
      update_table(lectures)
      msg = '更新が完了しました'
      status = 0
    else:
      msg = 'ログインに失敗しました'
      status = -1
  except TimeoutException as te:
      print(te)
  except Exception as e:
      msg = 'エラーが発生しました'
      status = -1
  finally:
    driver.quit()
    return status,msg




def update_table(lectures_list):
  '''
  取得した時間割をデータベースに保存する
  Args:
    lectures_list:([str,str,int,int])授業情報のリスト
  Return:
    なし
  '''
  conn = sqlite3.connect('reclass.db')
  cur = conn.cursor()
  delete_all = 'delete from lectures'
  cur.execute(delete_all)
  for lec in lectures_list:
      query = 'insert into  lectures (lecture_name,teacher_name,day,time) values(?,?,?,?)'
      cur.execute(query,tuple(lec))
  conn.commit()
  conn.close()


