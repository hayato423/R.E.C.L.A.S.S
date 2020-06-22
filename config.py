import PySimpleGUI as sg


class Config:

  def open(self):
    config_layout = [
      [sg.Text('設定')],[sg.Text('scombID')],[sg.Text('scombパスワード')],[sg.Button('終了')]
    ]
    config_window = sg.Window('設定',layout=config_layout,size=(200,200))
    while True:
      event , value = config_window.read()
      if event in (None,'終了'):
        print('ホーム画面に戻ります')
        break
    config_window.close()