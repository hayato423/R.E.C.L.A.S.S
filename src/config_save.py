"""
desiner:尾崎夢斗
date:6/29
purpose:iniファイルへ設定情報を書き込み
"""

import configparser


def timesave(ALERT_TASK, CONECT_ZOOM, UPDATE):
    '''引数の値をconfig.iniに保存する.
    Args:
        ALERT_TASK(str): 課題通知時間
        CNECT_ZOOM(str): zoom接続時間
        UPDATE(str): 課題更新間隔
    Returns: なし
    '''
    config = configparser.ConfigParser()
    section1 = 'Config'
    config.add_section(section1)
    config.set(section1, 'alert_task', ALERT_TASK)
    config.set(section1, 'connect_zoom', CONECT_ZOOM)
    config.set(section1, 'update', UPDATE)

# iniファイルへの書き込み
    with open('./config.ini', 'w') as file:
        config.write(file)
