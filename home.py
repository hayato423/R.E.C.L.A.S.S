import PySimpleGUI as sg
import config
import lecture

#時間割リスト [時間][曜日]
time_table = [[None]*4 for i in range(5)]
#lectureインスタンスを格納するリスト
lecture_instances = [[None]*4 for i in range(5)]

#各授業の辞書型データ
lectures_data = [
  {'lecture_name':'社会心理学','teacher_name':'岡田佳子','day':1,'time':2},
  {'lecture_name':'ソフトウェア工学','teacher_name':'中島　毅','day':2,'time':2},
  {'lecture_name':'高度情報演習1B','teacher_name':'中島　毅','day':2,'time':3},
  {'lecture_name':'高度情報演習1B','teacher_name':'中島　毅','day':2,'time':4},
  {'lecture_name':'データベース','teacher_name':'	木村　昌臣','day':3,'time':1},
  {'lecture_name':'高度情報演習１A','teacher_name':'杉本','day':3,'time':3},
  {'lecture_name':'高度情報演習１A','teacher_name':'杉本','day':3,'time':4},
  {'lecture_name':'上級プログラミング','teacher_name':'杉本','day':4,'time':1},
  {'lecture_name':'上級プログラミング','teacher_name':'杉本','day':4,'time':2},
  {'lecture_name':'デジタルメディア処理２','teacher_name':'井尻敬','day':4,'time':3},
  {'lecture_name':'情報通信技術英語','teacher_name':'山崎','day':5,'time':1},
  {'lecture_name':'組込みシステム','teacher_name':'菅谷','day':5,'time':2},
]

#授業のデータを時間割リストに格納
for l in lectures_data:
  time_table[l['day']-1][l['time']-1] = l

#画面レイアウト
main_layout = [
  [sg.Text('Main Window'),sg.Button('設定',key='config_btn')],
  [sg.Text('月　火　水　木　金')],
  [sg.Text('1')],
  [sg.Text('2')],
  [sg.Text('3')],
  [sg.Text('4')]
]




#時間割に基づいてレイアウトを追加
for time in range(4):
  line = []
  for day in range(5):
    if time_table[day][time] is None:
      main_layout[time+2].append(sg.Button('',key=str(day)+str(time),size=(13,3)))
    else:
      lec = time_table[day][time]
      main_layout[time+2].append(sg.Button(lec['lecture_name'],key=str(day)+str(time),size=(13,3)))
      instance = lecture.Lecture(lec['lecture_name'],lec['teacher_name'])
      lecture_instances[day][time] = instance



#ウィンドウ生成
main_window = sg.Window('Main',layout=main_layout)
config_window = config.Config()


while True:
  main_event , main_value = main_window.read()

  if main_event is None:
    break

  elif main_event == 'config_btn':
    config_window.open()

  elif main_event == '00':
    if lecture_instances[0][0] is not None:
      lecture_instances[0][0].open()
  elif main_event == '01':
    if lecture_instances[0][1] is not None:
      lecture_instances[0][1].open()
  elif main_event == '02':
    if lecture_instances[0][2] is not None:
      lecture_instances[0][2].open()
  elif main_event == '03':
    if lecture_instances[0][3] is not None:
      lecture_instances[0][3].open()

  elif main_event == '10':
    if lecture_instances[1][0] is not None:
      lecture_instances[1][0].open()
  elif main_event == '11':
    if lecture_instances[1][1] is not None:
      lecture_instances[1][1].open()
  elif main_event == '12':
    if lecture_instances[1][2] is not None:
      lecture_instances[1][2].open()
  elif main_event == '13':
    if lecture_instances[1][3] is not None:
      lecture_instances[1][3].open()

  elif main_event == '20':
    if lecture_instances[2][0] is not None:
      lecture_instances[2][0].open()
  elif main_event == '21':
    if lecture_instances[2][1] is not None:
      lecture_instances[2][1].open()
  elif main_event == '22':
    if lecture_instances[2][2] is not None:
      lecture_instances[2][2].open()
  elif main_event == '23':
    if lecture_instances[2][3] is not None:
      lecture_instances[2][3].open()

  elif main_event == '30':
    if lecture_instances[3][0] is not None:
      lecture_instances[3][0].open()
  elif main_event == '31':
    if lecture_instances[3][1] is not None:
      lecture_instances[3][1].open()
  elif main_event == '32':
    if lecture_instances[3][2] is not None:
      lecture_instances[3][2].open()
  elif main_event == '33':
    if lecture_instances[3][3] is not None:
      lecture_instances[3][3].open()

  elif main_event == '40':
    if lecture_instances[4][0] is not None:
      lecture_instances[4][0].open()
  elif main_event == '41':
    if lecture_instances[4][1] is not None:
      lecture_instances[4][1].open()
  elif main_event == '42':
    if lecture_instances[4][2] is not None:
      lecture_instances[4][2].open()
  elif main_event == '43':
    if lecture_instances[4][3] is not None:
      lecture_instances[4][3].open()

main_window.close()





