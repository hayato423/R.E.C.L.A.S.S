"""
designer :小澤 孟(Ozawa Hajime)
date : 編集日(2020.7.6)
purpose : 課題通知処理
"""


from datetime import datetime,date,timedelta
from plyer import notification
import sqlite3
import configparser
import schedule
from task_reload import task_reload

def task_alart():

    """
    課題をn日前に通知する.
    Args:

    Return:
    windows通知
    """


    config_ini = configparser.ConfigParser()

    config_ini.read('./config.ini',encoding = 'utf-8')

    alert = config_ini['Config']['alert_task']
    conn = sqlite3.connect('reclass.db')
    c = conn.cursor()

    c.execute('select * from tasks')

    tasks = c.fetchall()

    today = date.today()


    for task in tasks:
        print(task[3])
        deadline = task[3]
        deadline_day = date(int(deadline[0:4]),int(deadline[4:6]),int(deadline[6:8]))
        print(deadline_day)
        if deadline_day - timedelta(days = int(alert)) == today or deadline_day == today:
            notification.notify(
                title = '課題通知',
                message = task[0] + task[3],
                app_name = "RECLASS"
            )

def alart_time():
    """
    課題に関する定時処理を実行する
    Args:
    Return:
    null(関数実行のみ)
    """
    schedule.every().day.at("06:23").do(task_alart)
    schedule.every().day.at("12:00").do(task_alart)
    schedule.every().day.at("08:00").do(task_reload)
