"""
desiner:尾崎夢斗
date:6/29
purpose:iniファイルへ設定情報を書き込み
"""

import configparser


def timesave(ALERT_TASK, CONECT_ZOOM, UPDATE):
    config = configparser.ConfigParser()
    section1 = 'Config'
    config.add_section(section1)
    config.set(section1, 'alert_task', ALERT_TASK)
    config.set(section1, 'connect_zoom', CONECT_ZOOM)
    config.set(section1, 'update', UPDATE)

# iniファイルへの書き込み
    with open('./config.ini', 'w') as file:
        config.write(file)
