"""
designer :小澤 孟(Ozawa Hajime)
date : 編集日(2020.7.6)
purpose : 課題更新要請処理
"""

import configparser
from task_sc import task_sc
from task_sc import task_write
import PySimpleGUI as sg
#from time import sleep

def task_reload():

    """
    課題の更新を要請する.
    Args:
    Return:
    """

    config_ini = configparser.ConfigParser()
    config_ini.read('./scomb.ini',encoding = 'utf-8')
    ID = config_ini['Scomb']['id']
    PASSWORD = config_ini['Scomb']['password']
    task = []
    msg = ''

    msg,task = task_sc(ID,PASSWORD)
    while task == []:
        msg,task = task_sc(ID,PASSWORD)
        if task != ['error'] and msg == 'ログインに失敗しました':
            break

    print(task)
    print(msg)
    if msg == 'ログインに成功しました':
        task_write(task)
        sg.Popup('課題の取得に成功しました')
        return 0, msg

    else:
        sg.Popup('課題の取得に失敗しました.')
        return -1, msg



#task_reload()