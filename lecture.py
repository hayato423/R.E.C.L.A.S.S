"""
designer:中村友哉
date:2020.07.02
purpose:授業詳細画面表示
"""

import PySimpleGUI as sg

class Lecture:

  def __init__(self,lecture_name,teacher_name):
    self.lecture_name = lecture_name
    self.teacher_name = teacher_name

  def open(self):
    layout = [
      [sg.Text(self.lecture_name)],
      [sg.Text('担当講師'),sg.Text(self.teacher_name)],
      [sg.Text('zoomURL'),sg.InputText(key = 'zoom_url')],
      #[sg.Text('休講'),sg.Text(self.no_class_days)],
      [sg.Button('OK')],
      [sg.Button('キャンセル')]
    ]
    window = sg.Window(self.lecture_name,layout=layout,size=(200,200))

    while True:
      event ,value = window.read()

      if event == 'OK':
        if len(value['zoom_url']) > 80:
          show_message = 'zoomURLは80字以下にしてください'
          sg.popup(show_message)

      if event == 'キャンセル':
        window.close()

      if event is None:
        break
    window.close()