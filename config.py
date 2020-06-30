import PySimpleGUI as sg
from config_save import timesave

class Config:

  def open(self):
   #画面の作成(入力フォームなど)
   config_layout = [
    [sg.Text('課題通知時間',font=('IPAゴシック',16),
    text_color = '#696969',relief = sg.RELIEF_RAISED,background_color = '#afeeee')],
    [sg.Text('〇日前に通知 '),sg.InputText(key = 'alert_task')],
    [sg.Text('Zoom接続時間'),sg.InputText(key = 'conect_zoom')],
    [sg.Text('更新間隔'),sg.InputText(key = 'update')],
    [sg.Button('保存')],
    [sg.Button('キャンセル')]
   ]
   config_window = sg.Window('設定登録',layout=config_layout,size=(300,200))
   
   #入力された設定を正誤判定
   while True:
      event , values = config_window.read()
      if event == 'OK':
        if len(values['alert_task']) >= 2:
          show_message = "通知時間は一桁にしてください。"
          sg.popup(show_message)
        elif len(values['conect_zoom']) >= 3:
          show_message = "接続時間は二桁にして下さい。"
          sg.popup(show_message)
        elif len(values['update']) >= 3:
          show_message = "更新間隔は二桁にして下さい。"
          sg.popup(show_message)
        else :
          save(values['alert_task'],values['conect_zoom'],values['update'])
          show_message = "登録完了しました。"
          sg.popup(show_message)
      if event == 'キャンセル':
        window.close()
      if event is None:
        break
      config_window.close()