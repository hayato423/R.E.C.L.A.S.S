'''
disingner : 寺尾颯人
date      : 2020.06.23
purpose   : sqliteのファクトリ定義
'''
import sqlite3

def dict_factory(cursor,row):
  '''データベースの返り値をタプル型から辞書型に変換
  Args:
  Retrun:
  '''
  d = {}
  for idx, col in enumerate(cursor.description):
    d[col[0]] = row[idx]
  return d