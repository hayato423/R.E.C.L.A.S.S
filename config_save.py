import sqlite3
class config_save:
    conn=sqlite3.connect('config.db')
    c=conn.cursor()


    c.execute('''CREATE TABLE scomb(ID,password)''')

    scombID=str(input("IDを入力して下さい"))
    scomb_pass=str(input("passwordを入力して下さい"))

    c.execute("INSERT INTO scomb VALUES(scombID,scomb_pass)")

    conn.commit()
    conn.close()


