"""
designer :小澤 孟(Ozawa Hajime)
date : 編集日(2020.6.30)
purpose : 課題スクレイピングおよびデータベース書き込み
"""



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import chromedriver_binary
import re
import sqlite3


def task_scraping(ID,PASSWORD):

    """
    scombから課題を取得する.
    Args:
    id(str): 学籍番号
    password(str):scombのパスワード
    Return:
    task:課題一覧
    str:終了メッセージ
    """
    
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    scomb_url = 'https://scomb.shibaura-it.ac.jp/portal/index'
    wait = WebDriverWait(driver,20)
    driver.get(scomb_url)
    
    try:
        login_button = driver.find_element_by_id('loginField')
        login_button.click()
        cur_url = driver.current_url
        trim_url = str(cur_url).replace('https://','')
        basic_auth_url = 'https://' + ID + '%40sic:' + PASSWORD + '@' + trim_url
        driver.get(basic_auth_url)
        wait.until(EC.presence_of_all_elements_located)
        next_button = driver.find_element_by_id('continueButton')
        next_button.click()
        home_url = driver.current_url
        wait.until(EC.presence_of_all_elements_located)
        if home_url == 'https://scomb.shibaura-it.ac.jp/portal/contents/home/':
            msg = 'ログインに成功しました'
            print(msg)
            can_login = True
            source_code = driver.page_source
            soup = BeautifulSoup(source_code,'html.parser')
            onclick_js = []
            tasks = []
            onclick = soup.find(class_='list').find_all('a')
            for i in range(len(onclick)):
                driver.implicitly_wait(5)
                onclick_js.append(onclick[i].get('onclick'))
                tasks.append(onclick[i].text)
                task = [s.replace('\n\t\t\t\t\t\t\t\t\t','') for s in tasks]
            return msg,task
            
            """
            print(task)
            print(onclick_js)
            for i in range(len(onclick_js)):
            driver.execute_script(str(onclick_js[i]))
            wait.until(EC.presence_of_all_elements_located) 
            close = driver.find_element_by_id('fancybox-close')
            close.click()
            """
        
        else:
            print('開けていません')
            msg = 'ログインに失敗しました'
            task = None
            return msg,task
    except Exception as e:
        print('例外')
        print(e)
    finally:
        driver.close()
            
def task_write(tasks):

    """
    課題をデータベースに書き込む
    Args:
    task(list):課題一覧
    Return:
    null(データベース書き込みのみ)
    """
    conn = sqlite3.connect('reclass.db')
    c = conn.cursor()

    c.execute('SELECT COUNT(*) FROM sqlite_master WHERE TYPE="table" AND NAME="tasks"')

    if c.fetchone() == (0,):
        c.execute('create table tasks(name string)')

    tasks = tuple(tasks)

    print(tasks)
    
    c.execute('delete from tasks')
    for task in tasks:
        print(task)
        c.execute('insert into tasks (name) values(?)',(task,))
    conn.commit()
    conn.close()
        
