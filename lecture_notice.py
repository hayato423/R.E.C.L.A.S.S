'''
disingner : 寺尾颯人
date      : 2020.07.01
purpose   : 毎時間授業があるか確認する.
'''

import schedule
import time
import datetime
import sqlite3
import PySimpleGUI as sg
from zoom import join_meeting

def confirm_lecture(day,time):
  '''授業があるか確認し、あった場合zoomに参加するか確認する。.
    Args:
    day : 曜日
    time : 時限
    Returns: なし
  '''
  conn = sqlite3.connect('reclass.db')
  cur = conn.cursor()
  SQL = 'select lecture_name from lectures where day=? and time=?'
  cur.execute(SQL,(day,time))
  execte_result = cur.fetchone()
  LECTURE_NAME = execte_result[0]
  if LECTURE_NAME != None:
    CONFIRM_STR = '授業「'+LECTURE_NAME+'」が始まります。ミーティングに参加しますか？'
    is_join = sg.PopupYesNo(CONFIRM_STR)
    if is_join == 'Yes':
      SQL = 'select url from zoomURL where lecture_name = ?'
      cur.execute(SQL,(LECTURE_NAME,))
      execte_result = cur.fetchone()
      URL = execte_result[0]
      if URL != None:
        print(URL)
        join_meeting(URL)
      else:
        sg.popup('URLが見つかりませんでした')


confirm_lecture(2,0)