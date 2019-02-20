# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 23:39:10 2019

Use webdriver to get cookies and token for requests 

@author: Hui Cai
"""

from selenium import webdriver
import time

#explicitly write headers
headers = {
    'Host':'secure.conservation.ca.gov',
    'Referer': 'https://secure.conservation.ca.gov/WellSearch',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

#open google chrome and input the url
driver = webdriver.Chrome('chromedriver.exe')
driver.get('https://secure.conservation.ca.gov/WellSearch/') 

#click several buttons to do search
driver.find_element_by_id('chkActiveOperators').click()
driver.find_element_by_id('chkActiveWells').click()
btnSearch = driver.find_element_by_id('buttonSearch').click()

#get token and cookies
token = driver.find_element_by_name('__RequestVerificationToken'
                                    ).get_attribute('value')
cookies = {x['name']:x['value'] for x in driver.get_cookies()}
time.sleep(10)

#get the number of results in total and transfrom from str into int
totalResult = int(driver.find_element_by_id('myDataTable_info').text
                  .split()[-2].replace(',',''))
driver.quit()

#we could store cookies, token headers into local files
settings = {'headers':headers, 'cookies':cookies, 
           'token': token,'totalResult':totalResult}
with open('./settings/webSettings.txt','w') as f:
    f.write(str(settings))

    
    
    
    