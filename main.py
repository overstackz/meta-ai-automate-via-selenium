from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import requests
import os
import sys
import signal
import json
import time

hide_windows = False
chromeVersion = "0"
def getTimestamp(): return round(time.time())

def download_file(url, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"✅ Downloaded: {filename}")
        return True
    except Exception as e:
        return False

def writeJsonToFile(filename:str , obj):
    open(filename , 'w+').write(json.dumps(obj  , ensure_ascii=False))
    return True

def loadJsonFromFile(filename:str):
    getFile = open(filename , 'r')
    getData = getFile.read()
    getFile.close()
    try:
        getJson = json.loads(getData)
        return getJson
    except:
        return False

if not os.path.exists('settings.json'): open('settings.json','w+').write(writeJsonToFile('settings.json',{"username":"" , "password":"" , "headless":False}))
if not os.path.exists('genarate_video'): os.mkdir('genarate_video')

chromePID = 0
myPID = os.getppid()

def delete_files_in_directory(folder_path):
    try:
        file_list = os.listdir(folder_path)
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                delete_files_in_directory(file_path)

        print(f"Delete file all in {folder_path} Done")
        return True
    except Exception as e:
        print(f"Error Delete File : {e}")
    return False

def openDriver():
    global chromePID , hide_windows
        
    chrome_options = Options()  
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging" , "enable-automation"]) 
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--enable-unsafe-swiftshader')
    chrome_options.add_argument('log-level=3')
    if hide_windows : chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
                
    driver.set_window_size(1200, 1000)
    driver.set_page_load_timeout(90)
    chromePID = driver.service.process.pid
    open('cpid.txt' , 'w+').write(str(chromePID))
    writeJsonToFile('timestamp_chrome.json' , {"version": chromeVersion , "timestamp" : getTimestamp()})
    os.system('cls')
    return driver

def close_selenium(signum, frame):
    driver.quit()
    sys.exit(0)

signal.signal(signal.SIGINT, close_selenium)
signal.signal(signal.SIGTERM, close_selenium)

obj_settings = loadJsonFromFile('settings.json')
try:
    if not obj_settings['username'] or not obj_settings['password']: raise('Please , Setting file "settings.json" ')
except:
    pass

def tryClick(driver:webdriver.Chrome , tagName:str , pointer:int):
    limit = 0
    while True:
        if limit >= 30: break
        try:
            if tagName == 'a' and pointer == 0 :
                time.sleep(.25)
                getTagAll = driver.find_elements(By.TAG_NAME , tagName)
                for i in range(0 , len(getTagAll) , 1):
                    getText = getTagAll[i].get_attribute('innerText').lower()
                    if 'log in' in getText: 
                        pointer = i
                        print('MOVE POINTER : ', i)
                        break
                    
            getText = driver.find_elements(By.TAG_NAME , tagName)[pointer].get_attribute('innerText')
            print('Text : ',getText)
            driver.find_elements(By.TAG_NAME , tagName)[pointer].click()
            print(pointer , ' | Click done')
            break
        except Exception as err_click:
            time.sleep(.25)
            limit += 1
    return True

driver = openDriver()
if not driver : raise('Error code [1001] : closed')

def requestClickWithActionChains(driver:webdriver.Chrome , x:int , y:int):
    actions = ActionChains(driver)
    actions.move_by_offset(x, y).click().perform()
    actions.release()
    actions.reset_actions()
    time.sleep(.25)
    return True

def loginMeta(username:str , password:str):
    driver.get("https://auth.meta.com/?source_app_id=391894423991568&redirect_uri=https%3A%2F%2Fauth.meta.com%2Foidc%2F%3Fapp_id%3D391894423991568%26scope%3Dopenid%2Blinking%26response_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Fwww.meta.ai%252Foidc%252Fcallback%252F%26state%3DATkDl34kYSvaXB3bai2vlyLUMkEoE5B5XOsGkVS7giL4UJevh8o2PulJyru7-Md0ObHq4DxF-qT1FpER61M7ynz8_RKMMdSqUQATchX2yBBz6yctiy3NgxS6VzvIPT2O7aW9P_X2uiIbyvNY-hBNaTSteKFtVpu6_Tp3ALbuvhYpE8FOwRwHXRFUlO79kVrYXZeOlJcl4hRBmHoKFbYNpqIPDCUJmYBDwopCv94HkTgj5oVaJAaGO5PWfNcX_QSYSgb5gCmIjpz0rm-kZm7xayRNOiOgmQcHjJGNeW7q7UPCCsr9BUVUVEna9hw&csi=8065b232-9ba5-4f18-9e18-4983342f0cdf&rcs=ATmbT0ulOXlCPT7SYaqfUd2yYOlu4vb95wqWEtWCTHreh22vgbG9TPYx6PH-rOctDLAt1yzTgXzuLO7urK9qH9g9SUhSTeZTDVytX7pw2iiu1xkXlZ257GJXaIj5vaFu-uZDKV2hOmpkPpFwPpvQUGy5vHClGro8YpaAJg")
    driver.find_elements(By.TAG_NAME,'div')[47].click()
    driver.find_element(By.ID , "_r_8_").send_keys(username)
    time.sleep(1)
    tryClick(driver , 'div' , 36)
    time.sleep(1)

    tryClick(driver , 'div' , 56)
    time.sleep(1)
    driver.find_element(By.TAG_NAME , "input").send_keys(password)
    time.sleep(1)

    tryClick(driver , 'div' , 41)
    time.sleep(5)
    limit_login = 0
    while True:
        if limit_login >= 30: break
        getTagDIV = driver.find_elements(By.TAG_NAME , 'div')
        print(len(getTagDIV))
        if len(getTagDIV) < 120 :
            limit_login += 1
            time.sleep(1)
        else: 
            break
    if len(getTagDIV) < 120 :
        print('Error login : ')
        sys.exit(0)
    else:
        tryClick(driver , 'div' , 134)
        time.sleep(5)
        
    if "www.meta.ai" in driver.current_url : 
        print('First Step Login : ✅ PASSED')
        driver.get("https://www.meta.ai/?nr=1")
        time.sleep(.25)

        tryClick(driver , 'a' , 0)
        time.sleep(3)
        print('FINAL Step Login : ✅ PASSED')
        return True
    print('Login : ⚠️ FAIL')
    return False

hide_windows = obj_settings['headless']
send_login = loginMeta(obj_settings['username'] , obj_settings['password'])
requestClickWithActionChains(driver , 550 , 315)
time.sleep(1.5)

input_box = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")

input_box.send_keys('pig flying with children to the moon')
time.sleep(.5)
requestClickWithActionChains(driver , 450, 390)
time.sleep(.5)

requestClickWithActionChains(driver , 555, 390)
time.sleep(.5)

requestClickWithActionChains(driver , 600, 500)
time.sleep(.5)
input_box.send_keys(Keys.ENTER)

print()
print('>> Animate Image')
time.sleep(10)
getImages = driver.find_elements(By.CSS_SELECTOR , "img[draggable]")
print('Img size : ',len(getImages))
for m in range(0 , 4 , 1):
    getImgSrc = getImages[m].get_attribute('src')
    print(f'Image {m} : ',getImgSrc)
    send_download_image = download_file(getImgSrc , f'genarate_video/image_{m}.png')

requestClickWithActionChains(driver , 685, 870)
print()
print('>> Animate Video')
time.sleep(15)
getVideo = driver.find_elements(By.CSS_SELECTOR , "source")
print('Video size : ',len(getVideo))
for v in range(0 , 4 , 1):
    getVideoSrc = getVideo[v].get_attribute('src')
    print(f'Image {v} : ',getVideoSrc)
    send_download_video = download_file(getVideoSrc , f'genarate_video/video_{v}.mp4')



  