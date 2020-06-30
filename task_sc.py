from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import chromedriver_binary

options = Options()

def task_sc(ID,PASSWORD):
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
        wait.until(EC.presence_of_all_elements_located);
        next_button = driver.find_element_by_id('continueButton')
        next_button.click()
        home_url = driver.current_url
        print("after_open")
        wait.until(EC.presence_of_all_elements_located)
        print("after_load")
        #cur_url = driver.current_url
        if home_url == 'https://scomb.shibaura-it.ac.jp/portal/contents/home/':
            msg = 'ログインに成功しました'
            print(msg)
            can_login = True
            print(driver.find_element_by_class_name('list').text)
            
            #for i in range(1,len(report)):
                #print(report(i))
        else:
            print('開けていません')
            print(home_url)
    except Exception as e:
        print('例外')
        print(e)
    finally:
        driver.close()


ID = 'al18033'
PASSWORD = '$One038$'
task_sc(ID,PASSWORD)
