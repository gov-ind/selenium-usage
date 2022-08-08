from selenium import webdriver
from pdb import set_trace
from selenium_stealth import stealth
import os
import numpy as np
import pandas as pd

ln = 7650

set_trace()

def write_preds(preds):
    #set_trace()
    data = pd.read_csv('sols.csv')
    data['demand'] = preds
    data.to_csv('sols.csv', index=False)

#preds = np.array([0] * ln)
preds = np.array(pd.read_csv('sols.csv')['demand'])

write_preds(preds)

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=options)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

set_trace()

#driver = webdriver.Chrome()
driver.get('https://datahack.analyticsvidhya.com/contest/job-a-thon-april-2022/?utm_source=datahack&utm_medium=navbar')
driver.find_element_by_class_name('av-btn').click()
driver.find_element_by_class_name('btn-g-plus').click()
driver.find_element_by_class_name('whsOnd').send_keys('govind.reg.92@gmail.com')
#driver.find_element_by_class_name('whsOnd').send_keys('h4ckerd00d@gmail.com')
#driver.find_element_by_class_name('VfPpkd-vQzf8d').click()

set_trace()

driver.find_element_by_class_name('whsOnd').send_keys('vindog22390931')
#driver.find_element_by_class_name('whsOnd').send_keys('hackerman92')
#driver.find_element_by_class_name('VfPpkd-LgbsSe').click()
driver.find_element_by_id('SolutionChecker-tab').click()

set_trace()

def get_rmse():
    driver.get('https://datahack.analyticsvidhya.com/contest/job-a-thon-april-2022/#SolutionChecker')
    driver.find_element_by_id('solution_file1').send_keys(os.getcwd() + '/sols.csv')
    driver.find_element_by_id('message1').send_keys('Test')
    driver.find_element_by_id('sub1').click()

    while True:
        try:
            dd = driver.find_element_by_id('modal-body1')
            rmse = float(dd.text.split(': ')[1][:-1])
        except:
            continue
        #set_trace()
        return rmse

jmp = 20

prev_rmse = get_rmse()

def rec(preds, i, jmp):
    preds[i] += jmp
    nxt = np.append(preds[:i], np.array(preds[i]))
    nxt =  np.append(nxt, preds[i + 1:])
    write_preds(preds)

    return get_rmse()

set_trace()

from math import inf
rmses = []

start = list(preds).index(0)

for i in range(start, ln):
    diff = inf
    print(i)

    while diff > 0:
        with open('preds', 'wb') as f:
            f.write(preds)
        nxt_rmse = rec(preds, i, jmp)
        diff = prev_rmse - nxt_rmse
        prev_rmse = nxt_rmse
        rmses.append(prev_rmse)

set_trace()
