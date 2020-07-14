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
    #時間割リスト [時間][曜日]
    self.time_table = [[None]*5 for i in range(6)]
    #lectureインスタンスを格納するリスト
    self.lecture_instances = [[None]*5 for i in range(12)]
    #課題リスト
    self.task_data=[[None]*5 for i in range(6)]
    #taskインスタンスを格納するリスト
    self.task_instances=[[None]*5 for i in range(6)]

    #データベースから時間割を取得
    conn = sqlite3.connect('reclass.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute('select * from lectures')
    new_lectures_list = cur.fetchall()
    self.lectures_data = new_lectures_list

    #各課題の辞書型データ
    conn=sqlite3.connect('reclass.db')
    conn.row_factory=dict_factory
    c=conn.cursor()
    c.execute('select * from tasks')
    new_task_list=c.fetchall()
    self.task_d=new_task_list

    #授業のデータを時間割リストに格納
    for l in self.lectures_data:
      self.time_table[l['day']][l['time']] = l

    #課題のデータをリストに格納
    for l in self.task_d:
      self.task_data[l['day']][l['time']]=l


  def update_timetable(self,window):
    #config.iniからidとパスワードを読み込み
    scomb_ini = configparser.ConfigParser()
    scomb_ini.read('../scomb.ini',encoding='utf-8')
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
    if status==0:
      conn=sqlite3.connect('reclass.db')
      conn.row_factory=dict_factory
      c=conn.cursor()
      c.execute('select * from tasks')
      new_task_list=c.fetchall()
      self.task_d=new_task_list
      for l in self.task_d:
        self.task_data[l['day']][l['time']]=l
      sg.Popup(msg)
      window.close()
      self.open()
    else:
      sg.Popup(msg)

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

    #課題表示レイアウト
    task_layout=[[sg.Text('課題一覧')]]
    for time in range(5):
      for day in range(6):
        if self.task_data[day][time] is not None:
          tk=self.task_data[day][time]
          task_layout.append[sg.Button(tk['task_name'])]
          instance=task.Task(tk['lecture_name'],tk['task_name'],tk['deadline'])
          self.task_instances[day+6][time]=instance

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

      elif main_event == '60':
        if self.task_instances[6][0] is not None:
          self.task_instances[6][0].open()
      elif main_event == '61':
        if self.task_instances[6][1] is not None:
          self.task_instances[6][1].open()
      elif main_event == '62':
        if self.task_instances[6][2] is not None:
          self.task_instances[6][2].open()
      elif main_event == '63':
        if self.task_instances[6][3] is not None:
          self.task_instances[6][3].open()
      elif main_event == '64':
        if self.task_instances[6][4] is not None:
          self.task_instances[6][4].open()

      elif main_event == '70':
        if self.task_instances[7][0] is not None:
          self.task_instances[7][0].open()
      elif main_event == '71':
        if self.task_instances[7][1] is not None:
          self.task_instances[7][1].open()
      elif main_event == '72':
        if self.task_instances[7][2] is not None:
          self.task_instances[7][2].open()
      elif main_event == '73':
        if self.task_instances[7][3] is not None:
          self.task_instances[7][3].open()
      elif main_event == '74':
        if self.task_instances[7][4] is not None:
          self.task_instances[7][4].open()

      elif main_event == '80':
        if self.task_instances[8][0] is not None:
          self.task_instances[8][0].open()
      elif main_event == '81':
        if self.task_instances[8][1] is not None:
          self.task_instances[8][1].open()
      elif main_event == '82':
        if self.task_instances[8][2] is not None:
          self.task_instances[8][2].open()
      elif main_event == '83':
        if self.task_instances[8][3] is not None:
          self.task_instances[8][3].open()
      elif main_event == '84':
        if self.task_instances[8][4] is not None:
          self.task_instances[8][4].open()

      elif main_event == '90':
        if self.task_instances[9][0] is not None:
          self.task_instances[9][0].open()
      elif main_event == '91':
        if self.task_instances[9][1] is not None:
          self.task_instances[9][1].open()
      elif main_event == '92':
        if self.task_instances[9][2] is not None:
          self.task_instances[9][2].open()
      elif main_event == '93':
        if self.task_instances[9][3] is not None:
          self.task_instances[9][3].open()
      elif main_event == '94':
        if self.task_instances[9][4] is not None:
          self.task_instances[9][4].open()

      elif main_event == '100':
        if self.task_instances[10][0] is not None:
          self.task_instances[10][0].open()
      elif main_event == '101':
        if self.task_instances[10][1] is not None:
          self.task_instances[10][1].open()
      elif main_event == '102':
        if self.task_instances[10][2] is not None:
          self.task_instances[10][2].open()
      elif main_event == '103':
        if self.task_instances[10][3] is not None:
          self.task_instances[10][3].open()
      elif main_event == '104':
        if self.task_instances[10][4] is not None:
          self.task_instances[10][4].open()

      elif main_event == '110':
        if self.task_instances[11][0] is not None:
          self.task_instances[11][0].open()
      elif main_event == '111':
        if self.task_instances[11][1] is not None:
          self.task_instances[11][1].open()
      elif main_event == '112':
        if self.task_instances[11][2] is not None:
          self.task_instances[11][2].open()
      elif main_event == '113':
        if self.task_instances[11][3] is not None:
          self.task_instances[11][3].open()
      elif main_event == '114':
        if self.task_instances[11][4] is not None:
          self.task_instances[11][4].open()

      elif main_event == 'update_timetable':
        task_reload()
        self.update_timetable(main_window)

      elif main_event == 'timeout':
        schedule.run_pending()




    main_window.close()
    return 0


