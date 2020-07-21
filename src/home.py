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
from task_reload import task_reload
import configparser
import sqlite3
from org_factory import dict_factory
import sys,os
import threading
import schedule
import time
import datetime
import task


class Home:
  def __init__(self):
    '''ホーム画面の初期化を行う.
    Args: なし
    Returns: なし
    '''
    #時間割リスト [時間][曜日]
    self.time_table = [[None]*5 for i in range(6)]
    #lectureインスタンスを格納するリスト
    self.lecture_instances = [[None]*5 for i in range(12)]
    #課題リスト
    self.task_data=[[None] * 15]
    #taskインスタンスを格納するリスト
    self.task_instances=[]

    #データベースから時間割を取得
    conn = sqlite3.connect('reclass.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute('select * from lectures')
    new_lectures_list = cur.fetchall()
    self.lectures_data = new_lectures_list

    #データベースから課題を取得
    cur.execute('select * from tasks')
    new_tasks_list = cur.fetchall()
    self.task_data = new_tasks_list

    '''
    #各課題の辞書型データ
    conn=sqlite3.connect('reclass.db')
    conn.row_factory=dict_factory
    c=conn.cursor()
    c.execute('select * from tasks')
    new_task_list=c.fetchall()
    self.task_d=new_task_list
    '''

    #授業のデータを時間割リストに格納
    for l in self.lectures_data:
      self.time_table[l['day']][l['time']] = l

  def update_timetable(self,window):
    '''時間割の更新を行う.
    Args:
      window : ウィンドウオブジェクト
    Returns: なし
    '''
    #config.iniからidとパスワードを読み込み
    scomb_ini = configparser.ConfigParser()
    scomb_ini.read('./scomb.ini',encoding='utf-8')
    ID = scomb_ini['Scomb']['ID']
    PASSWORD = scomb_ini['Scomb']['Password']
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
      window.close()
      self.open()
    else:
      sg.Popup(msg)

  def update_task(self,window):
    '''課題更新を行う.
    Args:
      window : ウィンドウオブジェクト
    Returns: なし
    '''
    status, msg = task_reload()
    if status == 0:
      conn = sqlite3.connect('reclass.db')
      conn.row_factory = dict_factory
      cur = conn.cursor()
      cur.execute('select * from tasks')
      new_tasks_list = cur.fetchall()
      self.task_data = new_tasks_list
      window.close()
      self.open()


  def open(self):
    '''ホーム画面を開き、イベント処理を行う.
    Args: なし
    Returns: なし
    '''

    '''マルチスレッド処理
    t1 = threading.Thread(target=lecture_cron)
    t1.setDaemon(True)
    #t1.start()
    '''


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

    #課題に基づいてレイアウトを追加
    task_layout=[[sg.Text('課題一覧'),sg.Button('更新',key='update_task')]]

    for l in range(len(self.task_instances),15):
      self.task_instances.append(None)

    task_index = 0
    for l in  self.task_data:
      if l['complete'] != '済み':
        task_layout.append([sg.Button(l['task_name'],size=(width,3),key='task'+str(task_index))])
        instance = task.Task(l['lecture_name'],l['task_name'],l['deadline'],l['complete'])
        self.task_instances[task_index] = instance
        task_index += 1



    '''
    for l in self.task_instances:
      print(l)
    '''

    main_layout=[[sg.Frame('',timetable_layout),sg.Frame('',task_layout)]]


    #ウィンドウ生成
    main_window = sg.Window('R.E.C.L.A.S.S',layout=main_layout)
    config_window = config.Config()
    scomb_window = scomb.Scomb()



    while True:
      main_event , main_value = main_window.read(timeout=100,timeout_key='timeout')

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

      elif main_event == 'task0':
        if self.task_instances[0] is not None:
          self.task_instances[0].open()

      elif main_event == 'task1':
        if self.task_instances[1] is not None:
          self.task_instances[1].open()

      elif main_event == 'task2':
        if self.task_instances[2] is not None:
          self.task_instances[2].open()

      elif main_event == 'task3':
        if self.task_instances[3] is not None:
          self.task_instances[3].open()

      elif main_event == 'task4':
        if self.task_instances[4] is not None:
          self.task_instances[4].open()

      elif main_event == 'task5':
        if self.task_instances[5] is not None:
          self.task_instances[5].open()

      elif main_event == 'task6':
        if self.task_instances[6] is not None:
          self.task_instances[6].open()

      elif main_event == 'task7':
        if self.task_instances[7] is not None:
          self.task_instances[7].open()

      elif main_event == 'task8':
        if self.task_instances[8] is not None:
          self.task_instances[8].open()

      elif main_event == 'task9':
        if self.task_instances[9] is not None:
          self.task_instances[9].open()

      elif main_event == 'update_timetable':
        self.update_timetable(main_window)

      elif main_event == 'update_task':
        self.update_task(main_window)


      elif main_event == 'timeout':
        schedule.run_pending()




    main_window.close()
    return 0


