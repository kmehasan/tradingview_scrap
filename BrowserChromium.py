from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import chromedriver_autoinstaller

from datetime import datetime, timedelta
import time
import pandas as pd
import os
import shutil
day_dict = {
    'Mon':0,
    'Tue':1,
    'Wed':2,
    'Thu':3,
    'Fri':4,
    'Sat':5,
    'Sun':6
}
class Browser:
    def __init__(self,url,from_date=None,to_date=datetime.now()):
        print('\n\n'+url)
        self.last_date = from_date
        if to_date:
            self.first_date = to_date
        else:
            self.first_date = datetime.now()
	    
        
        chromedriver_autoinstaller.install()
        # shutil.rmtree('chrome_user_dir',ignore_errors=True)
        isExist = os.path.exists('chrome_user_dir')
        if not isExist:
            os.makedirs('chrome_user_dir')
            print("Create new session for chromes")
        options = Options()
        # options.headless = True
        options.add_argument('--user-data-dir=chrome_user_dir')
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument("--disable-dev-shm-usage")
        
        self.browser = webdriver.Chrome(options=options)
        self.browser.set_window_size(2660,1440)
        self.a = ActionChains(self.browser)

        try:
            self.login()
        except Exception as e:
            print('Already login')

    def login(self):
        self.browser.get('https://www.tradingview.com/')
        
        email = 'tacah78286@jwsuns.com'
        password = 'tacah78286@jwsuns.com'
        time.sleep(1)
        try:
            self.browser.find_element(By.XPATH, '//button[@aria-label="Open user menu"]').click()
            time.sleep(1)
        except:
            pass
        try:
            self.browser.find_element(By.XPATH, '//button[@data-name="header-user-menu-sign-in"]').click()
            time.sleep(1)
        except:
            pass
        try:
            self.browser.find_element(By.NAME, 'Email').click()
            time.sleep(1)
        except:
            pass
        self.browser.find_element(By.ID, 'id_username').send_keys(email)
        self.browser.find_element(By.ID, 'id_password').send_keys(password)
        time.sleep(1)
        self.browser.find_element(By.XPATH, "//form/button").click()
        time.sleep(2)

        

    def goRight(self):
        canvas = self.browser.find_element(By.XPATH,'//canvas')
        self.a.move_to_element(canvas).send_keys(Keys.ARROW_RIGHT).perform()
    def goLeft(self):
        canvas = self.browser.find_element(By.XPATH,'//canvas')
        self.a.move_to_element(canvas).send_keys(Keys.ARROW_LEFT).perform()
    def goToFirst(self):
        canvas = self.browser.find_element(By.XPATH,'//canvas')
        print('Go to first data')
        for _ in range(150):
            print('Move left (ctrl + left arrow)')
            self.a.move_to_element(canvas).perform()
            self.a.key_down(Keys.CONTROL)\
                .key_down(Keys.ARROW_LEFT)\
                .pause(5)\
                .key_up(Keys.ARROW_LEFT)\
                .key_up(Keys.CONTROL)\
                .perform()
            self.a.move_to_element(canvas).send_keys(Keys.ARROW_LEFT).perform()
            time.sleep(1)
            try:        
                values_elements = self.browser.find_elements(By.XPATH, "//*[@class='chart-data-window-item-value']")
                values = [value.get_attribute('innerText').replace('−','-') for value in values_elements if value.get_attribute('innerText') != '']
                print('Current date ==>',values[0])
                if values[0] == '∅':
                    print('Finally reached to first data')
                    break
            except Exception as e:
                # with open("error_data.html", 'a',encoding='utf-8') as f:
                #     f.write(self.browser.page_source)
                # exit()
                pass
    def goToLast(self):
        canvas = self.browser.find_element(By.XPATH,'//canvas')
        print('Go to last data')
        self.a.move_to_element(canvas).perform()
        self.a.key_down(Keys.CONTROL)\
            .pause(0.5)\
            .key_down(Keys.ARROW_RIGHT)\
            .pause(5)\
            .key_up(Keys.ARROW_RIGHT)\
            .pause(0.5)\
            .key_up(Keys.CONTROL)\
            .perform()
        for _ in range(10):
            self.a.key_down(Keys.CONTROL)\
                .pause(0.1)\
                .send_keys(Keys.UP)\
                .pause(0.1)\
                .key_up(Keys.CONTROL)\
                .perform()
        time.sleep(1)

    def clickDataBtn(self):
        print('Open data window')
        data_btn = WebDriverWait(self.browser, 60).until(
            EC.visibility_of_element_located((By.XPATH, '//button[@data-name="data-window"]'))
        )
        # data_btn = self.browser.find_element(By.XPATH, '//button[@data-name="data-window"]')
        data_btn.click()
        canvas = self.browser.find_element(By.XPATH,'//canvas')
        self.a.move_to_element(canvas).perform()
        time.sleep(1)
        # check if data window is opened
        try:
            data_value = WebDriverWait(self.browser, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@class='chart-data-window-item-value']"))
            )
        except:
            self.clickDataBtn()
        self.goToLast()
    
    def dismissPopUp(self):
        try:
            popup = self.browser.find_element(By.XPATH,'//*[@data-dialog-name="gopro"]')
            self.browser.execute_script("arguments[0].style.display = 'none';", popup)
        except:
            pass
    def getSingleValue(self):
        error_count = 0
        while True:
            try:
                values_elements = self.browser.find_elements(By.XPATH, "//*[@class='chart-data-window-item-value']")
                title_elements = self.browser.find_elements(By.XPATH, "//*[@class='chart-data-window-item-title']")
                
                values = [value.get_attribute('innerText').replace('−','-') for value in values_elements if value.get_attribute('innerText') != '']
                value_dict = {}
                for i in range(len(title_elements)):
                    value_dict[title_elements[i].get_attribute('innerText')] = values[i]
                if values[0] == '∅':
                    return [], None
                date_value = value_dict['Date']
                time_format = "%a %d %b '%y" if "Time" not in value_dict else "%a %d %b '%y %H:%M"
                if 'Time' in value_dict:
                    date_value += ' ' + value_dict['Time']
                # values[0] convert into date from string
                date_data = datetime.strptime(date_value, time_format)
                # check century
                while date_data.weekday() != day_dict[values[0][:3]]:
                    date_data = date_data.replace(year=date_data.year - 100)
                values = []
                values.append(date_data.strftime('%Y-%m-%d %H:%M'))
                values.append(value_dict['Open'])
                values.append(value_dict['High'])
                values.append(value_dict['Low'])
                values.append(value_dict['Close'])

                if len(self.scrapped_date)>0 and values[0] == self.scrapped_date[-1]:
                    return [], None
                if date_data < self.last_date:
                    self.is_runnig = False
                break
            except Exception as e:
                error_count += 1
                print(e)
                time.sleep(0.1)
                if error_count > 10:
                    with open("error.html", 'a',encoding='utf-8') as f:
                        f.write(self.browser.page_source)
                    self.is_runnig = False
        return values, date_data
        
    def getAlldata(self,name):
        print('Scraping data ==>')
        self.is_runnig = True
        self.scrapped_date = []
        
        isExistsData = os.path.exists('data')
        if not isExistsData:
            os.makedirs('data')
        
        with open(f'data/{name}_data.csv', 'w',encoding='utf-8') as f:
            f.write('Date,Open,High,Low,Close\n')
            while self.is_runnig:
                self.dismissPopUp()
                values, date_data = self.getSingleValue()
                if date_data is None:
                    self.goLeft()
                    time.sleep(0.1)
                    continue
                
                if values[0] not in self.scrapped_date and date_data < self.first_date:
                    print(values[:5])
                    f.write(','.join(values[:5]) + '\n')
                self.scrapped_date.append(values[0])
                self.goLeft()
                time.sleep(0.1)

    def sortData(self,name):
        df = pd.read_csv(f'data/{name}_data.csv')
        df = df.sort_values(by=['Date'], ascending = False)
        df.to_csv(f'data/{name}_data.csv', index=False)
    
    def getAlldataFromUrl(self,url):
        print(url)
        self.browser.get(url)
        # check if there is launch button
        try:
            launch_btn = WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//button'))
            )
            launch_btn = self.browser.find_elements(By.XPATH, '//button')
            if len(launch_btn) > 1:
                launch_btn = launch_btn[1]
                if 'Launch' in launch_btn.get_attribute('innerText'):
                    launch_btn.click()
                    time.sleep(2)
                    self.browser.switch_to.window(self.browser.window_handles[-1])
        except:
            pass
        
        time.sleep(2)
        self.clickDataBtn()
        name = self.browser.title.split()[0].replace('/','_div_')
        self.getAlldata(name)
        self.sortData(name)
    def quit(self):
        self.browser.quit()


