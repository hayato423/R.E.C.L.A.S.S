import home
import sqlite3
if __name__ == "__main__":
  dbname = 'reclass.db'
  #データベース接続
  conn = sqlite3.connect(dbname)
  cur = conn.cursor()
  create_lectures_table = '''CREATE TABLE IF NOT EXISTS lectures(lecture_name TEXT, teacher_name TEXT, day INTEGER, time INTERGER )'''
  cur.execute(create_lectures_table)
  create_tasks_table = '''CREATE TABLE IF NOT EXISTS tasks(lecture_name TEXT, teacher_name TEXT, task_name TEXT, submit_state INTEGER,deadline DATETIME)'''
  cur.execute(create_tasks_table)
  create_zoomURL_table = ''' CREATE TABLE IF NOT EXISTS zoomURL(lecutre_name TEXT, url TEXT)'''
  cur.execute(create_zoomURL_table)
  home_window = home.Home()
  home_window.open()
  conn.close()