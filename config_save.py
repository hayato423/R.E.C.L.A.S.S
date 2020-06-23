
import configparser 

#iniファイルへの書き込む情報
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

