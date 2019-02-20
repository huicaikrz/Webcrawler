# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 20:36:32 2019

Use it to collect well data from the website

@author: Hui Cai
"""

import requests
import json
import pickle

#read settings from local file
with open('./settings/webSettings.txt','r') as f:
    settings = eval(f.read())
cookies = settings['cookies']
headers = settings['headers']
token = settings['token']
totalResult = settings['totalResult']

#postData is a dictionary for the parameters of requests.post
with open('./settings/post_data.txt','rb') as f:
    postData = pickle.load(f)

wellData = []

#the length of data request each time, could not be too large
step = 1000

#start determines the start position of extraction
for start in range(0,totalResult,step):
    print(start)
    
    #input the parameters
    postData['__RequestVerificationToken'] = token
    postData['iDisplayLength'] = 1000
    postData['iDisplayStart'] = start
    
    #request the json file
    website = requests.post('https://secure.conservation.ca.gov/WellSearch/Search/AjaxHandler',
                            headers = headers,cookies = cookies,data = postData)
    websiteJson = website.text
    
    #use json package to deal with the text
    websiteContent = json.loads(websiteJson)
    
    #store the data into the whole dataset
    wellData.extend(websiteContent['aaData'])

#store in the local directory
with open("./wellData/WellData.json","w") as f:
    json.dump(wellData,f)
