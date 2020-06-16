import PySimpleGUI as sg

class Lecture:

  def __init__(self,lecture_name,teacher_name):
    self.lecture_name = lecture_name
    self.teacher_name = teacher_name

  def open(self):
    layout = [
      [sg.Text(self.lecture_name)],
      [sg.Text(self.teacher_name)]
    ]
    window = sg.Window(self.lecture_name,layout=layout,size=(200,200))
    while True:
      event ,value = window.read()
      if event is None:
        break
    window.close()