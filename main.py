'''
disingner : 寺尾颯人
date      : 2020.06.23
purpose   : プログラムのメイン処理
'''

import home
import sqlite3


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

  home_window = home.Home()
  home_window.open()
  conn.close()
