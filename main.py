'''
disingner : 寺尾颯人
date      : 2020.06.23
purpose   : プログラムのメイン処理
'''

import home
import sqlite3
from lecture_notice import lecture_schedule,day_update
import schedule
import os
import configparser


if __name__ == "__main__":
  dbname = 'reclass.db'
  #データベース接続
  conn = sqlite3.connect(dbname)
  cur = conn.cursor()
  #テーブル作成
  CREATE_LECTURES_TABLE = '''CREATE TABLE IF NOT EXISTS lectures(lecture_name TEXT, teacher_name TEXT, day INTEGER, time INTERGER )'''
  cur.execute(CREATE_LECTURES_TABLE)
  CREATE_TASKS_TABLE = '''CREATE TABLE IF NOT EXISTS tasks(lecture_name TEXT, teacher_name TEXT, task_name TEXT, submit_state INTEGER,deadline DATETIME)'''
  cur.execute(CREATE_TASKS_TABLE)
  CREATE_ZOOMURL_TABLE = ''' CREATE TABLE IF NOT EXISTS zoomURL(lecture_name TEXT, url TEXT)'''
  cur.execute(CREATE_ZOOMURL_TABLE)
  conn.commit()

  if not os.path.exists('config.ini'):
    config_ini = configparser.ConfigParser()
    config_ini['Config'] = {
      'alert_task' : 1,
      'connect_zoom' : 5,
      'update' : 6
    }
    with open('config.ini','w') as file:
      config_ini.write(file)

  if not os.path.exists('scomb.ini'):
    scomb_ini = configparser.ConfigParser()
    scomb_ini['Scomb'] = {
      'id' : '',
      'password' : ''
    }
    with open('scomb.ini','w') as file:
      scomb_ini.write(file)


  #授業スケジュールの設定
  lecture_schedule()
  schedule.every().day.at("00:00").do(day_update)

  home_window = home.Home()
  home_window.open()
  conn.close()
