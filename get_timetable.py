from scomb_login import login_confirm
import configparser

#config.iniの読み込み
config_ini = configparser.ConfigParser()
config_ini.read('config.ini',encoding='utf-8')

ID = config_ini['Scomb']['ID']
PASSWORD = config_ini['Scomb']['Password']

can_login , msg = login_confirm(ID,PASSWORD)
print(msg)


