# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 16:39:03 2019

@author: admin
"""

from bs4 import BeautifulSoup
#import requests   
from selenium import webdriver
import pandas as pd  
from datetime import datetime 
import time
import numpy as np
import re
import sys


def open_url(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5) 
    return driver  

#country_ = range(1,187)
#year_ = range(1999,2005)


country_ = [1,187]
year_ = range(1970,2005)


c_y = []
for y in year_:
    for c in country_:
        reg = [c,y]
        c_y.append(reg)
del c,y,reg

url ='https://www.transfermarkt.com'
driver = open_url(url)

market = []
for data in c_y:
    year = (data[1])
    country = (data[0])
    # year,country = 1987,185
    try:
        url ='https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop?land_id=' + str(country) + '&ausrichtung=alle&spielerposition_id=alle&altersklasse=alle&jahrgang=' + str(year) + '&plus=1'
        driver.get(url) 
        time.sleep(1)
    except:
        continue
    
    for i in [3,4,5,6,7,8,9,9,9,9,9,9,9,9,9,9,10,11,12,13]:
        # i=0
        path = '//*[@id="yw2"]/li['+str(i)+']/a'
        #       //*[@id="yw2"]/li[          ]/a
        try:
            driver.find_element_by_xpath(path).click()
            time.sleep(1)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            soupX = soup.find('table', attrs={'class': 'items'}).find('tbody')
            
        except:
            continue
          
        try:
            players = []    
            for row in soupX.find_all('tr'):
                #row = soupX.find('tr')
                player = []
                for cell in row.find_all('td'):
                    # cell = row.find('td')
                    try:
                        value1 = cell.text.strip()
                        #print(value1)
                        player.append(value1)
                    except:
                        print('No text here')
                        
                    try:
                        for multip in cell.find_all('img'):
                            #multip = cell.find('img')
                            value2 = multip['alt']
                            #print(value2)
                            player.append(value2)        
                    except:
                        print('No img here')
                #players = players + player    
                players.append(player)        
        except:
            continue
    try:
        market = market + players
    except:
        continue

        
        
        
        
        
        
player_list = [] 
for element in market:
    if type(element) == list and len(element) == 22:
        player_list.append(element)



df = pd.DataFrame(player_list)
df1 = df.drop_duplicates([1,9,11])
df1 = df1.drop([1,3,4,5,8,10,],axis=1)

df1.loc[:,12] = df1.loc[:,12].replace(' thousand €',',000',regex=True).replace(' mil. €','0,000',regex=True).replace(',','',regex=True)

cond = df1.loc[:,7].apply(lambda x: '†' not in x)
df1 = df1.loc[cond,:]
del cond

ints = [0,7,12,13,14,15,16,17,18,19,20,21]
for col in ints:
    df1.loc[:,col] = df1.loc[:,col].apply(int)


df1.columns = ['C_Index',"Name", "Position", "Age", "Citizenship",'Club','MkValue',
               'Matches','Goals','OwnGoals','Assist','YCard','2YCard','RCard','SubtOn','SubtOff']




for X in range(16,40):
    ages = df1.loc[ df1.loc[:,'Age']==X   ,'Age'].count() 
    print(X,':',ages)    
    
#df1.to_csv('Top_players.csv' ,index=False) 



