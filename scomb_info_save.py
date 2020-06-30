"""
designer : 坂下直樹
date : 編集日(2020.06.D23)
purpose : 入力フォームにて入力されたものをconfig.iniに保存する
"""

import configparser 

#iniファイルへの書き込む情報
def save(ID,PASSWORD):
 config = configparser.ConfigParser()
 section1 = 'Scomb'
 config.add_section(section1)
 config.set(section1, 'ID', ID)    #なぜかiniファイルには'Id'の'I'が小文字で入力されている
 config.set(section1, 'PASSWORD', PASSWORD)

#iniファイルへの書き込み
 with open('scomb.ini','w') as file:
     config.write(file)