import PySimpleGUI as sg
from scomb_info_save import save
from login_check import login
import getpass

class Scomb:

  def open(self):
   #画面の作成(入力フォームなど)
   layout = [
    [sg.Text('ScombID パスワード登録',font=('IPAゴシック',16),
    text_color = '#696969',relief = sg.RELIEF_RAISED,background_color = '#afeeee')],
    [sg.Text('ID              '),sg.InputText(key = 'scomb_ID')],
    [sg.Text('パスワード'),sg.InputText(key = 'scomb_pass')],
    [sg.Button('OK')],
    [sg.Button('キャンセル')]
   ]
   window = sg.Window('Scomb登録',layout=layout,size=(300,200))
   
   #画面表示と入力されたIDとPasswordを正誤判定
   #ID Password間違い時になぜか例外処理で通ってしまう
   while True:
      event , values = window.read()

      if event == 'OK':
        if len(values['scomb_ID']) > 11:
          show_message = "IDは11文字以下にしてください。"
          sg.popup(show_message)
        elif len(values['scomb_pass']) > 30:
          show_message = "パスワードは30文字以下にしてください。"
          sg.popup(show_message)
        else :
          judge_login = login(values['scomb_ID'],values['scomb_pass'])
          if judge_login == 1:
           save(values['scomb_ID'],values['scomb_pass'])
           show_message = "登録完了しました。"
           sg.popup(show_message)
          elif judge_login == 2:
           show_message = "IDもしくはパスワードが間違っています"
           sg.popup(show_message) 
          elif judge_login == 3:
           show_message = "タイムアウトによりログインを失敗しました"
           sg.popup(show_message)
          elif judge_login == 4:
           show_message = "例外が発生し、ログインできませんでした"
           sg.popup(show_message) 
      if event == 'キャンセル':
        window.close()
      if event is None:
        break
      window.close()