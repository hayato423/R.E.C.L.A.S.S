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
import re
import sqlite3
from datetime import datetime,date
import os

def task_sc(id,password):

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
    chormepath = os.path.abspath('../driver/chromedriver.exe')
    print(chormepath)
    driver = webdriver.Chrome(executable_path=chormepath,options=options)
    wait = WebDriverWait(driver,20)
    scomb_url = 'https://scomb.shibaura-it.ac.jp/portal/index'
    driver.get(scomb_url)
    wait.until(EC.presence_of_all_elements_located)
    msg = ''
    tasks = []

    try:
        #ログインボタンをクリック
        login_button = driver.find_element_by_id("loginField")
        login_button.click()
        wait.until(EC.presence_of_all_elements_located)

        cur_url = driver.current_url
        trim_url = str(cur_url).replace('https://','')
        #basic認証
        basic_auth_url = 'https://' + id + '%40sic:' + password + '@' + trim_url
        driver.get(basic_auth_url)
        wait.until(EC.presence_of_all_elements_located)

        #次へボタンをクリック
        next_button = driver.find_element_by_id('continueButton')
        next_button.click()
        wait.until(EC.presence_of_all_elements_located)
        driver.implicitly_wait(10)
        home_url = driver.current_url
        
        if home_url == 'https://scomb.shibaura-it.ac.jp/portal/contents/home/':
            msg = 'ログインに成功しました'
            wait.until(EC.presence_of_all_elements_located)
            source_code = driver.page_source
            soup = BeautifulSoup(source_code,'html.parser')
            onclick_js = []
            print(msg)
            func = soup.find_all('dd',class_='list')
            onclick = func[0].select('a[onclick]')
            print(onclick)
            for click in onclick:
                driver.implicitly_wait(5)
                onclick_js.append(click.get('onclick')[16:21])
            date_today = date.today()
            date_today = str(date_today).replace('-','')
            print(date_today)
            
            for low in onclick_js:
                print(low)
                low = low.replace('\'','').replace('\"','').replace(',','').replace('j','')
                urllib = 'https://scomb.shibaura-it.ac.jp/ScombPortlet/fancybox/lbLmsInit?primaryKey='+ str(low) +'&selDate='+ date_today +'&request_locale=ja&format=1'
                driver.get(urllib)
                wait.until(EC.presence_of_all_elements_located)
                source_code = driver.page_source
                soup = BeautifulSoup(source_code,'html.parser')
                temp = soup.find_all('td')
                title = temp[0].text
                detail = temp[1].text
                complete = temp[2].text
                title = title.replace('\n','').replace('\t','').replace('\u3000','')
                detail = detail.replace('\n','').replace('\t','').replace('\u3000','')
                deadline = detail[detail.find('締切日：'):(detail.find('締切日：')+14)]
                detail = detail[0:detail.find('締切日')]
                teacher = detail[detail.find('教員名'):len(detail)]
                detail = detail[0:detail.find('教員名')]
                complete = complete.replace('\n','').replace('\t','').replace('\u3000','')
                detail = detail.replace('コース名：','')
                teacher = teacher.replace('教員名：','')
                deadline = deadline.replace('締切日：','').replace('/','')
                tasks.append([title,detail,teacher,deadline,complete])
        
        else:
            print('開けていません')
            msg = 'ログインに失敗しました'
            tasks = ['error']
        
    except Exception as e:
        print('例外')
        msg = '例外'
        tasks = ['error']
        print(e)
    finally:
        driver.close()
        return msg,tasks
            
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

    c.execute('create table if not exists tasks(task_name text,lecture_name text,teacher_name text,deadline text,complete text)')

    tasks = tuple(tasks)

    print(tasks)
    
    c.execute('delete from tasks')
    for task in tasks:
        print(task)
        c.execute('insert into tasks (task_name,lecture_name,teacher_name,deadline,complete) values(?,?,?,?,?)',[task[0],task[1],task[2],task[3],task[4]])
    conn.commit()
    conn.close()
        
