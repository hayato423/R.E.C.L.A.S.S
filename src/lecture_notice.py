'''
disingner : 寺尾颯人
date      : 2020.07.04
purpose   : 毎時間授業があるか確認し,通知,zoom参加を行う.
'''

import sqlite3
import PySimpleGUI as sg
from zoom import join_meeting
import configparser
import time
import datetime
import schedule
from plyer import notification

def confirm_lecture(day,time):
  '''授業があるか確認し、あった場合zoomに参加するか確認する.
    Args:
    day : 曜日
    time : 時限
    Returns: なし
  '''
  try:
    #データベースに接続
    conn = sqlite3.connect('reclass.db')
    cur = conn.cursor()
    #day曜日のtime時間目の授業名を取得する
    SQL = 'select lecture_name from lectures where day=? and time=?'
    cur.execute(SQL,(day,time))
    execte_result = cur.fetchone()
    #授業があるならポップアップ表示
    if execte_result != None:
      LECTURE_NAME = execte_result[0]
      CONFIRM_STR = '授業「'+LECTURE_NAME+'」が始まります。ミーティングに参加しますか？'
      #windowsバルーン通知
      notification.notify(
        title='授業通知',
        message = CONFIRM_STR,
        app_name = 'reclass'
      )
      is_join = sg.PopupYesNo(CONFIRM_STR)
      if is_join == 'Yes':
        #授業名からURLを取得
        SQL = 'select url from zoomURL where lecture_name = ?'
        cur.execute(SQL,(LECTURE_NAME,))
        execte_result = cur.fetchone()
        if execte_result != None:
          URL = execte_result[0]
          #URLが存在するなら接続
          join_meeting(URL)
        else:
          sg.popup('URLが見つかりませんでした')
  except Exception as e:
    sg.popup(e)

def lecture_schedule():
  '''授業スケジュールの設定.
    Args:なし
    Returns: なし
  '''
  config_ini = configparser.ConfigParser()
  config_ini.read('config.ini')
  start_time = config_ini['Config']['connect_zoom']
  #1限目
  first_period_time = datetime.datetime.combine(datetime.date.today(),datetime.time(9,0)) - datetime.timedelta(minutes=int(start_time))
  first_period_time = first_period_time.strftime("%H:%M")
  #2限目
  second_period_time = datetime.datetime.combine(datetime.date.today(),datetime.time(10,50)) - datetime.timedelta(minutes=int(start_time))
  second_period_time = second_period_time.strftime("%H:%M")
  #3限目
  third_period_time = datetime.datetime.combine(datetime.date.today(),datetime.time(13,10)) - datetime.timedelta(minutes=int(start_time))
  third_period_time = third_period_time.strftime("%H:%M")
  #4限目
  fourth_period_time = datetime.datetime.combine(datetime.date.today(),datetime.time(15,0)) - datetime.timedelta(minutes=int(start_time))
  fourth_period_time = fourth_period_time.strftime("%H:%M")
  #5限目
  fifth_period_time = datetime.datetime.combine(datetime.date.today(),datetime.time(16,50)) - datetime.timedelta(minutes=int(start_time))
  fifth_period_time = fifth_period_time.strftime("%H:%M")

  #スケジュール設定
  schedule.every().day.at(first_period_time).do(confirm_lecture,day=datetime.date.today().weekday(),time=0).tag('lecture')
  schedule.every().day.at(second_period_time).do(confirm_lecture,day=datetime.date.today().weekday(),time=1).tag('lecture')
  schedule.every().day.at(third_period_time).do(confirm_lecture,day=datetime.date.today().weekday(),time=2).tag('lecture')
  schedule.every().day.at(fourth_period_time).do(confirm_lecture,day=datetime.date.today().weekday(),time=3).tag('lecture')
  schedule.every().day.at(fifth_period_time).do(confirm_lecture,day=datetime.date.today().weekday(),time=4).tag('lecture')

  '''
  while True:
    schedule.run_pending()
    print(datetime.datetime.now())
    #time.sleep(1)
  '''

def day_update():
  '''授業スケジュールの曜日更新.
    Args:なし
    Returns: なし
  '''
  schedule.clear('lecture')
  lecture_schedule()