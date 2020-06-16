import PySimpleGUI as sg


class Scomb:

  def open(self):
    layout = [
      [sg.Text('Scomb')]
    ]
    window = sg.Window('Scomb登録',layout=layout,size=(200,200))
    while True:
      event , value = window.read()
      if event is None:
        break
    window.close()