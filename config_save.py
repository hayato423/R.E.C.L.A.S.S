#製作者:尾崎夢斗
#制作日時:6/29
import configparser 

"""config.ini.txtへ設定情報を書き込む"""
def timesave(alert_task,conect_zoom,update):
 config = configparser.ConfigParser()
 section1 = 'Config'
 config.add_section(section1)
 config.set(section1, 'alert_task', alert_task)    
 config.set(section1, 'conect_zoom', conect_zoom)
 config.set(section1, 'update',update)

#iniファイルへの書き込み
 with open('config.ini','w') as file:
     config.write(file)

