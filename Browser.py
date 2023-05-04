from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, timedelta
import time
from pynput.keyboard import Key, Controller
import pandas as pd

keyboard = Controller()

from pynput.mouse import Controller as MouseController
mouse = MouseController()
class Browser:
    def __init__(self):
        self.browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.a = ActionChains(self.browser)

    def goToFirst(self):
        for _ in range(150):
            for _ in range(20):
                mouse.scroll(-500,0)
                time.sleep(0.1)
            time.sleep(1)
            try:        
                values_elements = self.browser.find_elements(By.XPATH, "//*[@class='chart-data-window-item-value']")
                values = [value.get_attribute('innerText').replace('−','-') for value in values_elements if value.get_attribute('innerText') != '']
                print(values)
                if values[0] == '∅':
                    break
            except:
                pass
            
    def clickDataBtn(self):
        data_btn = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//button[@data-name="data-window"]'))
        )
        # data_btn = self.browser.find_element(By.XPATH, '//button[@data-name="data-window"]')
        data_btn.click()
        canvas = self.browser.find_element(By.XPATH,'//canvas')
        self.a.move_to_element(canvas).perform()
        mouse.position = (canvas.location['x'] + canvas.size['width']//2,canvas.location['y']+canvas.size['height']//1.5)
        print(canvas.location['x'],canvas.location['y'])
        time.sleep(1)
        self.goToFirst()
    
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
                values = [value.get_attribute('innerText').replace('−','-') for value in values_elements if value.get_attribute('innerText') != '']
                if values[0] == '∅':
                    return [], None
                # values[0] convert into date from string
                date_data = datetime.strptime(values[0], "%a %d %b '%y")
                values[0] = date_data.strftime('%Y-%m-%d')
                if len(self.scrapped_date)>0 and values[0] == self.scrapped_date[-1]:
                    time.sleep(.1)
                    day_before_7 = datetime.now() - timedelta(days=7)
                    if date_data > day_before_7:
                        self.is_runnig = False
                        return [], None
                    return self.getSingleValue()
                break
            except Exception as e:
                error_count += 1
                # print(e)
                time.sleep(1)
                if error_count > 10:
                    with open("error.html", 'a',encoding='utf-8') as f:
                        f.write(self.browser.page_source)
                    self.is_runnig = False
        return values, date_data
        
    def getAlldata(self,name):
        self.is_runnig = True
        self.scrapped_date = []
        with open(f'data/{name}_data.csv', 'w',encoding='utf-8') as f:
            f.write('Date,Open,High,Low,Close\n')
            while self.is_runnig:
                self.dismissPopUp()
                values, date_data = self.getSingleValue()
                if date_data is None:
                    keyboard.press(Key.right)
                    keyboard.release(Key.right)
                    time.sleep(0.2)
                    continue
                if date_data >= datetime.now():
                    break
                if values[0] not in self.scrapped_date and date_data < datetime.now():
                    f.write(','.join(values[:-1]) + '\n')
                self.scrapped_date.append(values[0])
                keyboard.press(Key.right)
                keyboard.release(Key.right)
                time.sleep(0.2)

    def sortData(self,name):
        df = pd.read_csv(f'data/{name}_data.csv')
        df = df.sort_values(by=['Date'])
        df.to_csv(f'data/{name}_data.csv',index=False)
    
    def getAlldataFromUrl(self,url):
        print(url)
        self.browser.get(url)
        time.sleep(2)
        self.clickDataBtn()
        name = self.browser.title.split()[0].replace('/','_div_')
        self.getAlldata(name)
        self.sortData(name)
    def quit(self):
        self.browser.quit()


