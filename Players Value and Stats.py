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

##################################################################################################
##################################################################################################
# GET TEAM IDS

##################################################################################################
# TOURNAMENT
Base_url = 'https://www.transfermarkt.com/major-league-soccer/startseite/wettbewerb/'
League = 'MLS1'

url =  Base_url + League
driver = open_url(url)
soup = BeautifulSoup(driver.page_source, 'html.parser')

soup1 = soup.find('table', attrs={'class': 'items'}).tbody.find_all('tr')


team_ids = []
for soup2 in soup1:
    team_id = soup2.contents[3].a['id']
    team_ids.append(team_id)

driver.close()

del team_id, url, Base_url, soup1

##################################################################################################
# TEAMS
 
url = 'https://www.transfermarkt.com/'
driver = open_url(url)
time.sleep(2)

player_ids = []   
for integer_id in team_ids: 
    
    team_id = str(integer_id)        
    url = 'https://www.transfermarkt.com/atlanta-united-fc/kader/verein/'+team_id+'/saison_id/2018/plus/1'
    driver.get(url) 
    time.sleep(1)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    
    soup1 = soup.find('table', attrs={'class': 'items'}).tbody.find_all('tr')
    
    
    for soup2 in soup1:
        try:
            player_id = soup2.contents[2].div.span.a['href']
            #print(player_id)
            player_ids.append(player_id)
        except:
            continue
    
driver.close()

del integer_id, player_id, soup1, team_id, url
##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################
# PLAYERS

# players_list = player_ids


url = 'https://www.transfermarkt.com/'
driver = open_url(url)
time.sleep(2)

tournament_players = []


#player_ids = player_ids[221:]
for player in player_ids:
    #player = player_ids[0]
    player_data = {}


    player_data['player_id'] = player.split('/')[-1]
    player_data['player_name'] = player.split('/')[1].replace('-',' ').title()
    player_data['url'] = player
    
    url = 'https://www.transfermarkt.com'+player
    driver.get(url) 

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    try:
        number = soup.find('div',attrs={'class':'dataName'}).span.text.strip()
    except:
        number= 'N/D'
        
    short_name = soup.find('div',attrs={'class':'dataName'}).h1.b.text.strip()
    player_data['known_as'] = short_name
    player_data['number'] = number

    soup1 = soup.find('table', attrs={'class': 'auflistung'}).tbody

    
    for X in range(0,30,2):
        try:
            name = soup1.contents[X].th.text.strip() 
            content = soup1.contents[X].td.text.strip() 
            player_data[name] = content
        except:
            player_data[name] = np.nan


    ###############################################################################
    
    try:  
        soup1 = soup.find('div', attrs={'class': 'box transferhistorie'}).table.tbody

        
        transf_history = []
    
        for X in range(0,100):
            transfer_data =  {}
            try:
                transfer_data['Season'] = soup1.contents[X].contents[1].text.strip() 
                transfer_data['Date'] = soup1.contents[X].contents[3].text.strip() 
                
                transfer_data['Left'] = soup1.contents[X].contents[5].a.img['alt']
                transfer_data['Joined'] = soup1.contents[X].contents[13].a.img['alt']
                
                transfer_data['MV'] = soup1.contents[X].contents[21].text.strip()
                transfer_data['Fee'] = soup1.contents[X].contents[23].text.strip()
            except:
                transfer_data['Season'] = np.nan
                
            transf_history.append(transfer_data)
    
        player_data['transf_history'] = transf_history
        
    except:
        player_data['transf_history'] = np.nan
    #############################
        
    soup1 = soup.find('div', attrs={'class': 'weitere-daten-spielerprofil'}) 
    try:
        pos1 = soup1.contents[3].div.contents[1].div.div.text.strip()
    except:
        try:
            soupX = soup.find_all('div', attrs={'class': 'weitere-daten-spielerprofil'})
            count = 0
            for i in soupX:
                soup1 = i
                count += 1
                if count == 2:
                    break
            pos1 = soup1.contents[3].div.contents[1].div.div.text.strip()
        except:
            pos1 = 'N/D'
        
    try:
        pos2 = soup1.contents[3].div.contents[1].div.contents[3].text.strip()
    except:
        pos2 = 'N/D'
        
    try:    
        Curr_MV = soup1.contents[7].find('div',attrs={'class':'zeile-oben'}).text.strip()
        Last_update = soup1.contents[7].find('div',attrs={'class':'zeile-mitte'}).text.strip()
        Max_MV = soup1.contents[7].find('div',attrs={'class':'zeile-unten'}).text.strip()

        def clean_and_split(text,i):
            while '\n' in text:
                text = text.replace('\n','')
            
            while '  ' in text:
                text = text.replace('  ',' ')
            
            text1 = text.split(':')[i]
            return text1
        
        Curr_MV     = clean_and_split(Curr_MV,1)
        Last_update = clean_and_split(Last_update,1)
        Max_MV      = clean_and_split(Max_MV,2)
        
        player_data['Current_MV'] = Curr_MV
        player_data['Last_MV_update'] = Last_update
        player_data['Max_MV'] = Max_MV
    
    except:
        print( player, 'without MV')    
    
    


    ###############################################################################

     
    try:
        soup1 = soup.find('table', attrs={'class': 'items'}).tbody  
        league_stats =  []
        for X in range(0,20):
            stats =  {}
            try:
                stats['tournament'] = soup1.contents[X].contents[1].text.strip() 
                stats['games'] = soup1.contents[X].contents[2].text.strip() 
                stats['goals'] = soup1.contents[X].contents[3].text.strip() 
                stats['assist'] = soup1.contents[X].contents[4].text.strip() 
                stats['total_min'] = soup1.contents[X].contents[6].text.strip() 
            except:
                stats['tournament'] = np.nan
                
            league_stats.append(stats)

    except:
        print( player, 'without league stats') 


###############################################################################
    try:
        
        soup1 = soup.find('div', attrs={'data-id': League})
        
        stats =  {}
        stats['main'] = True
    
        stats['tournament'] = soup1.contents[1].a.text.strip()
    
        stats['games'] = soup1.contents[3].contents[1].a.text.strip()
        stats['goals'] = soup1.contents[3].contents[5].a.text.strip()
        stats['assist'] = soup1.contents[3].contents[9].a.text.strip()
        stats['perc_init'] = soup1.contents[5].span.text.strip()
        stats['yellow'] = soup1.contents[3].contents[3].a.text.strip()
        stats['doub_yellow'] = soup1.contents[3].contents[7].a.text.strip()
        stats['red'] = soup1.contents[3].contents[11].a.text.strip()
    

    except:
        print( player, 'without league stats')
    
    league_stats.append(stats)

    player_data['League_stats'] = league_stats


    tournament_players.append(player_data)


driver.close()


del Curr_MV,Last_update,Max_MV,X,content,count,league_stats,name,player,player_data,pos1,pos2,short_name,soupX,stats
del transf_history,transfer_data,url,number,


# SAVE DATA
data = tournament_players[:]

import json

# WRITTING
with open('dataMLS2019.txt', 'w') as outfile:
    json.dump(data, outfile)

with open('dataMLS2019.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


# READING
with open('dataMLS2019.txt') as json_file:
    data = json.load(json_file)
#tournament_players = data1['MLS'].copy()    


    
##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################


for X in range( len(data) ):
    try:
        clean_value = data[X]['Height:'].replace('\xa0m','').replace('\xa0m','').replace(',','.')
        clean_value = float(clean_value)
        data[X]['Height:'] = clean_value
    except:
        data[X]['Height:'] = np.nan

    try:
        Max_MV, Max_MV_date = data[X]['Max_MV'].split(' € ')
        Max_MV = Max_MV.replace('thousand','000').replace('mil.','0000').replace(',','').replace(' ','')
        Max_MV = int(Max_MV)
        data[X]['Max_MV'] = Max_MV
        data[X]['Max MV date'] = Max_MV_date
    except:
        data[X]['Max_MV'] = np.nan
        data[X]['Max MV date'] = np.nan       
        
        
    try:
        MV = data[X]['Current_MV']
        MV = MV.replace('thousand','000').replace('mil.','0000').replace(',','').replace(' ','').replace('€','')
        MV = int(MV)
        data[X]['Current_MV'] = MV 
    except:
        data[X]['Current_MV'] = np.nan 

    try:
        Pos = data[X]['Position:'].split(' - ')[0] 
        PosX = data[X]['Position:'].split(' - ')[1]
        if '-' in PosX:
            PosX = PosX.replace('-',' ')
        Pos1 = PosX.split(' ')[0] 
        Pos2 = PosX.split(' ')[1]         
        data[X]['Position1'] = Pos1 
        data[X]['Position2'] = Pos2        
    except:
        data[X]['Position1'] = 'Centre' 
        data[X]['Position2'] = 'Mid'        
        
    try:
        Pos = data[X]['Position:'].split(' - ')[0]         
        data[X]['Position:'] = Pos  
    except:
        data[X]['Position:'] = data[X]['Position:']  
           
    
    try:
        Main_cit = data[X]['Citizenship:'].split('\xa0\xa0')[0] 
        Second_cit = data[X]['Citizenship:'].split('\xa0\xa0')[1] 
        data[X]['Main_Citizenship'] = Main_cit 
        data[X]['Other_Citizenship'] = Second_cit 
    except:
        data[X]['Main_Citizenship'] = data[X]['Citizenship:']
        

    try:
        birthday = data[X]['Date of birth:']
        Zodiac = zodiac_sign(birthday)
        data[X]['Zodiac'] = Zodiac 
    except:
        data[X]['Zodiac'] = np.nan

    
    try:
        data[X]['transf_history'] = data[X]['transf_history'][0]['Left']  
    except:
        data[X]['transf_history'] = np.nan
        
    try:        
        data[X]['League_Perc_Init'] =   data[X]['League_stats'][-1]['perc_init']
        data[X]['League_Games']   = data[X]['League_stats'][-1]['games'].replace('-','0')   
        data[X]['League_Goals']   = data[X]['League_stats'][-1]['goals'].replace('-','0')       
        data[X]['League_Assist']  = data[X]['League_stats'][-1]['assist'].replace('-','0')  
        data[X]['League_Red']  = data[X]['League_stats'][-1]['red'].replace('-','0')  
        data[X]['League_Yellow']  = data[X]['League_stats'][-1]['yellow'].replace('-','0')  
        data[X]['League_2Yellow']  = data[X]['League_stats'][-1]['doub_yellow'].replace('-','0') 
        data[X]['League_stats']   = 'MLS 2019'
    except:
        data[X]['League_stats']   = 'MLS 2019'



del Main_cit,Max_MV,Max_MV_date,Pos,Pos1,Pos2,PosX,Second_cit,X,Zodiac,birthday,clean_value
del dictionary,tournament_players



df_tableau = pd.DataFrame()
for dictionary in data:     
    df = pd.DataFrame.from_dict(dictionary,orient='index').T
    df_tableau = df_tableau.append(df)
    #print(df['player_name'])

df_tableau.to_csv('MLS2019_tableau.csv',sep=',',index =False)

del dictionary,df
