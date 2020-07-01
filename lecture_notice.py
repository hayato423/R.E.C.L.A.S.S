'''
disingner : 寺尾颯人
date      : 2020.07.01
purpose   : 毎時間授業があるか確認し,通知,zoom参加を行う.
'''
from plyer import notification
import sqlite3
import PySimpleGUI as sg
from zoom import join_meeting
import configparser
import time
import datetime

def confirm_lecture(day,time):
  '''授業があるか確認し、あった場合zoomに参加するか確認する。.
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