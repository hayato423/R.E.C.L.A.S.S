import home
import threading
import datetime
import time
import sys


home_window = home.Home()

def func():
  while True:
    dt_now = datetime.datetime.now()
    print(dt_now)
    time.sleep(1)


if __name__== '__main__':
  thread_1 = threading.Thread(target=home_window.open)
  thread_2 = threading.Thread(target=func)

  thread_1.start()
  thread_2.start()