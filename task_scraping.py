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
import datetime

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
                onclick_js.append(onclick[i].get('onclick')[16:21])
            #print(onclick_js)
            date = datetime.date.today()
            date = str(date).replace('-','')
            #print(date)

            for low in onclick_js:
                urllib = 'https://scomb.shibaura-it.ac.jp/ScombPortlet/fancybox/lbLmsInit?primaryKey='+ low +'&selDate='+ date +'&request_locale=ja&format=1'
                driver.get(urllib)
                #wait.until(EC.presence_of_all_elements_located)
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
                tasks.append([title,detail,teacher,deadline,complete])
            return msg,tasks
        
        else:
            print('開けていません')
            msg = 'ログインに失敗しました'
            tasks = None
            return msg,tasks
        
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

    c.execute('drop table tasks')
    c.execute('create table tasks(name text,class text,teacher text,deadline text,complete text)')

    tasks = tuple(tasks)

    print(tasks)
    
    c.execute('delete from tasks')
    for task in tasks:
        print(task)
        c.execute('insert into tasks (name,class,teacher,deadline,complete) values(?,?,?,?,?)',[task[0],task[1],task[2],task[3],task[4]])
    conn.commit()
    conn.close()
        
