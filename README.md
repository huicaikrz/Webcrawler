# Project Title

Puget Financial Technical Challenge

## Prerequisites

What things you need to install the software and how to install them

Software required:
* [chromedriver](https://seleniumhq.github.io/selenium/docs/api/java/org/openqa/selenium/chrome/ChromeDriver.html)
Note to put chromedriver at the same directory as the webcrawlerSetting.py file.

Python Packages Reuqired:
* selenium
* requests
* re
* json
* pickle
* tqdm
* multiprocessing
* pandas

## Structure of the Folders, Files and Description
```
PugetFinancialTecChallange
│   README.md
│   chromedriver.exe
│   webcrawlerSetting.py
│   pugetWellData.py
│   pugetProductionData.py
│       
│
└───settings
│       post_data.txt
│       webSettings.txt
│   
└───wellData
│       wellData.json
│
│
└───wellProductionData
│       ProductionData1.json
│       ProductionData2.json
│       ...
|       ProductionData49.json

```

## Description of .py Files
webcrawlerSetting.py: The first file that should be ran. It will open the chrome and get the required settings (headers, cookies, token), then store those settings into the "settings" folder.

pugetWellData.py: Used to get the well data from the website. Save the json file into the wellData folders. It will generate two json files, the first is called "wellData.json", and the second is called "wellDataRequired.json". wellData.json is a little bit redundanct, and wellDataRequired.json is the final structured well data. It will take a while to run this file, not too long.

pugetProductionData.py: Used to get the production data of each well. It will provide 49 json files in "wellProductionData" folder. This .py file will require a long time to run.

## Structure of the Json Data
wellData.json: \[{well1 information},{well2 information},...\]
Some information that I get is quite strange. For example, there's a key named 'IsCurrentActive' and for all well, the value is False. I guess that since these data are not shown to browser viewers, they do not have the right value onto them in source code. But I have checked other data which could be directly seen on through browsers, and they are consistent with wellData.json.

ProductionData1.json {'APINumber1': \[{total production of this well in year1}, {production data of this well on year1 day1}, {production data of this well on year1 day2}, ...\], 'APINumber2': ...}
Note that for the other ProductionData.json file, they are of the similar stucture. API Number is unique for every well, so I decided to use is as the key. Also, note that for the time series data, I also included yearly sum, in the list. For 2 or 3 wells, I met with the problem of error 414 to get the production data.

## Challenges and Solutions
```
Challenge 1. Using selenium.webdriver to get data is too slow.

Solution: Instead, I decided to use requests to get the content of the website
```
```
Challenge 2. When I wanted to use requests.post to get the well data, cookies and token were required.

Solution: I directly use selenium.webdriver to simulate the operation of Chrome, like clicking and I managed to get the cookies, token and some other basic information that could help in my future development.
```
```
Challenge 3. There are more than 240000 wells, which means that there are more than 240000 tables of production data (although most of them are empty). On the one hand, it will take a lot of time to get them from the website,and on the other hand, my computer's RAM is not big enough to store all of them and then save them to my discs.

Solution: Using multiprocessing to increase the speed. And divided dataset into several parts, get them, store them and then delete them from memory.
```

Actually, there are many other minor challenges. For example, I could not run a .py file with multiprocessing in IPython console. And I managed to overcome most of them. I am happy with that!

## Future Development
1. I could write them as objects but not functions. So that others could input some parameters and use it to get data without the necessary to read the .py files.

2. I think maybe there are some other methods to get cookies and token without using selenium.webdriver.
