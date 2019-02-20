# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 20:23:43 2019

Use it to collect production data from website

@author: Hui Cai
"""
import pandas as pd
import requests
import json
import re
import tqdm
from multiprocessing import Pool
import datetime
from retrying import retry

#I just do not want to make them as an input of my function
global headers
global cookies

with open('./settings/webSettings.txt','r') as f:
    settings = eval(f.read())

#we could get headers and cookies from local txt files 
cookies = settings['cookies']
headers = settings['headers']

#try 3 times at maximum
@retry(stop_max_attempt_number=3)
def productionDataGet(api):
    '''
    get the time series table of certain well (denoted by API number)
    '''
   
    website = requests.get('https://secure.conservation.ca.gov/WellSearch/Details?api=%s' 
                           %(api),headers = headers,cookies = cookies,timeout = 8)
    #error checking 414
    if website.status_code != 200:
        return (api,[])
    websiteContent = website.text
    
    #match out the whole time series table
    pattern = re.compile(r'drawProdTable\((.*?)\);')
    productionData = re.findall(pattern,websiteContent)[0]
    
    #if I need to convert into python data, I'd better do some changes
    #productionData = productionData.replace('null','nan').replace('true','True').replace('false','False')
    
    #use json to read these data
    productionData = json.loads(productionData)
    
    #if the list is empty, no results for this api, directly return
    if not productionData:
        return (api,productionData)
    
    #transform date from milliseconds into standard date
    for i in range(len(productionData)):
        date = int(productionData[i]['ProductionDate'][6:-2])
        if date > 90000000:
            date = datetime.datetime.fromtimestamp(date/1000.0)
        else:
            date = datetime.datetime.fromtimestamp(90000)
        productionData[i]['ProductionDate'] = str(date.month)+'/'+str(date.day)+'/'+ str(date.year)
    
    #return a tuple with api and data
    return (api,productionData)

if __name__ == '__main__':
    #use the previous dataset to get all the api numbers
    with open("./wellData/WellData.json",'r') as f:
        wellData = json.load(f)
    wellData = pd.DataFrame(wellData)
    allApi = list(wellData['APINumber'])
    #delete the large data to save memory
    del wellData
    
    step = 5000
    import math
    total = math.ceil(len(allApi)/step)
    count = 0
    #because of the limitation of RAM, each time, I extract the 
    #production data of 10000 APIs, use multiprocessing to increase speed
    for j in range(0,len(allApi),step):
        count += 1
        print(count)
        API = allApi[j:j+step]
        #use tqdm to see where the code is 
        with Pool(8) as p:
            allProductionData = list(tqdm.tqdm(p.imap(productionDataGet,API), total=len(API)))
        #use a txt file to see how many loops have we done
        with open("codeSuperviser.txt",'w') as f:
            f.write('managed to finish %s and total is %s' %(count,total))
        
        #save the dataset into local file  
        allProductionData = {x[0]:x[1] for x in allProductionData} 
        with open("./wellProductionData/ProductionData%s.json" %(count),"w") as f:
            json.dump(allProductionData,f)
        del allProductionData
