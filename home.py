'''
disingner : 寺尾颯人
date      : 2020.06.23
purpose   : ホーム画面クラス
'''

import PySimpleGUI as sg
import config
import lecture
import scomb
from get_timetable import get_timetable
import configparser
import sqlite3
from org_factory import dict_factory
import sys,os
import threading
import schedule
import time
import datetime


class Home:
  def __init__(self):
    #時間割リスト [時間][曜日]
    self.time_table = [[None]*5 for i in range(6)]
    #lectureインスタンスを格納するリスト
    self.lecture_instances = [[None]*5 for i in range(6)]

    #データベースから時間割を取得
    conn = sqlite3.connect('reclass.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute('select * from lectures')
    new_lectures_list = cur.fetchall()
    self.lectures_data = new_lectures_list

    #各課題の辞書型データ
    self.task_data=[
      {'lecture_name':'ソフトウェア工学','task_name':'シークエンス図','deadline':'??/!!'}
    ]

    #授業のデータを時間割リストに格納
    for l in self.lectures_data:
      self.time_table[l['day']][l['time']] = l


  def job(self):
    print(datetime.datetime.now())

  def cron(self):
    schedule.every(1).seconds.do(self.job)
    while True:
      schedule.run_pending()
      time.sleep(1)



  def open(self):
    '''ホーム画面を開き、イベント処理を行う.
    Args: なし
    Returns: なし
    '''

    '''マルチスレッド処理'''
    t1 = threading.Thread(target=self.cron)
    t1.setDaemon(True)
    t1.start()


    '''画面構成処理'''
    width = 16
    #画面レイアウト
    #時間割レイアウト
    timetable_layout = [
      [sg.Text('Main Window'),sg.Button('設定',key='config_btn'),sg.Button('Scomb',key='scomb_btn'),sg.Button('更新',key='update_timetable')],
      [sg.Text('',size=(2,1)),
      sg.Text('月',size=(width,1),justification='center'),
      sg.Text('火',size=(width,1),justification='center'),
      sg.Text('水',size=(width,1),justification='center'),
      sg.Text('木',size=(width,1),justification='center'),
      sg.Text('金',size=(width,1),justification='center'),
      sg.Text('土',size=(width,1),justification='center'),],
      [sg.Text('1')],
      [sg.Text('2')],
      [sg.Text('3')],
      [sg.Text('4')],
      [sg.Text('5')]
    ]

    #時間割に基づいてレイアウトを追加
    for time in range(5):
      for day in range(6):
        if self.time_table[day][time] is None:
          timetable_layout[time+2].append(sg.Button('',key=str(day)+str(time),size=(width,3)))
        else:
          lec = self.time_table[day][time]
          timetable_layout[time+2].append(sg.Button(lec['lecture_name'],key=str(day)+str(time),size=(width,3)))
          instance = lecture.Lecture(lec['lecture_name'],lec['teacher_name'])
          self.lecture_instances[day][time] = instance

    #課題表示レイアウト
    task_layout=[
      [sg.Text('ソフトウェア工学')],
      [sg.Text('シークエンス図')],
      [sg.Text('2020/??/!!')]
    ]

    main_layout=[[sg.Frame('',timetable_layout),sg.Frame('課題一覧',task_layout)]]



    #ウィンドウ生成
    main_window = sg.Window('Main',layout=main_layout)
    config_window = config.Config()
    scomb_window = scomb.Scomb()



    while True:
      main_event , main_value = main_window.read()

      if main_event is None:
        break

      elif main_event == 'config_btn':
        config_window.open()

      elif main_event == 'scomb_btn':
        scomb_window.open()

      elif main_event == '00':
        if self.lecture_instances[0][0] is not None:
          self.lecture_instances[0][0].open()
      elif main_event == '01':
        if self.lecture_instances[0][1] is not None:
          self.lecture_instances[0][1].open()
      elif main_event == '02':
        if self.lecture_instances[0][2] is not None:
          self.lecture_instances[0][2].open()
      elif main_event == '03':
        if self.lecture_instances[0][3] is not None:
          self.lecture_instances[0][3].open()
      elif main_event == '04':
        if self.lecture_instances[0][4] is not None:
          self.lecture_instances[0][4].open()

      elif main_event == '10':
        if self.lecture_instances[1][0] is not None:
          self.lecture_instances[1][0].open()
      elif main_event == '11':
        if self.lecture_instances[1][1] is not None:
          self.lecture_instances[1][1].open()
      elif main_event == '12':
        if self.lecture_instances[1][2] is not None:
          self.lecture_instances[1][2].open()
      elif main_event == '13':
        if self.lecture_instances[1][3] is not None:
          self.lecture_instances[1][3].open()
      elif main_event == '14':
        if self.lecture_instances[1][4] is not None:
          self.lecture_instances[1][4].open()

      elif main_event == '20':
        if self.lecture_instances[2][0] is not None:
          self.lecture_instances[2][0].open()
      elif main_event == '21':
        if self.lecture_instances[2][1] is not None:
          self.lecture_instances[2][1].open()
      elif main_event == '22':
        if self.lecture_instances[2][2] is not None:
          self.lecture_instances[2][2].open()
      elif main_event == '23':
        if self.lecture_instances[2][3] is not None:
          self.lecture_instances[2][3].open()
      elif main_event == '24':
        if self.lecture_instances[2][4] is not None:
          self.lecture_instances[2][4].open()

      elif main_event == '30':
        if self.lecture_instances[3][0] is not None:
          self.lecture_instances[3][0].open()
      elif main_event == '31':
        if self.lecture_instances[3][1] is not None:
          self.lecture_instances[3][1].open()
      elif main_event == '32':
        if self.lecture_instances[3][2] is not None:
          self.lecture_instances[3][2].open()
      elif main_event == '33':
        if self.lecture_instances[3][3] is not None:
          self.lecture_instances[3][3].open()
      elif main_event == '34':
        if self.lecture_instances[3][4] is not None:
          self.lecture_instances[3][4].open()

      elif main_event == '40':
        if self.lecture_instances[4][0] is not None:
          self.lecture_instances[4][0].open()
      elif main_event == '41':
        if self.lecture_instances[4][1] is not None:
          self.lecture_instances[4][1].open()
      elif main_event == '42':
        if self.lecture_instances[4][2] is not None:
          self.lecture_instances[4][2].open()
      elif main_event == '43':
        if self.lecture_instances[4][3] is not None:
          self.lecture_instances[4][3].open()
      elif main_event == '44':
        if self.lecture_instances[4][4] is not None:
          self.lecture_instances[4][4].open()

      elif main_event == '50':
        if self.lecture_instances[5][0] is not None:
          self.lecture_instances[5][0].open()
      elif main_event == '51':
        if self.lecture_instances[5][1] is not None:
          self.lecture_instances[5][1].open()
      elif main_event == '52':
        if self.lecture_instances[5][2] is not None:
          self.lecture_instances[5][2].open()
      elif main_event == '53':
        if self.lecture_instances[5][3] is not None:
          self.lecture_instances[5][3].open()
      elif main_event == '54':
        if self.lecture_instances[5][4] is not None:
          self.lecture_instances[5][4].open()

      elif main_event == 'update_timetable':
        #config.iniからidとパスワードを読み込み
        config_ini = configparser.ConfigParser()
        config_ini.read('config.ini',encoding='utf-8')
        ID = config_ini['Scomb']['ID']
        PASSWORD = config_ini['Scomb']['Password']
        status , msg = get_timetable(ID,PASSWORD)
        #時間割取得成功したら
        if status == 0:
          conn = sqlite3.connect('reclass.db')
          conn.row_factory = dict_factory
          cur = conn.cursor()
          cur.execute('select * from lectures')
          new_lectures_list = cur.fetchall()
          self.lectures_data = new_lectures_list
          for l in self.lectures_data:
            self.time_table[l['day']][l['time']] = l
          sg.Popup(msg)
          main_window.close()
          self.open()
        else:
          sg.Popup(msg)



    main_window.close()
    return 0


