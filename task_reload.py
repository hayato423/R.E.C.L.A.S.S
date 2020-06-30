import configparser
import task_scraping

def task_reload():
    
    config_ini = configparser.ConfigParser()
    config_ini.read('config.ini',encoding = 'utf-8')
    ID = config_ini['Scomb']['id']
    PASSWORD = config_ini['Scomb']['password']
    task = []
    msg = ''
    msg,task = task_scraping.task_scraping(ID,PASSWORD)
    print(task)
    print(msg)
    if msg != 'ログインに失敗しました':
        task_scraping.task_write(task)

task_reload()
