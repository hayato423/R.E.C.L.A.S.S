import PySimpleGUI as sg


class Config:

  def open(self):
    config_layout = [
      [sg.Text('設定')]
    ]
    config_window = sg.Window('設定',layout=config_layout,size=(200,200))
    while True:
      event , value = config_window.read()
      if event is None:
        break
    config_window.close()