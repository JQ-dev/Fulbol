# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 09:50:00 2019

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



url = 'https://fantasy.mlssoccer.com'

driver = open_url(url)

driver.find_element_by_xpath('//*[@id="landing-body"]/div[1]/div/div[2]/div[3]/div[2]/a').click()
time.sleep(2) 
driver.find_element_by_xpath('//*[@id="gigya-textbox-141263563588013010"]').send_keys('juanjose77@gmail.com')
driver.find_element_by_xpath('//*[@id="gigya-login-form"]/div[2]/div[3]/div[2]/input').send_keys('IL2bQK657?')
driver.find_element_by_xpath('//*[@id="gigya-login-form"]/div[2]/div[3]/div[5]/input').click()
time.sleep(3) 

driver.get('https://fantasy.mlssoccer.com/#stats-center')

for i in range(5):           
    try:
        driver.find_element_by_xpath('//*[@id="stats-content"]/div/div[2]/div').click()
    except:
        continue

soup = BeautifulSoup(driver.page_source, 'html.parser')

soupX = soup.find_all('div', attrs={'class': 'table-body js-body'})

player_fantasy1 = []   
player_fantasy2 = []  

count = 0
for table in soup.find_all('div', attrs={'class': 'table-body js-body'}):
    
    #table = soup.find('div', attrs={'class': 'table-body js-body'})
    if count == 0:
        print('it is a ',str(count))
        for row in table.find_all('div', attrs={'class': 'row-table'}):
            fant_dict1 = {}
            #row = table.find('div', attrs={'class': 'row-table'})
            fant_dict1['player_id'] = row.find('a')['data-player_id']
            fant_dict1['name'] = row.find('a').span.text.strip()
            name = row.find('a').span.text.strip()
            info = row.find('a').text.strip().replace(name,'')
            info = info.replace('\n','').replace('\t','').replace('\xa0','').replace(' ','')
            team,pos,value = info.split('/')
            fant_dict1['team'] = team
            fant_dict1['position'] = pos
            fant_dict1['value'] = value.replace('$','').replace('m','')
            player_fantasy1.append(fant_dict1)
        
    elif count == 1:
        print('it is a ',str(count))
        for row in table.find_all('div', attrs={'class': 'row-table'}):
            #row = table.find('div', attrs={'class': 'row-table'})
            fant_dict2 = {}
            for cell in row.find_all('div'):
                #cell = row.find('div')
                title = cell['class'][0]
                value = cell.text.strip()
                fant_dict2[title] = value
            player_fantasy2.append(fant_dict2)
    else:
        print('it is a ',str(count))
        continue
    count += 1
    


'https://www.mlssoccer.com/stats/season?page=1&franchise=select&year=2019&season_type=REG&group=shots'     
# REAL STATS

player_all_stats = [] 
stat_pages = ['goals','assists','shots','fouls','saves','goalkeeping','shutouts']
      
for stats in stat_pages:
    player_stats = [] 
    for page in range(0,30):
        try:
            url_stats = 'https://www.mlssoccer.com/stats/season?page='+str(page)+'&franchise=select&year=2019&season_type=REG&group='+stats    
            driver.get(url_stats)
            soup1 = BeautifulSoup(driver.page_source, 'html.parser')
            soup1X = soup1.find('table', attrs={'class': 'responsive no-more-tables season_stats'}).tbody.find_all('tr')
            for row in soup1X:
                #row = soup1.find('table', attrs={'class': 'responsive no-more-tables season_stats'}).tbody.find('tr')
                player = {}
                for cell in row.find_all('td'):
                    #cell = row.find('td')
                    title = cell['data-title']
                    value = cell.text.strip()
                    player[title] = value
                player_stats.append(player)    
        except:  
            continue
        player_all_stats = player_all_stats + player_stats

driver.close()

del count,fant_dict1,fant_dict2,i,info,name,player,page
del pos,soup1X,soupX,team,title,url,url_stats,value





##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################



team_names = {'ATL' : 'Atlanta United FC','CHI' : 'Chicago Fire','COL' : 'Colorado Rapids','CLB' : 'Columbus Crew SC',
    'DC' : 'D.C. United','CIN' : 'FC Cincinnati','DAL' : 'FC Dallas','HOU' : 'Houston Dynamo','LFC' : 'Los Angeles Football Club',
    'LA' : 'LA Galaxy','LAFC' : 'Los Angeles Football Club','MIN' : 'Minnesota United FC','MTL' : 'Montreal Impact',
    'NE' : 'New England Revolution','NYC' : 'New York City FC','RBNY' : 'New York Red Bulls','ORL' : 'Orlando City SC',
    'PHI' : 'Philadelphia Union','POR' : 'Portland Timbers','RSL' : 'Real Salt Lake','SJ' : 'San Jose Earthquakes',
    'SEA' : 'Seattle Sounders FC','SKC' : 'Sporting Kansas City','TOR' : 'Toronto FC','VAN' : 'Vancouver Whitecaps FC'}

team_names2 = {'ATL' : 'Atlanta United FC','CHI' : 'Chicago Fire','COL' : 'Colorado Rapids','CLB' : 'Columbus Crew SC',
    'DC' : 'D.C. United','CIN' : 'FC Cincinnati','DAL' : 'FC Dallas','HOU' : 'Houston Dynamo','LFC' : 'Los Angeles Football Club',
    'LA' : 'LA Galaxy','LAFC' : 'Los Angeles Football Club','MIN' : 'Minnesota United FC','MTL' : 'Montreal Impact',
    'NE' : 'New England Revolution','NYC' : 'New York City FC','NY' : 'New York Red Bulls','ORL' : 'Orlando City SC',
    'PHI' : 'Philadelphia Union','POR' : 'Portland Timbers','RSL' : 'Real Salt Lake','SJ' : 'San Jose Earthquakes',
    'SEA' : 'Seattle Sounders FC','SKC' : 'Sporting Kansas City','TOR' : 'Toronto FC','VAN' : 'Vancouver Whitecaps FC'}



#stats_dict = {'Player': 'Player','Club': 'Club','POS': 'Position','GP' : 'Games Played'  , 'GS': 'Games Started',
#        'MINS': 'Minutes Played','G': 'Goals', 'A': 'Assists', 'SHT': 'Shots', 'SOG': 'Shots on Goal' ,
#        'GWG':'Game Winning Goal','PKG/A':'Penalty Kick Goals / Attempts','HmG':'Home Goals','RdG':'Road Goals',
#        'G/90min' : 'Goals per 90' , 'SC%': 'Shots Converted'}




players_all_stats = {}
for DIC in player_all_stats:
    players_all_stats[DIC['Player']] = DIC['Club']

all_stats = {}
for DIC in player_all_stats:
    for key in DIC:
        all_stats[key] = np.nan

main_dict = {}
for player in players_all_stats:
    main_dict[player] = np.nan
    stat_dic = {}
    for stat in all_stats:  
        stat_dic[stat] = np.nan
    main_dict[player] = stat_dic

for DIC in player_all_stats:
    player = DIC['Player']
    for stat in DIC:
        value = DIC[stat]
        if len(value) > 0:
            main_dict[player][stat] = value




df_player_stats = pd.DataFrame()
for DICT in main_dict:
    DIC = main_dict[DICT]
    df_temp1 = pd.DataFrame.from_dict(DIC,orient='index').T
    df_player_stats = df_player_stats.append(df_temp1)




df_player_stats['team'] = df_player_stats['Club'].map(team_names)


df_player_stats['name']= df_player_stats['Player'].apply(
        lambda x: x.split(' ')[0][0].upper() + '. ' + x.split(' ')[-1].title() )

df_player_stats['name'] = df_player_stats['name'].apply(lambda x: x.replace('  ',' ') )

df_player_stats['Position'] = df_player_stats['POS'].replace('F','FWD').replace('M','MID'). \
            replace('D','DEF').replace('D-M','DEF').replace('M-F','DEF').replace('G','DEF')



df_player_stats.to_csv('stats_database.csv',sep=',',index =False)


# FANTASY

df_player_fantasy1 = pd.DataFrame()
for DIC in player_fantasy1:
    df_temp1 = pd.DataFrame.from_dict(DIC,orient='index').T
    df_player_fantasy1 = df_player_fantasy1.append(df_temp1)

df_player_fantasy2 = pd.DataFrame()
for DIC in player_fantasy2:
    df_temp1 = pd.DataFrame.from_dict(DIC,orient='index').T
    df_player_fantasy2 = df_player_fantasy2.append(df_temp1)

df_player_fantasy = pd.concat([df_player_fantasy1, df_player_fantasy2], axis=1, join='inner')


df_player_fantasy['Club'] = df_player_fantasy['team']
df_player_fantasy['team'] = df_player_fantasy['Club'].map(team_names2)

df_player_fantasy['name'] = df_player_fantasy['name'].apply(lambda x: x.replace('  ',' ') )


del df_player_fantasy1,df_player_fantasy2,df_temp1,team_names, team_names2,stats_dict
del player_fantasy1,player_fantasy2,player_stats


df_player_fantasy.to_csv('fantasy_database.csv',sep=',',index =False)




################ JOINING BY BY NAMES

df_player_fantasy['names_fantasy'] = (df_player_fantasy.loc[:,('name')] + '-' + df_player_fantasy.loc[:,('Club')])
df_player_stats['names_stats'] = (df_player_stats.loc[:,('name')] + '-' + df_player_stats.loc[:,('Club')] )


dict_ids = df_player_fantasy.loc[:,'names_fantasy']
dict_ids.index = df_player_fantasy.loc[:,'name']
dict_ids = dict_ids.to_dict()

df_player_stats['names_fantasy'] = df_player_stats.loc[:,'name'].map(dict_ids)

 
#list(df_player_stats.loc[ df_player_stats.loc[:,'names_fantasy'].isna() ,'names_stats'])


dict_ids = df_player_stats.loc[:,'names_stats']
dict_ids.index = df_player_stats.loc[:,'name']
dict_ids = dict_ids.to_dict()

df_player_fantasy['names_stats'] = df_player_fantasy.loc[:,'name'].map(dict_ids)

#list(df_player_fantasy.loc[ df_player_fantasy.loc[:,'names_stats'].isna() ,'names_fantasy'])


naming_fix1 = {
        'A. John-ORL' : 'A. De John-ORL',
        'A. Delagarza-HOU' : 'A. DeLaGarza-HOU',
        'A. Artur-CLB' : 'Artur-CLB',
        'A. Auro-TOR' : 'Auro-TOR',
        'B. Iv-LA' : 'B. Jamieson IV-LA',
        'B. Mcdonough-VAN' : 'B. McDonough-VAN',
        'C. Mccann-DC' : 'C. McCann-DC',
        'D. Quintero-MIN' : 'C. Quintero-MIN',
        'D. Silva-LAFC' : 'D. da Silva-LAFC',
        'D. Jr.-CIN' : 'D. Etienne Jr.-CIN',
        'D. Mccarty-CHI' : 'D. McCarty-CHI',
        'D. Jr.-VAN' : 'D. Norman Jr.-VAN',
        'D. Clair-MIN' : 'D. St. Clair-MIN',
        'E. Jr.-DC' : 'E. Edwards Jr.-DC',
        'E. Mccue-HOU' : 'E. McCue-HOU',
        'E. Luiz-RSL' : 'Everton Luiz-RSL',
        'F. Gutiérrez-SKC' : 'F. Gutierrez-SKC',
        'G. Wiel-TOR' : 'G. van der Wiel-TOR',
        'H. Heber-NYC' : 'H. Araujo dos Santos-NYC',
        'I. Ilsinho-PHI' : 'Ilsinho-PHI',
        'J. Mclaughlin-CIN' : 'J. McLaughlin-CIN',
        'S. Mendez-ORL' : 'J. Mendez-ORL',
        'J. Steeg-LA' : 'J. Vom Steeg-LA',
        'K. Kee-Hee-SEA' : 'K. Kee-hee-SEA',
        'K. Mcintosh-POR' : 'K. McIntosh-POR',
        'L. Pirez-ATL' : 'L. Gonzalez Pirez-ATL',
        'B. Bressan-DAL' : 'M. Bressanelli-DAL',
        'M. Crepeau-VAN' : 'M. Crépeau-VAN',
        'M. Mckenzie-PHI' : 'M. McKenzie-PHI',
        'M. Rzatkowski-RBNY' : 'M. Rzatkowksi-NY',
        'M. Werff-CIN' : 'M. van der Werff-CIN',
        'M. Marcelo-CHI' : 'Marcelo-CHI',
        'N. Deleon-TOR' : 'N. DeLeon-TOR',
        'P. Silva-ORL' : 'P. Da Silva-ORL',
        'P. Pc-VAN' : 'PC-VAN',
        'R. Robinho-ORL' : 'Robinho-ORL',
        'R. Ruan-ORL' : 'Ruan-ORL',
        'T. Mccabe-CIN' : 'T. McCabe-CIN',
        'T. Mcnamara-HOU' : 'T. McNamara-HOU',
        'V. Vako-SJ' : 'Vako-SJ',
        'Z. Macmath-VAN' : 'Z. MacMath-VAN',
        'A. Blondell-VAN' : 'XX A. Blondell-VAN',
        'A. Gamarra-RBNY' : 'Kaku-NY',
        'A. Ii-CHI' : 'XX A. Ii-CHI',
        'B. Adjei-Boateng-COL' : 'XX B. Adjei-Boateng-COL',
        'C. Jr.-RBNY' : 'C. Casseres Jr.-NY',
        'F. Fabinho-PHI' : 'Fabinho-PHI',
        'F. Felipe-DC' : 'F. Martins-DC',
        'J. Judson-SJ' : 'J. Silva Tavares-SJ',
        'J. Juninho-LA' : 'J. Vitor Junior-LA',
        'J. Santos-LA' : 'J. dos Santos-LA',
        'N. Nani-ORL' : 'Nani-ORL',
        'S. Hopeau-SEA' : 'XX S. Hopeau-SEA',
        'S. Jr.-LFC' : 'S. Brewer Jr.-LAFC',
        'W. Kamal-SKC' : 'Kuzain-SKC',
        'XX A. Abang-NY' : 'A. Abang-NY',
        'XX A. Mohamed-NYC' : 'A. Mohamed-NYC',
        'XX A. Reynolds II-CHI' : 'A. Reynolds II-CHI',
        'XX D. Sealy-DAL' : 'D. Sealy-DAL',
        'XX G. Campbell-ATL' : 'G. Campbell-ATL',
        'XX G. dos Santos-LA' : 'G. dos Santos-LA',
        'XX J. Allen-RSL' : 'J. Allen-RSL',
        'XX J. McCrary-SEA' : 'J. McCrary-SEA',
        'XX J. Qwiberg-SJ' : 'J. Qwiberg-SJ',
        'XX J. Vargas-MTL' : 'J. Vargas-MTL',
        'XX Nana-COL' : 'Nana-COL'   }

naming_fix2 = {
        'A. De John-ORL' : 'A. John-ORL',
        'A. DeLaGarza-HOU' : 'A. Delagarza-HOU',
        'Artur-CLB' : 'A. Artur-CLB',
        'Auro-TOR' : 'A. Auro-TOR',
        'B. Jamieson IV-LA' : 'B. Iv-LA',
        'B. McDonough-VAN' : 'B. Mcdonough-VAN',
        'C. McCann-DC' : 'C. Mccann-DC',
        'C. Quintero-MIN' : 'D. Quintero-MIN',
        'D. da Silva-LAFC' : 'D. Silva-LAFC',
        'D. Etienne Jr.-CIN' : 'D. Jr.-CIN',
        'D. McCarty-CHI' : 'D. Mccarty-CHI',
        'D. Norman Jr.-VAN' : 'D. Jr.-VAN',
        'D. St. Clair-MIN' : 'D. Clair-MIN',
        'E. Edwards Jr.-DC' : 'E. Jr.-DC',
        'E. McCue-HOU' : 'E. Mccue-HOU',
        'Everton Luiz-RSL' : 'E. Luiz-RSL',
        'F. Gutierrez-SKC' : 'F. Gutiérrez-SKC',
        'G. van der Wiel-TOR' : 'G. Wiel-TOR',
        'H. Araujo dos Santos-NYC' : 'H. Heber-NYC',
        'Ilsinho-PHI' : 'I. Ilsinho-PHI',
        'J. McLaughlin-CIN' : 'J. Mclaughlin-CIN',
        'J. Mendez-ORL' : 'S. Mendez-ORL',
        'J. Vom Steeg-LA' : 'J. Steeg-LA',
        'K. Kee-hee-SEA' : 'K. Kee-Hee-SEA',
        'K. McIntosh-POR' : 'K. Mcintosh-POR',
        'L. Gonzalez Pirez-ATL' : 'L. Pirez-ATL',
        'M. Bressanelli-DAL' : 'B. Bressan-DAL',
        'M. Crépeau-VAN' : 'M. Crepeau-VAN',
        'M. McKenzie-PHI' : 'M. Mckenzie-PHI',
        'M. Rzatkowksi-NY' : 'M. Rzatkowski-RBNY',
        'M. van der Werff-CIN' : 'M. Werff-CIN',
        'Marcelo-CHI' : 'M. Marcelo-CHI',
        'N. DeLeon-TOR' : 'N. Deleon-TOR',
        'P. Da Silva-ORL' : 'P. Silva-ORL',
        'PC-VAN' : 'P. Pc-VAN',
        'Robinho-ORL' : 'R. Robinho-ORL',
        'Ruan-ORL' : 'R. Ruan-ORL',
        'T. McCabe-CIN' : 'T. Mccabe-CIN',
        'T. McNamara-HOU' : 'T. Mcnamara-HOU',
        'Vako-SJ' : 'V. Vako-SJ',
        'Z. MacMath-VAN' : 'Z. Macmath-VAN',
        'XX A. Blondell-VAN' : 'A. Blondell-VAN',
        'Kaku-NY' : 'A. Gamarra-RBNY',
        'XX A. Ii-CHI' : 'A. Ii-CHI',
        'XX B. Adjei-Boateng-COL' : 'B. Adjei-Boateng-COL',
        'C. Casseres Jr.-NY' : 'C. Jr.-RBNY',
        'Fabinho-PHI' : 'F. Fabinho-PHI',
        'F. Martins-DC' : 'F. Felipe-DC',
        'J. Silva Tavares-SJ' : 'J. Judson-SJ',
        'J. Vitor Junior-LA' : 'J. Juninho-LA',
        'J. dos Santos-LA' : 'J. Santos-LA',
        'Nani-ORL' : 'N. Nani-ORL',
        'XX S. Hopeau-SEA' : 'S. Hopeau-SEA',
        'S. Brewer Jr.-LAFC' : 'S. Jr.-LFC',
        'Kuzain-SKC' : 'W. Kamal-SKC',
        'A. Mohamed-NYC' : 'XX A. Mohamed-NYC',
        'A. Reynolds II-CHI' : 'XX A. Reynolds II-CHI',
        'D. Sealy-DAL' : 'XX D. Sealy-DAL',
        'G. Campbell-ATL' : 'XX G. Campbell-ATL',
        'G. dos Santos-LA' : 'XX G. dos Santos-LA',
        'J. Allen-RSL' : 'XX J. Allen-RSL',
        'J. McCrary-SEA' : 'XX J. McCrary-SEA',
        'J. Qwiberg-SJ' : 'XX J. Qwiberg-SJ',
        'J. Vargas-MTL' : 'XX J. Vargas-MTL',
        'Nana-COL' : 'XX Nana-COL'  }       
        
df_player_stats = df_player_stats.reset_index(drop=True) 


for index in df_player_stats.index:
    value = df_player_stats.loc[index,'names_fantasy']
    name = df_player_stats.loc[index,'names_stats']
    if value is np.nan:
        new_value = naming_fix1[name]
        df_player_stats.loc[index,'names_fantasy'] = new_value
       


######################################################################################################
        
        
    

df_full = pd.merge(df_player_stats, df_player_fantasy, on='names_fantasy')

df_values = pd.read_csv('MLS2019_tableau.csv',sep=',')


df_full = df_full.reset_index(drop = True)
df_values = df_values.reset_index(drop = True)

df_full['names_full'] = df_full.loc[:,'Player'] + '-' + df_full.loc[:,'team_x']
df_values['names_values'] = df_values.loc[:,'player_name'] + '-' + df_values.loc[:,'Current club:']


dict_ids = df_full.loc[:,'names_full']
dict_ids.index = df_full.loc[:,'names_full']
dict_ids = dict_ids.to_dict()

df_values['names_full'] = df_values.loc[:,'names_values'].map(dict_ids)
 
list(df_values.loc[ df_values.loc[:,'names_full'].isna() ,'names_values'])


dict_ids = df_values.loc[:,'names_values']
dict_ids.index = df_values.loc[:,'names_values']
dict_ids = dict_ids.to_dict()

df_full['names_values'] = df_full.loc[:,'names_full'].map(dict_ids)
 
list(df_full.loc[ df_full.loc[:,'names_values'].isna() ,'names_full'])


naming_fix1 = {
        'A J Delagarza-Houston Dynamo' : 'A.J. DeLaGarza-Houston Dynamo',
        'Aaron Herrera-Real Salt Lake City' : 'Aaron Herrera-Real Salt Lake',
        'XX Abdul Rwatubyaye-Colorado Rapids' : 'Abdul Rwatubyaye-Colorado Rapids',
        'XX Adam Henley-Real Salt Lake' : 'Adam Henley-Real Salt Lake',
        'Adam Lundqvist-Houston Dynamo' : 'Adam Lundkvist-Houston Dynamo',
        'Adama Diomande-Los Angeles FC' : 'Adama Diomande-Los Angeles Football Club',
        'Adrian Zendejas-Swope Park Rangers' : 'Adrian Zendejas-Sporting Kansas City',
        'Adrien Perez-Los Angeles FC' : 'Adrien Perez-Los Angeles Football Club',
        'XX Aidan Daniels-Toronto FC' : 'Aidan Daniels-Toronto FC',
        'XX Akeem Ward-D.C. United' : 'Akeem Ward-D.C. United',
        'Albert Rusnak-Real Salt Lake City' : 'Albert Rusnak-Real Salt Lake',
        'Alec Kann-Atlanta United 2' : 'Alec Kann-Atlanta United FC',
        'Alejandro Fuenmayor-Rio Grande Valley FC Toros' : 'Alejandro Fuenmayor-Houston Dynamo',
        'Alejandro Guido-Los Angeles FC' : 'Alejandro Guido-Los Angeles Football Club',
        'Alex Crognale-Indy Eleven' : 'Alex Crognale-Columbus Crew SC',
        'Alex Horwath-Real Salt Lake City' : 'Alex Horwath-Real Salt Lake',
        'Alex Roldan-Tacoma Defiance' : 'Alex Roldan-Seattle Sounders FC',
        'Alfonso Ocampo Chavez-Tacoma Defiance' : 'Alfonso Ocampo-Chavez-Seattle Sounders FC',
        'Aljaz Ivacic-Portland Timbers 2' : 'Aljaz Ivacic-Portland Timbers',
        'XX Amar Sejdic-Montreal Impact' : 'Amar Sejdic-Montreal Impact',
        'XX Anderson Asiedu-Atlanta United FC' : 'Anderson Asiedu-Atlanta United FC',
        'XX Andre Horta-Los Angeles Football Club' : 'Andre Horta-Los Angeles Football Club',
        'Andre Rawls-Colorado Springs Switchbacks FC' : 'Andre Rawls-Colorado Rapids',
        'Andre Reynolds Ii-Chicago Fire' : 'XX Andre Reynolds Ii-Chicago Fire',
        'XX Andreas Ivan-New York Red Bulls' : 'Andreas Ivan-New York Red Bulls',
        'Andrew Carleton-Atlanta United 2' : 'Andrew Carleton-Atlanta United FC',
        'Andrew Putna-Real Monarchs SLC' : 'Andrew Putna-Real Salt Lake',
        'Anthony Fontana-Bethlehem Steel FC' : 'Anthony Fontana-Philadelphia Union',
        'Anthony Jackson Hamel-Montreal Impact' : 'Anthony Jackson-Hamel-Montreal Impact',
        'Antonio Bustamante-Loudoun United FC' : 'Antonio Bustamante-D.C. United',
        'Antonio Delamea Mlinar-New England Revolution' : 'Antonio Mlinar Delamea-New England Revolution',
        'Auro Jr -Toronto FC' : 'Auro-Toronto FC',
        'Axel Sjoberg-Colorado Rapids' : 'Axel Sjöberg-Colorado Rapids',
        'Ballou Tabla-Montreal Impact' : 'Ballou Jean-Yves Tabla-Montreal Impact',
        'Ben Mines-New York Red Bulls II' : 'Ben Lundgaard-Columbus Crew SC',
        'XX Ben Lundt-FC Cincinnati' : 'Ben Lundt-FC Cincinnati',
        'XX Ben Mines-New York Red Bulls' : 'Ben Mines-New York Red Bulls',
        'XX Blake Smith-FC Cincinnati' : 'Blake Smith-FC Cincinnati',
        'XX Bobby Shuttleworth-Minnesota United FC' : 'Bobby Shuttleworth-Minnesota United FC',
        'XX Bradford Jamieson IV-LA Galaxy' : 'Bradford Jamieson IV-LA Galaxy',
        'Bradley Wright Phillips-New York Red Bulls' : 'Bradley Wright-Phillips-New York Red Bulls',
        'Brandon Vazquez-Atlanta United 2' : 'Brandon Vazquez-Atlanta United FC',
        'XX Brendan McDonough-Vancouver Whitecaps FC' : 'Brendan McDonough-Vancouver Whitecaps FC',
        'Brendan Moore-Atlanta United 2' : 'Brendan Moore-Atlanta United FC',
        'Brian Rodriguez-Los Angeles FC' : 'Brian Rodriguez-Los Angeles Football Club',
        'Brian Wright-Birmingham Legion FC' : 'Brian Wright-New England Revolution',
        'Brooks Lennon-Real Salt Lake City' : 'Brooks Lennon-Real Salt Lake',
        'Bryan Meredith-Tacoma Defiance' : 'Bryan Meredith-Seattle Sounders FC',
        'C J Sapong-Chicago Fire' : 'CJ Sapong-Chicago Fire',
        'Cade Cowell-Reno 1868 FC' : 'Cade Cowell-San Jose Earthquakes',
        'Caleb Patterson Sewell-Toronto FC' : 'Caleb Patterson-Sewell-Toronto FC',
        'XX Cameron Lindley-Orlando City SC' : 'Cameron Lindley-Orlando City SC',
        'XX Carlos Gruezo-FC Dallas' : 'Carlos Gruezo-FC Dallas',
        'XX Carlos Miguel Coronel-Philadelphia Union' : 'Carlos Miguel Coronel-Philadelphia Union',
        'Carlos Vela-Los Angeles FC' : 'Carlos Vela-Los Angeles Football Club',
        'Carter Manley-Forward Madison FC' : 'Carter Manley-Minnesota United FC',
        'XX Chad Marshall-Seattle Sounders FC' : 'Chad Marshall-Seattle Sounders FC',
        'XX Chris Durkin-D.C. United' : 'Chris Durkin-D.C. United',
        'XX Chris Duvall-Houston Dynamo' : 'Chris Duvall-Houston Dynamo',
        'Chris Goslin-Atlanta United 2' : 'Chris Goslin-Atlanta United FC',
        'XX Chris McCann-D.C. United' : 'Chris McCann-D.C. United',
        'Chris Odoi Atsem-Loudoun United FC' : 'Chris Odoi-Atsem-D.C. United',
        'Chris Pontius-Los Angeles Galaxy' : 'Chris Pontius-LA Galaxy',
        'XX Cody Cropper-New England Revolution' : 'Cody Cropper-New England Revolution',
        'Collin Martin-Hartford Athletic' : 'Collin Martin-Minnesota United FC',
        'Corey Baird-Real Salt Lake City' : 'Corey Baird-Real Salt Lake',
        'XX Cory Burke-Philadelphia Union' : 'Cory Burke-Philadelphia Union',
        'Cristhian Casseres Jr -New York Red Bulls' : 'Cristian Casseres Jr.-New York Red Bulls',
        'XX Cristian Martinez-Chicago Fire' : 'Cristian Martinez-Chicago Fire',
        'Cristian Pavon-Los Angeles Galaxy' : 'Cristian Pavon-LA Galaxy',
        'Dairon Asprilla-Portland Timbers 2' : 'Dairon Asprilla-Portland Timbers',
        'Damarcus Beasley-Houston Dynamo' : 'DaMarcus Beasley-Houston Dynamo',
        'Damir Kreilach-Real Salt Lake City' : 'Damir Kreilach-Real Salt Lake',
        'XX Daniel Bedoya-New York City FC' : 'Daniel Bedoya-New York City FC',
        'Daniel Steres-Los Angeles Galaxy' : 'Daniel Steres-LA Galaxy',
        'Danilo Silva-Los Angeles FC' : 'Danilo Silva-Los Angeles Football Club',
        'Danny Leyva-Tacoma Defiance' : 'Danny Leyva-Seattle Sounders FC',
        'Dave Romney-Los Angeles Galaxy' : 'Dave Romney-LA Galaxy',
        'David Bingham-Los Angeles Galaxy' : 'David Bingham-LA Galaxy',
        'XX David Norman Jr.-Vancouver Whitecaps FC' : 'David Norman Jr.-Vancouver Whitecaps FC',
        'XX David Ochoa-Real Salt Lake' : 'David Ochoa-Real Salt Lake',
        'Dax Mccarty-Chicago Fire' : 'Dax McCarty-Chicago Fire',
        'Dayne St Clair-Forward Madison FC' : 'Dayne St. Clair-Minnesota United FC',
        'XX Dejan Jakovic-Los Angeles Football Club' : 'Dejan Jakovic-Los Angeles Football Club',
        'Dejuan Jones-New England Revolution' : 'DeJuan Jones-New England Revolution',
        'Derrick Etienne-FC Cincinnati' : 'Derrick Etienne Jr.-FC Cincinnati',
        'Diedie Traore-Los Angeles Galaxy II' : 'Diedie Traore-LA Galaxy',
        'Diego Palacios-Los Angeles FC' : 'Diego Palacios-Los Angeles Football Club',
        'Diego Polenta-Los Angeles Galaxy' : 'Diego Polenta-LA Galaxy',
        'Diego Rossi-Los Angeles FC' : 'Diego Rossi-Los Angeles Football Club',
        'Dion Pereira-Atlanta United 2' : 'Dion Pereira-Atlanta United FC',
        'Donny Toia-Real Salt Lake City' : 'Donny Toia-Real Salt Lake',
        'Douglas Martinez-Real Salt Lake City' : 'Douglas Martinez-Real Salt Lake',
        'Earl Edwards Jr -Loudoun United FC' : 'Earl Edwards Jr.-D.C. United',
        'Eddie Segura-Los Angeles FC' : 'Eddie Segura-Los Angeles Football Club',
        'Eduard Atuesta-Los Angeles FC' : 'Eduard Atuesta-Los Angeles Football Club',
        'XX Edward Opoku-Columbus Crew SC' : 'Edward Opoku-Columbus Crew SC',
        'Efrain Alvarez-Los Angeles Galaxy' : 'Efrain Alvarez-LA Galaxy',
        'Emil Cuello-Los Angeles Galaxy II' : 'Elliot Collier-Chicago Fire',
        'XX Ema Twumasi-FC Dallas' : 'Ema Twumasi-FC Dallas',
        'XX Emery Welshman-FC Cincinnati' : 'Emery Welshman-FC Cincinnati',
        'XX Emil Cuello-LA Galaxy' : 'Emil Cuello-LA Galaxy',
        'Eric Bird-Rio Grande Valley FC Toros' : 'Eric Bird-Houston Dynamo',
        'Eric Calvillo-Reno 1868 FC' : 'Eric Calvillo-San Jose Earthquakes',
        'Eric Dick-Swope Park Rangers' : 'Eric Dick-Sporting Kansas City',
        'Erik Holt-Real Monarchs SLC' : 'Erik Holt-Real Salt Lake',
        'Erik Mccue-Rio Grande Valley FC Toros' : 'Erik McCue-Houston Dynamo',
        'Eryk Williamson-Portland Timbers 2' : 'Eryk Williamson-Portland Timbers',
        'Ethan Zubak-Los Angeles Galaxy II' : 'Ethan Zubak-LA Galaxy',
        'Evan Louro-New York Red Bulls II' : 'Evan Louro-New York Red Bulls',
        'Everton Luiz-Real Salt Lake City' : 'Everton Luiz-Real Salt Lake',
        'Favio Alvarez-Los Angeles Galaxy' : 'Favio Alvarez-LA Galaxy',
        'Felipe Gutierrez-Sporting Kansas City' : 'Felipe Gutiérrez-Sporting Kansas City',
        'Felipe Hernandez-Swope Park Rangers' : 'Felipe Hernandez-Sporting Kansas City',
        'Felipe Martins-D.C. United' : 'Felipe-D.C. United',
        'XX Forrest Lasso-FC Cincinnati' : 'Forrest Lasso-FC Cincinnati',
        'Foster Langsdorf-Portland Timbers 2' : 'Foster Langsdorf-Portland Timbers',
        'Francis Atuahene-Austin Bold FC' : 'Francis Atuahene-FC Dallas',
        'XX Gabriel Somi-New England Revolution' : 'Gabriel Somi-New England Revolution',
        'Gary Mackay Steven-New York City FC' : 'Gary Mackay-Steven-New York City FC',
        'XX Gaston Sauro-Columbus Crew SC' : 'Gaston Sauro-Columbus Crew SC',
        'Gedion Zelalem-Swope Park Rangers' : 'Gedion Zelalem-Sporting Kansas City',
        'George Bello-Atlanta United 2' : 'George Bello-Atlanta United FC',
        'Gerso-Sporting Kansas City' : 'Gerso Fernandes-Sporting Kansas City',
        'Giancarlo Gonzalez-Los Angeles Galaxy' : 'Giancarlo Gonzalez-LA Galaxy',
        'Gianluca Busio-Swope Park Rangers' : 'Gianluca Busio-Sporting Kansas City',
        'Gilbert Fuentes-Reno 1868 FC' : 'Gilbert Fuentes-San Jose Earthquakes',
        'Gonzalo Martinez-Atlanta United FC' : 'XX Gonzalo Martinez-Atlanta United FC',
        'Gordon Wild-Loudoun United FC' : 'Gordon Wild-D.C. United',
        'Graham Smith-Swope Park Rangers' : 'Graham Smith-Sporting Kansas City',
        'Grant Lillard-Lansing Ignite FC' : 'Grant Lillard-Chicago Fire',
        'XX Gregory van der Wiel-Toronto FC' : 'Gregory van der Wiel-Toronto FC',
        'Griffin Yow-Loudoun United FC' : 'Griffin Yow-D.C. United',
        'Handwalla Bwana-Tacoma Defiance' : 'Handwalla Bwana-Seattle Sounders FC',
        'XX Harry Novillo-Montreal Impact' : 'Harry Novillo-Montreal Impact',
        'XX Hassan Ndam-FC Cincinnati' : 'Hassan Ndam-FC Cincinnati',
        'XX Henry Wingo-Seattle Sounders FC' : 'Henry Wingo-Seattle Sounders FC',
        'Hugo Arellano-Orange County SC' : 'Hugo Arellano-LA Galaxy',
        'In Beom Hwang-Vancouver Whitecaps FC' : 'Inbeom Hwang-Vancouver Whitecaps FC',
        'Ismael Tajouri Shradi-New York City FC' : 'Isaac Angking-New England Revolution',
        'XX Ismael Tajouri-Shradi-New York City FC' : 'Ismael Tajouri-Shradi-New York City FC',
        'Jacob Akanyirige-Reno 1868 FC' : 'Jacob Akanyirige-San Jose Earthquakes',
        'Jasser Khemiri-Vancouver Whitecaps FC' : 'Jasser Khmiri-Vancouver Whitecaps FC',
        'Javi Perez-Los Angeles FC' : 'Javi Perez-Los Angeles Football Club',
        'Jaylin Lindsey-Swope Park Rangers' : 'Jaylin Lindsey-Sporting Kansas City',
        'Jean Christophe Koffi-New York Red Bulls II' : 'Jean-Christophe Koffi-New York Red Bulls',
        'XX Jeff Caldwell-New York City FC' : 'Jeff Caldwell-New York City FC',
        'Jefferson Savarino-Real Salt Lake City' : 'Jefferson Savarino-Real Salt Lake',
        'Jimmy Mclaughlin-FC Cincinnati' : 'Jimmy McLaughlin-FC Cincinnati',
        'XX Jimmy Ockford-San Jose Earthquakes' : 'Jimmy Ockford-San Jose Earthquakes',
        'Jj Williams-Birmingham Legion FC' : 'JJ Williams-Columbus Crew SC',
        'Joao Plata-Real Salt Lake City' : 'Joao Plata-Real Salt Lake',
        'Joe Corona-Los Angeles Galaxy' : 'Joe Corona-LA Galaxy',
        'XX Johan Blomberg-Colorado Rapids' : 'Johan Blomberg-Colorado Rapids',
        'XX Jon Bakero-Toronto FC' : 'Jon Bakero-Toronto FC',
        'XX Jon Gallagher-Atlanta United FC' : 'Jon Gallagher-Atlanta United FC',
        'Jonathan Campbell-Tacoma Defiance' : 'Jonathan Campbell-Seattle Sounders FC',
        'Jonathan Dos Santos-Los Angeles Galaxy' : 'Jonathan dos Santos-LA Galaxy',
        'Jordan Allen-Real Salt Lake City' : 'XX Jordan Allen-Real Salt Lake City',
        'Jordan Harvey-Los Angeles FC' : 'Jordan Harvey-Los Angeles Football Club',
        'Jordy Delem-Tacoma Defiance' : 'Jordy Delem-Seattle Sounders FC',
        'Jorge Villafana-Portland Timbers' : 'Jorge Villafaña-Portland Timbers',
        'Jorgen Skjelvik-Los Angeles Galaxy' : 'Jorgen Skjelvik-LA Galaxy',
        'Joseph Claude Gyau-FC Cincinnati' : 'Joe Gyau-FC Cincinnati',
        'Joshua Perez-Phoenix Rising FC' : 'Josh Perez-Los Angeles Football Club',
        'Jt Marcinkowski-Reno 1868 FC' : 'JT Marcinkowski-San Jose Earthquakes',
        'XX Jose Hernandez-Atlanta United FC' : 'Jose Hernandez-Atlanta United FC',
        'XX Josue Colman-Orlando City SC' : 'Josue Colman-Orlando City SC',
        'Juan Torres-New York City FC' : 'Juan Pablo Torres-New York City FC',
        'Julian Araujo-Los Angeles Galaxy' : 'Julian Araujo-LA Galaxy',
        'Julian Dunn Johnson-Toronto FC' : 'Julian Dunn-Toronto FC',
        'Julian Vazquez-Real Monarchs SLC' : 'Julian Vazquez-Real Salt Lake',
        'Juninho-Los Angeles Galaxy' : 'Juninho-LA Galaxy',
        'Justen Glad-Real Salt Lake City' : 'Justen Glad-Real Salt Lake',
        'Justin Dhillon-Tacoma Defiance' : 'Justin Dhillon-Seattle Sounders FC',
        'Justin Portillo-Real Monarchs SLC' : 'Justin Portillo-Real Salt Lake',
        'XX Justin Rennicks-New England Revolution' : 'Justin Rennicks-New England Revolution',
        'Justin Vom Steeg-Los Angeles Galaxy II' : 'Justin Vom Steeg-LA Galaxy',
        'Kee Hee Kim-Seattle Sounders FC' : 'Kim Kee-hee-Seattle Sounders FC',
        'Kelyn Rowe-Real Salt Lake City' : 'Kelyn Rowe-Real Salt Lake',
        'Kendall Mcintosh-Portland Timbers' : 'Kendall McIntosh-Portland Timbers',
        'XX Kenny Saief-FC Cincinnati' : 'Kenny Saief-FC Cincinnati',
        'Kevin Partida-Reno 1868 FC' : 'Kevin Partida-San Jose Earthquakes',
        'Kyle Beckerman-Real Salt Lake City' : 'Kyle Beckerman-Real Salt Lake',
        'Kyle Duncan-New York Red Bulls II' : 'Kyle Duncan-New York Red Bulls',
        'XX Lagos Kunga-Atlanta United FC' : 'Lagos Kunga-Atlanta United FC',
        'Lamar Batista-FC Tucson' : 'Lamar Batista-Los Angeles Football Club',
        'Latif Blessing-Los Angeles FC' : 'Latif Blessing-Los Angeles Football Club',
        'Lee Nguyen-Los Angeles FC' : 'Lee Nguyen-Los Angeles Football Club',
        'XX Logan Gdula-FC Cincinnati' : 'Logan Gdula-FC Cincinnati',
        'XX Lucas Melano-Portland Timbers' : 'Lucas Melano-Portland Timbers',
        'XX Lucas Venuto-Vancouver Whitecaps FC' : 'Lucas Venuto-Vancouver Whitecaps FC',
        'Luis Caicedo-New England Revolution' : 'Luis Alberto Caicedo-New England Revolution',
        'Luis Arriaga-Real Monarchs SLC' : 'Luis Arriaga-Real Salt Lake',
        'Luiz Fernando Nascimento-Atlanta United 2' : 'Luiz Fernando-Atlanta United FC',
        'Luke Mulholland-Real Monarchs SLC' : 'Luke Mulholland-Real Salt Lake',
        'Maikel Van Der Werff-FC Cincinnati' : 'Maikel van der Werff-FC Cincinnati',
        'Marcelo Silva-Real Salt Lake City' : 'Marcelo Silva-Real Salt Lake',
        'Marco Farfan-Portland Timbers 2' : 'Marco Farfan-Portland Timbers',
        'XX Marcus Epps-New York Red Bulls' : 'Marcus Epps-New York Red Bulls',
        'Mark Mckenzie-Bethlehem Steel FC' : 'Mark McKenzie-Philadelphia Union',
        'Mark Anthony Kaye-Los Angeles FC' : 'Mark-Anthony Kaye-Los Angeles Football Club',
        'Marvin Loria-Portland Timbers 2' : 'Marvin Loria-Portland Timbers',
        'XX Mason Stajduhar-Orlando City SC' : 'Mason Stajduhar-Orlando City SC',
        'Mason Toye-Forward Madison FC' : 'Mason Toye-Minnesota United FC',
        'Mathias Jorgensen-New York Red Bulls II' : 'Mathias Jorgensen-New York Red Bulls',
        'Matt Bersano-Reno 1868 FC' : 'Matt Bersano-San Jose Earthquakes',
        'Matt Freese-Bethlehem Steel FC' : 'Matt Freese-Philadelphia Union',
        'Matt Hundley-Colorado Springs Switchbacks FC' : 'Matt Hundley-Colorado Rapids',
        'Matt Lampson-Los Angeles Galaxy' : 'Matt Lampson-LA Galaxy',
        'Matthew Real-Bethlehem Steel FC' : 'Matthew Real-Philadelphia Union',
        'Maxi Moralez-New York City FC' : 'Maximiliano Moralez-New York City FC',
        'Michael Murillo-New York Red Bulls' : 'Michael Amir Murillo-New York Red Bulls',
        'Michael Nelson-Rio Grande Valley FC Toros' : 'Michael Nelson-Houston Dynamo',
        'Michael Salazar-Rio Grande Valley FC Toros' : 'Michael Salazar-Houston Dynamo',
        'Michee Ngalina-Bethlehem Steel FC' : 'Michee Ngalina-Philadelphia Union',
        'Mike Azira-Chicago Fire' : 'Micheal Azira-Chicago Fire',
        'Mikey Ambrose-Atlanta United 2' : 'Mikey Ambrose-Atlanta United FC',
        'Mo Adams-Atlanta United 2' : 'Mo Adams-Atlanta United FC',
        'Modou Jadama-Portland Timbers 2' : 'Modou Jadama-Portland Timbers',
        'Mohamed El Munir-Los Angeles FC' : 'Mohamed El-Munir-Los Angeles Football Club',
        'Moses Nyeman-Loudoun United FC' : 'Moises Hernandez-FC Dallas',
        'Nedum Onuoha-Real Salt Lake City' : 'Nedum Onuoha-Real Salt Lake',
        'XX Nazmi Albadawi-FC Cincinnati' : 'Nazmi Albadawi-FC Cincinnati',
        'Nemanja Nikolics-Chicago Fire' : 'Nemanja Nikolic-Chicago Fire',
        'Nick Besler-Real Salt Lake City' : 'Nick Besler-Real Salt Lake',
        'Nick Deleon-Toronto FC' : 'Nick DeLeon-Toronto FC',
        'Nick Rimando-Real Salt Lake City' : 'Nick Rimando-Real Salt Lake',
        'Nico Gaitan-Chicago Fire' : 'Nicolas Gaitan-Chicago Fire',
        'Nicolas Lodeiro-Seattle Sounders FC' : 'Nicolás Lodeiro-Seattle Sounders FC',
        'Niki Jackson-Charlotte Independence' : 'Niki Jackson-Colorado Rapids',
        'XX Niko Hamalainen-Los Angeles Football Club' : 'Niko Hamalainen-Los Angeles Football Club',
        'Noble Okello-Toronto FC II' : 'Noble Okello-Toronto FC',
        'Nouhou-Tacoma Defiance' : 'Nouhou Tolo-Seattle Sounders FC',
        'Olivier Mbaizo-Bethlehem Steel FC' : 'Olivier Mbaizo-Philadelphia Union',
        'XX Omar Browne-Montreal Impact' : 'Omar Browne-Montreal Impact',
        'XX Pablo Aranguiz-FC Dallas' : 'Pablo Aranguiz-FC Dallas',
        'XX Pablo Ruiz-Real Salt Lake' : 'Pablo Ruiz-Real Salt Lake',
        'Pablo Sisniega-Los Angeles FC' : 'Pablo Sisniega-Los Angeles Football Club',
        'Patrick Okonkwo-Atlanta United 2' : 'Patrick Okonkwo-Atlanta United FC',
        'Pctm-Vancouver Whitecaps FC' : 'PC-Vancouver Whitecaps FC',
        'Perry Kitchen-Los Angeles Galaxy' : 'Perry Kitchen-LA Galaxy',
        'XX Peter-Lee Vassell-Los Angeles Football Club' : 'Peter-Lee Vassell-Los Angeles Football Club',
        'XX Phillip Ejimadu-Los Angeles Football Club' : 'Phillip Ejimadu-Los Angeles Football Club',
        'XX Pierre Da Silva-Orlando City SC' : 'Pierre Da Silva-Orlando City SC',
        'XX Pity Martinez-Atlanta United FC' : 'Pity Martinez-Atlanta United FC',
        'XX Renzo Zambrano-Portland Timbers' : 'Renzo Zambrano-Portland Timbers',
        'Renzo Zambrano-Portland Timbers 2' : 'Renzo Zambrano-Portland Timbers',
        'R J Allen-Philadelphia Union' : 'RJ Allen-Philadelphia Union',
        'XX Rodolfo Zelaya-Los Angeles Football Club' : 'Rodolfo Zelaya-Los Angeles Football Club',
        'Rolf Feltscher-Los Angeles Galaxy' : 'Rolf Feltscher-LA Galaxy',
        'Romain Alessandrini-Los Angeles Galaxy' : 'Romain Alessandrini-LA Galaxy',
        'Roman Torres-Tacoma Defiance' : 'Román Torres-Seattle Sounders FC',
        'XX Romario Ibarra-Minnesota United FC' : 'Romario Ibarra-Minnesota United FC',
        'Ronaldo Pena-Rio Grande Valley FC Toros' : 'Ronaldo Peña-Houston Dynamo',
        'Ryan Telfer-York9 FC' : 'Ryan Telfer-Toronto FC',
        'Saad Abdul Salaam-Tacoma Defiance' : 'Saad Abdul-Salaam-Seattle Sounders FC',
        'Sam Johnson-Real Salt Lake City' : 'Sam Johnson-Real Salt Lake',
        'Sam Junqua-Rio Grande Valley FC Toros' : 'Sam Junqua-Houston Dynamo',
        'Sam Raben-Colorado Springs Switchbacks FC' : 'Sam Raben-Colorado Rapids',
        'Santiago Patino-Orlando City SC' : 'Santiago Patiño-Orlando City SC',
        'Sean Nealis-New York Red Bulls II' : 'Sean Nealis-New York Red Bulls',
        'Sebastian Lletget-Los Angeles Galaxy' : 'Sebastian Lletget-LA Galaxy',
        'Sebastian Saucedo-Real Salt Lake City' : 'Sebastian Saucedo-Real Salt Lake',
        'Servando Carrasco-Los Angeles Galaxy' : 'Servando Carrasco-LA Galaxy',
        'XX Shaft Brewer Jr.-Los Angeles Football Club' : 'Shaft Brewer Jr.-Los Angeles Football Club',
        'Shane Oneill-Orlando City SC' : 'Shane O\'Neill-Orlando City SC',
        'Siad Haji-Reno 1868 FC' : 'Siad Haji-San Jose Earthquakes',
        'Stefan Cleveland-Lansing Ignite FC' : 'Stefan Cleveland-Chicago Fire',
        'Steve Birnbaum-D.C. United' : 'Steven Birnbaum-D.C. United',
        'Steven Beitashour-Los Angeles FC' : 'Steven Beitashour-Los Angeles Football Club',
        'Tate Schmitt-Real Monarchs SLC' : 'Tate Schmitt-Real Salt Lake',
        'Tom Barlow-New York Red Bulls II' : 'Tom Barlow-New York Red Bulls',
        'Tomas Hilliard Arce-Los Angeles Galaxy II' : 'Tomas Hilliard-Arce-LA Galaxy',
        'XX Terrence Boyd-Toronto FC' : 'Terrence Boyd-Toronto FC',
        'Tommy Mcnamara-Houston Dynamo' : 'Thomas McNamara-Houston Dynamo',
        'XX Thomas Meilleur-Giguere-Montreal Impact' : 'Thomas Meilleur-Giguere-Montreal Impact',
        'XX Tommy McCabe-FC Cincinnati' : 'Tommy McCabe-FC Cincinnati',
        'XX Tony Beltran-Real Salt Lake' : 'Tony Beltran-Real Salt Lake',
        'Trey Muse-Tacoma Defiance' : 'Trey Muse-Seattle Sounders FC',
        'Tristan Blackmon-Los Angeles FC' : 'Tristan Blackmon-Los Angeles Football Club',
        'Tyler Deric-Rio Grande Valley FC Toros' : 'Tyler Deric-Houston Dynamo',
        'Tyler Freeman-Swope Park Rangers' : 'Tyler Freeman-Sporting Kansas City',
        'Tyler Miller-Los Angeles FC' : 'Tyler Miller-Los Angeles Football Club',
        'Uriel Antuna-Los Angeles Galaxy' : 'Uriel Antuna-LA Galaxy',
        'Valeri Qazaishvili-San Jose Earthquakes' : 'Vako-San Jose Earthquakes',
        'Vincent Bezecourt-New York Red Bulls II' : 'Vincent Bezecourt-New York Red Bulls',
        'Walker Zimmerman-Los Angeles FC' : 'Walker Zimmerman-Los Angeles Football Club',
        'Wan Kuzain-Swope Park Rangers' : 'Wan Kuzain Wan Kamal-Sporting Kansas City',
        'Will Bruin-Tacoma Defiance' : 'Will Bruin-Seattle Sounders FC',
        'Wyatt Omsberg-Forward Madison FC' : 'Wyatt Omsberg-Minnesota United FC',
        'Zac Macmath-Vancouver Whitecaps FC' : 'Yohan Croizet-Sporting Kansas City',
        'XX Zac MacMath-Vancouver Whitecaps FC' : 'Zac MacMath-Vancouver Whitecaps FC',
        'Zachary Brault Guillard-Montreal Impact' : 'Zachary Brault-Guillard-Montreal Impact',
        'Zachary Herivaux-Birmingham Legion FC' : 'Zachary Herivaux-New England Revolution',
        'XX Zack Steffen-Columbus Crew SC' : 'Zack Steffen-Columbus Crew SC',
        'XX Zakaria Diallo-Montreal Impact' : 'Zakaria Diallo-Montreal Impact',
        'Zlatan Ibrahimovic-Los Angeles Galaxy' : 'Zlatan Ibrahimovic-LA Galaxy',
        'XX Zoltan Stieber-D.C. United' : 'Zoltan Stieber-D.C. United'}

        
naming_fix2 = {
        'A.J. DeLaGarza-Houston Dynamo' : 'A J Delagarza-Houston Dynamo',
        'Aaron Herrera-Real Salt Lake' : 'Aaron Herrera-Real Salt Lake City',
        'Abdul Rwatubyaye-Colorado Rapids' : 'XX Abdul Rwatubyaye-Colorado Rapids',
        'Adam Henley-Real Salt Lake' : 'XX Adam Henley-Real Salt Lake',
        'Adam Lundkvist-Houston Dynamo' : 'Adam Lundqvist-Houston Dynamo',
        'Adama Diomande-Los Angeles Football Club' : 'Adama Diomande-Los Angeles FC',
        'Adrian Zendejas-Sporting Kansas City' : 'Adrian Zendejas-Swope Park Rangers',
        'Adrien Perez-Los Angeles Football Club' : 'Adrien Perez-Los Angeles FC',
        'Aidan Daniels-Toronto FC' : 'XX Aidan Daniels-Toronto FC',
        'Akeem Ward-D.C. United' : 'XX Akeem Ward-D.C. United',
        'Albert Rusnak-Real Salt Lake' : 'Albert Rusnak-Real Salt Lake City',
        'Alec Kann-Atlanta United FC' : 'Alec Kann-Atlanta United 2',
        'Alejandro Fuenmayor-Houston Dynamo' : 'Alejandro Fuenmayor-Rio Grande Valley FC Toros',
        'Alejandro Guido-Los Angeles Football Club' : 'Alejandro Guido-Los Angeles FC',
        'Alex Crognale-Columbus Crew SC' : 'Alex Crognale-Indy Eleven',
        'Alex Horwath-Real Salt Lake' : 'Alex Horwath-Real Salt Lake City',
        'Alex Roldan-Seattle Sounders FC' : 'Alex Roldan-Tacoma Defiance',
        'Alfonso Ocampo-Chavez-Seattle Sounders FC' : 'Alfonso Ocampo Chavez-Tacoma Defiance',
        'Aljaz Ivacic-Portland Timbers' : 'Aljaz Ivacic-Portland Timbers 2',
        'Amar Sejdic-Montreal Impact' : 'XX Amar Sejdic-Montreal Impact',
        'Anderson Asiedu-Atlanta United FC' : 'XX Anderson Asiedu-Atlanta United FC',
        'Andre Horta-Los Angeles Football Club' : 'XX Andre Horta-Los Angeles Football Club',
        'Andre Rawls-Colorado Rapids' : 'Andre Rawls-Colorado Springs Switchbacks FC',
        'XX Andre Reynolds Ii-Chicago Fire' : 'Andre Reynolds Ii-Chicago Fire',
        'Andreas Ivan-New York Red Bulls' : 'XX Andreas Ivan-New York Red Bulls',
        'Andrew Carleton-Atlanta United FC' : 'Andrew Carleton-Atlanta United 2',
        'Andrew Putna-Real Salt Lake' : 'Andrew Putna-Real Monarchs SLC',
        'Anthony Fontana-Philadelphia Union' : 'Anthony Fontana-Bethlehem Steel FC',
        'Anthony Jackson-Hamel-Montreal Impact' : 'Anthony Jackson Hamel-Montreal Impact',
        'Antonio Bustamante-D.C. United' : 'Antonio Bustamante-Loudoun United FC',
        'Antonio Mlinar Delamea-New England Revolution' : 'Antonio Delamea Mlinar-New England Revolution',
        'Auro-Toronto FC' : 'Auro Jr -Toronto FC',
        'Axel Sjöberg-Colorado Rapids' : 'Axel Sjoberg-Colorado Rapids',
        'Ballou Jean-Yves Tabla-Montreal Impact' : 'Ballou Tabla-Montreal Impact',
        'Ben Lundgaard-Columbus Crew SC' : 'Ben Mines-New York Red Bulls II',
        'Ben Lundt-FC Cincinnati' : 'XX Ben Lundt-FC Cincinnati',
        'Ben Mines-New York Red Bulls' : 'XX Ben Mines-New York Red Bulls',
        'Blake Smith-FC Cincinnati' : 'XX Blake Smith-FC Cincinnati',
        'Bobby Shuttleworth-Minnesota United FC' : 'XX Bobby Shuttleworth-Minnesota United FC',
        'Bradford Jamieson IV-LA Galaxy' : 'XX Bradford Jamieson IV-LA Galaxy',
        'Bradley Wright-Phillips-New York Red Bulls' : 'Bradley Wright Phillips-New York Red Bulls',
        'Brandon Vazquez-Atlanta United FC' : 'Brandon Vazquez-Atlanta United 2',
        'Brendan McDonough-Vancouver Whitecaps FC' : 'XX Brendan McDonough-Vancouver Whitecaps FC',
        'Brendan Moore-Atlanta United FC' : 'Brendan Moore-Atlanta United 2',
        'Brian Rodriguez-Los Angeles Football Club' : 'Brian Rodriguez-Los Angeles FC',
        'Brian Wright-New England Revolution' : 'Brian Wright-Birmingham Legion FC',
        'Brooks Lennon-Real Salt Lake' : 'Brooks Lennon-Real Salt Lake City',
        'Bryan Meredith-Seattle Sounders FC' : 'Bryan Meredith-Tacoma Defiance',
        'CJ Sapong-Chicago Fire' : 'C J Sapong-Chicago Fire',
        'Cade Cowell-San Jose Earthquakes' : 'Cade Cowell-Reno 1868 FC',
        'Caleb Patterson-Sewell-Toronto FC' : 'Caleb Patterson Sewell-Toronto FC',
        'Cameron Lindley-Orlando City SC' : 'XX Cameron Lindley-Orlando City SC',
        'Carlos Gruezo-FC Dallas' : 'XX Carlos Gruezo-FC Dallas',
        'Carlos Miguel Coronel-Philadelphia Union' : 'XX Carlos Miguel Coronel-Philadelphia Union',
        'Carlos Vela-Los Angeles Football Club' : 'Carlos Vela-Los Angeles FC',
        'Carter Manley-Minnesota United FC' : 'Carter Manley-Forward Madison FC',
        'Chad Marshall-Seattle Sounders FC' : 'XX Chad Marshall-Seattle Sounders FC',
        'Chris Durkin-D.C. United' : 'XX Chris Durkin-D.C. United',
        'Chris Duvall-Houston Dynamo' : 'XX Chris Duvall-Houston Dynamo',
        'Chris Goslin-Atlanta United FC' : 'Chris Goslin-Atlanta United 2',
        'Chris McCann-D.C. United' : 'XX Chris McCann-D.C. United',
        'Chris Odoi-Atsem-D.C. United' : 'Chris Odoi Atsem-Loudoun United FC',
        'Chris Pontius-LA Galaxy' : 'Chris Pontius-Los Angeles Galaxy',
        'Cody Cropper-New England Revolution' : 'XX Cody Cropper-New England Revolution',
        'Collin Martin-Minnesota United FC' : 'Collin Martin-Hartford Athletic',
        'Corey Baird-Real Salt Lake' : 'Corey Baird-Real Salt Lake City',
        'Cory Burke-Philadelphia Union' : 'XX Cory Burke-Philadelphia Union',
        'Cristian Casseres Jr.-New York Red Bulls' : 'Cristhian Casseres Jr -New York Red Bulls',
        'Cristian Martinez-Chicago Fire' : 'XX Cristian Martinez-Chicago Fire',
        'Cristian Pavon-LA Galaxy' : 'Cristian Pavon-Los Angeles Galaxy',
        'Dairon Asprilla-Portland Timbers' : 'Dairon Asprilla-Portland Timbers 2',
        'DaMarcus Beasley-Houston Dynamo' : 'Damarcus Beasley-Houston Dynamo',
        'Damir Kreilach-Real Salt Lake' : 'Damir Kreilach-Real Salt Lake City',
        'Daniel Bedoya-New York City FC' : 'XX Daniel Bedoya-New York City FC',
        'Daniel Steres-LA Galaxy' : 'Daniel Steres-Los Angeles Galaxy',
        'Danilo Silva-Los Angeles Football Club' : 'Danilo Silva-Los Angeles FC',
        'Danny Leyva-Seattle Sounders FC' : 'Danny Leyva-Tacoma Defiance',
        'Dave Romney-LA Galaxy' : 'Dave Romney-Los Angeles Galaxy',
        'David Bingham-LA Galaxy' : 'David Bingham-Los Angeles Galaxy',
        'David Norman Jr.-Vancouver Whitecaps FC' : 'XX David Norman Jr.-Vancouver Whitecaps FC',
        'David Ochoa-Real Salt Lake' : 'XX David Ochoa-Real Salt Lake',
        'Dax McCarty-Chicago Fire' : 'Dax Mccarty-Chicago Fire',
        'Dayne St. Clair-Minnesota United FC' : 'Dayne St Clair-Forward Madison FC',
        'Dejan Jakovic-Los Angeles Football Club' : 'XX Dejan Jakovic-Los Angeles Football Club',
        'DeJuan Jones-New England Revolution' : 'Dejuan Jones-New England Revolution',
        'Derrick Etienne Jr.-FC Cincinnati' : 'Derrick Etienne-FC Cincinnati',
        'Diedie Traore-LA Galaxy' : 'Diedie Traore-Los Angeles Galaxy II',
        'Diego Palacios-Los Angeles Football Club' : 'Diego Palacios-Los Angeles FC',
        'Diego Polenta-LA Galaxy' : 'Diego Polenta-Los Angeles Galaxy',
        'Diego Rossi-Los Angeles Football Club' : 'Diego Rossi-Los Angeles FC',
        'Dion Pereira-Atlanta United FC' : 'Dion Pereira-Atlanta United 2',
        'Donny Toia-Real Salt Lake' : 'Donny Toia-Real Salt Lake City',
        'Douglas Martinez-Real Salt Lake' : 'Douglas Martinez-Real Salt Lake City',
        'Earl Edwards Jr.-D.C. United' : 'Earl Edwards Jr -Loudoun United FC',
        'Eddie Segura-Los Angeles Football Club' : 'Eddie Segura-Los Angeles FC',
        'Eduard Atuesta-Los Angeles Football Club' : 'Eduard Atuesta-Los Angeles FC',
        'Edward Opoku-Columbus Crew SC' : 'XX Edward Opoku-Columbus Crew SC',
        'Efrain Alvarez-LA Galaxy' : 'Efrain Alvarez-Los Angeles Galaxy',
        'Elliot Collier-Chicago Fire' : 'Emil Cuello-Los Angeles Galaxy II',
        'Ema Twumasi-FC Dallas' : 'XX Ema Twumasi-FC Dallas',
        'Emery Welshman-FC Cincinnati' : 'XX Emery Welshman-FC Cincinnati',
        'Emil Cuello-LA Galaxy' : 'XX Emil Cuello-LA Galaxy',
        'Eric Bird-Houston Dynamo' : 'Eric Bird-Rio Grande Valley FC Toros',
        'Eric Calvillo-San Jose Earthquakes' : 'Eric Calvillo-Reno 1868 FC',
        'Eric Dick-Sporting Kansas City' : 'Eric Dick-Swope Park Rangers',
        'Erik Holt-Real Salt Lake' : 'Erik Holt-Real Monarchs SLC',
        'Erik McCue-Houston Dynamo' : 'Erik Mccue-Rio Grande Valley FC Toros',
        'Eryk Williamson-Portland Timbers' : 'Eryk Williamson-Portland Timbers 2',
        'Ethan Zubak-LA Galaxy' : 'Ethan Zubak-Los Angeles Galaxy II',
        'Evan Louro-New York Red Bulls' : 'Evan Louro-New York Red Bulls II',
        'Everton Luiz-Real Salt Lake' : 'Everton Luiz-Real Salt Lake City',
        'Favio Alvarez-LA Galaxy' : 'Favio Alvarez-Los Angeles Galaxy',
        'Felipe Gutiérrez-Sporting Kansas City' : 'Felipe Gutierrez-Sporting Kansas City',
        'Felipe Hernandez-Sporting Kansas City' : 'Felipe Hernandez-Swope Park Rangers',
        'Felipe-D.C. United' : 'Felipe Martins-D.C. United',
        'Forrest Lasso-FC Cincinnati' : 'XX Forrest Lasso-FC Cincinnati',
        'Foster Langsdorf-Portland Timbers' : 'Foster Langsdorf-Portland Timbers 2',
        'Francis Atuahene-FC Dallas' : 'Francis Atuahene-Austin Bold FC',
        'Gabriel Somi-New England Revolution' : 'XX Gabriel Somi-New England Revolution',
        'Gary Mackay-Steven-New York City FC' : 'Gary Mackay Steven-New York City FC',
        'Gaston Sauro-Columbus Crew SC' : 'XX Gaston Sauro-Columbus Crew SC',
        'Gedion Zelalem-Sporting Kansas City' : 'Gedion Zelalem-Swope Park Rangers',
        'George Bello-Atlanta United FC' : 'George Bello-Atlanta United 2',
        'Gerso Fernandes-Sporting Kansas City' : 'Gerso-Sporting Kansas City',
        'Giancarlo Gonzalez-LA Galaxy' : 'Giancarlo Gonzalez-Los Angeles Galaxy',
        'Gianluca Busio-Sporting Kansas City' : 'Gianluca Busio-Swope Park Rangers',
        'Gilbert Fuentes-San Jose Earthquakes' : 'Gilbert Fuentes-Reno 1868 FC',
        'XX Gonzalo Martinez-Atlanta United FC' : 'Gonzalo Martinez-Atlanta United FC',
        'Gordon Wild-D.C. United' : 'Gordon Wild-Loudoun United FC',
        'Graham Smith-Sporting Kansas City' : 'Graham Smith-Swope Park Rangers',
        'Grant Lillard-Chicago Fire' : 'Grant Lillard-Lansing Ignite FC',
        'Gregory van der Wiel-Toronto FC' : 'XX Gregory van der Wiel-Toronto FC',
        'Griffin Yow-D.C. United' : 'Griffin Yow-Loudoun United FC',
        'Handwalla Bwana-Seattle Sounders FC' : 'Handwalla Bwana-Tacoma Defiance',
        'Harry Novillo-Montreal Impact' : 'XX Harry Novillo-Montreal Impact',
        'Hassan Ndam-FC Cincinnati' : 'XX Hassan Ndam-FC Cincinnati',
        'Henry Wingo-Seattle Sounders FC' : 'XX Henry Wingo-Seattle Sounders FC',
        'Hugo Arellano-LA Galaxy' : 'Hugo Arellano-Orange County SC',
        'Inbeom Hwang-Vancouver Whitecaps FC' : 'In Beom Hwang-Vancouver Whitecaps FC',
        'Isaac Angking-New England Revolution' : 'Ismael Tajouri Shradi-New York City FC',
        'Ismael Tajouri-Shradi-New York City FC' : 'XX Ismael Tajouri-Shradi-New York City FC',
        'Jacob Akanyirige-San Jose Earthquakes' : 'Jacob Akanyirige-Reno 1868 FC',
        'Jasser Khmiri-Vancouver Whitecaps FC' : 'Jasser Khemiri-Vancouver Whitecaps FC',
        'Javi Perez-Los Angeles Football Club' : 'Javi Perez-Los Angeles FC',
        'Jaylin Lindsey-Sporting Kansas City' : 'Jaylin Lindsey-Swope Park Rangers',
        'Jean-Christophe Koffi-New York Red Bulls' : 'Jean Christophe Koffi-New York Red Bulls II',
        'Jeff Caldwell-New York City FC' : 'XX Jeff Caldwell-New York City FC',
        'Jefferson Savarino-Real Salt Lake' : 'Jefferson Savarino-Real Salt Lake City',
        'Jimmy McLaughlin-FC Cincinnati' : 'Jimmy Mclaughlin-FC Cincinnati',
        'Jimmy Ockford-San Jose Earthquakes' : 'XX Jimmy Ockford-San Jose Earthquakes',
        'JJ Williams-Columbus Crew SC' : 'Jj Williams-Birmingham Legion FC',
        'Joao Plata-Real Salt Lake' : 'Joao Plata-Real Salt Lake City',
        'Joe Corona-LA Galaxy' : 'Joe Corona-Los Angeles Galaxy',
        'Johan Blomberg-Colorado Rapids' : 'XX Johan Blomberg-Colorado Rapids',
        'Jon Bakero-Toronto FC' : 'XX Jon Bakero-Toronto FC',
        'Jon Gallagher-Atlanta United FC' : 'XX Jon Gallagher-Atlanta United FC',
        'Jonathan Campbell-Seattle Sounders FC' : 'Jonathan Campbell-Tacoma Defiance',
        'Jonathan dos Santos-LA Galaxy' : 'Jonathan Dos Santos-Los Angeles Galaxy',
        'XX Jordan Allen-Real Salt Lake City' : 'Jordan Allen-Real Salt Lake City',
        'Jordan Harvey-Los Angeles Football Club' : 'Jordan Harvey-Los Angeles FC',
        'Jordy Delem-Seattle Sounders FC' : 'Jordy Delem-Tacoma Defiance',
        'Jorge Villafaña-Portland Timbers' : 'Jorge Villafana-Portland Timbers',
        'Jorgen Skjelvik-LA Galaxy' : 'Jorgen Skjelvik-Los Angeles Galaxy',
        'Joe Gyau-FC Cincinnati' : 'Joseph Claude Gyau-FC Cincinnati',
        'Josh Perez-Los Angeles Football Club' : 'Joshua Perez-Phoenix Rising FC',
        'JT Marcinkowski-San Jose Earthquakes' : 'Jt Marcinkowski-Reno 1868 FC',
        'Jose Hernandez-Atlanta United FC' : 'XX Jose Hernandez-Atlanta United FC',
        'Josue Colman-Orlando City SC' : 'XX Josue Colman-Orlando City SC',
        'Juan Pablo Torres-New York City FC' : 'Juan Torres-New York City FC',
        'Julian Araujo-LA Galaxy' : 'Julian Araujo-Los Angeles Galaxy',
        'Julian Dunn-Toronto FC' : 'Julian Dunn Johnson-Toronto FC',
        'Julian Vazquez-Real Salt Lake' : 'Julian Vazquez-Real Monarchs SLC',
        'Juninho-LA Galaxy' : 'Juninho-Los Angeles Galaxy',
        'Justen Glad-Real Salt Lake' : 'Justen Glad-Real Salt Lake City',
        'Justin Dhillon-Seattle Sounders FC' : 'Justin Dhillon-Tacoma Defiance',
        'Justin Portillo-Real Salt Lake' : 'Justin Portillo-Real Monarchs SLC',
        'Justin Rennicks-New England Revolution' : 'XX Justin Rennicks-New England Revolution',
        'Justin Vom Steeg-LA Galaxy' : 'Justin Vom Steeg-Los Angeles Galaxy II',
        'Kim Kee-hee-Seattle Sounders FC' : 'Kee Hee Kim-Seattle Sounders FC',
        'Kelyn Rowe-Real Salt Lake' : 'Kelyn Rowe-Real Salt Lake City',
        'Kendall McIntosh-Portland Timbers' : 'Kendall Mcintosh-Portland Timbers',
        'Kenny Saief-FC Cincinnati' : 'XX Kenny Saief-FC Cincinnati',
        'Kevin Partida-San Jose Earthquakes' : 'Kevin Partida-Reno 1868 FC',
        'Kyle Beckerman-Real Salt Lake' : 'Kyle Beckerman-Real Salt Lake City',
        'Kyle Duncan-New York Red Bulls' : 'Kyle Duncan-New York Red Bulls II',
        'Lagos Kunga-Atlanta United FC' : 'XX Lagos Kunga-Atlanta United FC',
        'Lamar Batista-Los Angeles Football Club' : 'Lamar Batista-FC Tucson',
        'Latif Blessing-Los Angeles Football Club' : 'Latif Blessing-Los Angeles FC',
        'Lee Nguyen-Los Angeles Football Club' : 'Lee Nguyen-Los Angeles FC',
        'Logan Gdula-FC Cincinnati' : 'XX Logan Gdula-FC Cincinnati',
        'Lucas Melano-Portland Timbers' : 'XX Lucas Melano-Portland Timbers',
        'Lucas Venuto-Vancouver Whitecaps FC' : 'XX Lucas Venuto-Vancouver Whitecaps FC',
        'Luis Alberto Caicedo-New England Revolution' : 'Luis Caicedo-New England Revolution',
        'Luis Arriaga-Real Salt Lake' : 'Luis Arriaga-Real Monarchs SLC',
        'Luiz Fernando-Atlanta United FC' : 'Luiz Fernando Nascimento-Atlanta United 2',
        'Luke Mulholland-Real Salt Lake' : 'Luke Mulholland-Real Monarchs SLC',
        'Maikel van der Werff-FC Cincinnati' : 'Maikel Van Der Werff-FC Cincinnati',
        'Marcelo Silva-Real Salt Lake' : 'Marcelo Silva-Real Salt Lake City',
        'Marco Farfan-Portland Timbers' : 'Marco Farfan-Portland Timbers 2',
        'Marcus Epps-New York Red Bulls' : 'XX Marcus Epps-New York Red Bulls',
        'Mark McKenzie-Philadelphia Union' : 'Mark Mckenzie-Bethlehem Steel FC',
        'Mark-Anthony Kaye-Los Angeles Football Club' : 'Mark Anthony Kaye-Los Angeles FC',
        'Marvin Loria-Portland Timbers' : 'Marvin Loria-Portland Timbers 2',
        'Mason Stajduhar-Orlando City SC' : 'XX Mason Stajduhar-Orlando City SC',
        'Mason Toye-Minnesota United FC' : 'Mason Toye-Forward Madison FC',
        'Mathias Jorgensen-New York Red Bulls' : 'Mathias Jorgensen-New York Red Bulls II',
        'Matt Bersano-San Jose Earthquakes' : 'Matt Bersano-Reno 1868 FC',
        'Matt Freese-Philadelphia Union' : 'Matt Freese-Bethlehem Steel FC',
        'Matt Hundley-Colorado Rapids' : 'Matt Hundley-Colorado Springs Switchbacks FC',
        'Matt Lampson-LA Galaxy' : 'Matt Lampson-Los Angeles Galaxy',
        'Matthew Real-Philadelphia Union' : 'Matthew Real-Bethlehem Steel FC',
        'Maximiliano Moralez-New York City FC' : 'Maxi Moralez-New York City FC',
        'Michael Amir Murillo-New York Red Bulls' : 'Michael Murillo-New York Red Bulls',
        'Michael Nelson-Houston Dynamo' : 'Michael Nelson-Rio Grande Valley FC Toros',
        'Michael Salazar-Houston Dynamo' : 'Michael Salazar-Rio Grande Valley FC Toros',
        'Michee Ngalina-Philadelphia Union' : 'Michee Ngalina-Bethlehem Steel FC',
        'Micheal Azira-Chicago Fire' : 'Mike Azira-Chicago Fire',
        'Mikey Ambrose-Atlanta United FC' : 'Mikey Ambrose-Atlanta United 2',
        'Mo Adams-Atlanta United FC' : 'Mo Adams-Atlanta United 2',
        'Modou Jadama-Portland Timbers' : 'Modou Jadama-Portland Timbers 2',
        'Mohamed El-Munir-Los Angeles Football Club' : 'Mohamed El Munir-Los Angeles FC',
        'Moises Hernandez-FC Dallas' : 'Moses Nyeman-Loudoun United FC',
        'Nedum Onuoha-Real Salt Lake' : 'Nedum Onuoha-Real Salt Lake City',
        'Nazmi Albadawi-FC Cincinnati' : 'XX Nazmi Albadawi-FC Cincinnati',
        'Nemanja Nikolic-Chicago Fire' : 'Nemanja Nikolics-Chicago Fire',
        'Nick Besler-Real Salt Lake' : 'Nick Besler-Real Salt Lake City',
        'Nick DeLeon-Toronto FC' : 'Nick Deleon-Toronto FC',
        'Nick Rimando-Real Salt Lake' : 'Nick Rimando-Real Salt Lake City',
        'Nicolas Gaitan-Chicago Fire' : 'Nico Gaitan-Chicago Fire',
        'Nicolás Lodeiro-Seattle Sounders FC' : 'Nicolas Lodeiro-Seattle Sounders FC',
        'Niki Jackson-Colorado Rapids' : 'Niki Jackson-Charlotte Independence',
        'Niko Hamalainen-Los Angeles Football Club' : 'XX Niko Hamalainen-Los Angeles Football Club',
        'Noble Okello-Toronto FC' : 'Noble Okello-Toronto FC II',
        'Nouhou Tolo-Seattle Sounders FC' : 'Nouhou-Tacoma Defiance',
        'Olivier Mbaizo-Philadelphia Union' : 'Olivier Mbaizo-Bethlehem Steel FC',
        'Omar Browne-Montreal Impact' : 'XX Omar Browne-Montreal Impact',
        'Pablo Aranguiz-FC Dallas' : 'XX Pablo Aranguiz-FC Dallas',
        'Pablo Ruiz-Real Salt Lake' : 'XX Pablo Ruiz-Real Salt Lake',
        'Pablo Sisniega-Los Angeles Football Club' : 'Pablo Sisniega-Los Angeles FC',
        'Patrick Okonkwo-Atlanta United FC' : 'Patrick Okonkwo-Atlanta United 2',
        'PC-Vancouver Whitecaps FC' : 'Pctm-Vancouver Whitecaps FC',
        'Perry Kitchen-LA Galaxy' : 'Perry Kitchen-Los Angeles Galaxy',
        'Peter-Lee Vassell-Los Angeles Football Club' : 'XX Peter-Lee Vassell-Los Angeles Football Club',
        'Phillip Ejimadu-Los Angeles Football Club' : 'XX Phillip Ejimadu-Los Angeles Football Club',
        'Pierre Da Silva-Orlando City SC' : 'XX Pierre Da Silva-Orlando City SC',
        'Pity Martinez-Atlanta United FC' : 'XX Pity Martinez-Atlanta United FC',
        'Renzo Zambrano-Portland Timbers' : 'XX Renzo Zambrano-Portland Timbers',
        'Renzo Zambrano-Portland Timbers' : 'Renzo Zambrano-Portland Timbers 2',
        'RJ Allen-Philadelphia Union' : 'R J Allen-Philadelphia Union',
        'Rodolfo Zelaya-Los Angeles Football Club' : 'XX Rodolfo Zelaya-Los Angeles Football Club',
        'Rolf Feltscher-LA Galaxy' : 'Rolf Feltscher-Los Angeles Galaxy',
        'Romain Alessandrini-LA Galaxy' : 'Romain Alessandrini-Los Angeles Galaxy',
        'Román Torres-Seattle Sounders FC' : 'Roman Torres-Tacoma Defiance',
        'Romario Ibarra-Minnesota United FC' : 'XX Romario Ibarra-Minnesota United FC',
        'Ronaldo Peña-Houston Dynamo' : 'Ronaldo Pena-Rio Grande Valley FC Toros',
        'Ryan Telfer-Toronto FC' : 'Ryan Telfer-York9 FC',
        'Saad Abdul-Salaam-Seattle Sounders FC' : 'Saad Abdul Salaam-Tacoma Defiance',
        'Sam Johnson-Real Salt Lake' : 'Sam Johnson-Real Salt Lake City',
        'Sam Junqua-Houston Dynamo' : 'Sam Junqua-Rio Grande Valley FC Toros',
        'Sam Raben-Colorado Rapids' : 'Sam Raben-Colorado Springs Switchbacks FC',
        'Santiago Patiño-Orlando City SC' : 'Santiago Patino-Orlando City SC',
        'Sean Nealis-New York Red Bulls' : 'Sean Nealis-New York Red Bulls II',
        'Sebastian Lletget-LA Galaxy' : 'Sebastian Lletget-Los Angeles Galaxy',
        'Sebastian Saucedo-Real Salt Lake' : 'Sebastian Saucedo-Real Salt Lake City',
        'Servando Carrasco-LA Galaxy' : 'Servando Carrasco-Los Angeles Galaxy',
        'Shaft Brewer Jr.-Los Angeles Football Club' : 'XX Shaft Brewer Jr.-Los Angeles Football Club',
        'Shane O\'Neill-Orlando City SC' : 'Shane Oneill-Orlando City SC',
        'Siad Haji-San Jose Earthquakes' : 'Siad Haji-Reno 1868 FC',
        'Stefan Cleveland-Chicago Fire' : 'Stefan Cleveland-Lansing Ignite FC',
        'Steven Birnbaum-D.C. United' : 'Steve Birnbaum-D.C. United',
        'Steven Beitashour-Los Angeles Football Club' : 'Steven Beitashour-Los Angeles FC',
        'Tate Schmitt-Real Salt Lake' : 'Tate Schmitt-Real Monarchs SLC',
        'Tom Barlow-New York Red Bulls' : 'Tom Barlow-New York Red Bulls II',
        'Tomas Hilliard-Arce-LA Galaxy' : 'Tomas Hilliard Arce-Los Angeles Galaxy II',
        'Terrence Boyd-Toronto FC' : 'XX Terrence Boyd-Toronto FC',
        'Thomas McNamara-Houston Dynamo' : 'Tommy Mcnamara-Houston Dynamo',
        'Thomas Meilleur-Giguere-Montreal Impact' : 'XX Thomas Meilleur-Giguere-Montreal Impact',
        'Tommy McCabe-FC Cincinnati' : 'XX Tommy McCabe-FC Cincinnati',
        'Tony Beltran-Real Salt Lake' : 'XX Tony Beltran-Real Salt Lake',
        'Trey Muse-Seattle Sounders FC' : 'Trey Muse-Tacoma Defiance',
        'Tristan Blackmon-Los Angeles Football Club' : 'Tristan Blackmon-Los Angeles FC',
        'Tyler Deric-Houston Dynamo' : 'Tyler Deric-Rio Grande Valley FC Toros',
        'Tyler Freeman-Sporting Kansas City' : 'Tyler Freeman-Swope Park Rangers',
        'Tyler Miller-Los Angeles Football Club' : 'Tyler Miller-Los Angeles FC',
        'Uriel Antuna-LA Galaxy' : 'Uriel Antuna-Los Angeles Galaxy',
        'Vako-San Jose Earthquakes' : 'Valeri Qazaishvili-San Jose Earthquakes',
        'Vincent Bezecourt-New York Red Bulls' : 'Vincent Bezecourt-New York Red Bulls II',
        'Walker Zimmerman-Los Angeles Football Club' : 'Walker Zimmerman-Los Angeles FC',
        'Wan Kuzain Wan Kamal-Sporting Kansas City' : 'Wan Kuzain-Swope Park Rangers',
        'Will Bruin-Seattle Sounders FC' : 'Will Bruin-Tacoma Defiance',
        'Wyatt Omsberg-Minnesota United FC' : 'Wyatt Omsberg-Forward Madison FC',
        'Yohan Croizet-Sporting Kansas City' : 'Zac Macmath-Vancouver Whitecaps FC',
        'Zac MacMath-Vancouver Whitecaps FC' : 'XX Zac MacMath-Vancouver Whitecaps FC',
        'Zachary Brault-Guillard-Montreal Impact' : 'Zachary Brault Guillard-Montreal Impact',
        'Zachary Herivaux-New England Revolution' : 'Zachary Herivaux-Birmingham Legion FC',
        'Zack Steffen-Columbus Crew SC' : 'XX Zack Steffen-Columbus Crew SC',
        'Zakaria Diallo-Montreal Impact' : 'XX Zakaria Diallo-Montreal Impact',
        'Zlatan Ibrahimovic-LA Galaxy' : 'Zlatan Ibrahimovic-Los Angeles Galaxy',
        'Zoltan Stieber-D.C. United' : 'XX Zoltan Stieber-D.C. United'  , 'nan': np.nan      }

df_full = df_full.reset_index(drop=True) 


for index in df_full.index:
    value = df_full.loc[index,'names_values']
    name = df_full.loc[index,'names_full']
    if value is np.nan:
        try:
            new_value = naming_fix2[name]
            df_full.loc[index,'names_values'] = new_value
        except:
            print('Check row number: ',index)





df_final = pd.merge(df_full, df_values, on='names_values')

list(df_final.columns)

redunt = ['Club_x','POS', 'name_x', 'Position', 'names_stats_x', 'names_fantasy',  'name_y',
 'team_y', 'position', 'Club_y', 'player_index', 'names_stats_y', 'names_full_x', 'names_values',
 'League_2Yellow', 'League_Assist', 'League_Games', 'League_Goals',  'League_Red', 'League_Yellow',
 'League_stats', 'Social media:', 'player_id_y', 'player_name', 'transf_history', 'url', 'names_full_y']

df_final = df_final.drop(redunt,axis=1)


df_final.loc[:,'rating'] = df_final.loc[:,'rating'].apply(lambda x: x.replace('$','').replace('K','').replace(',','.'))


df_final.to_csv('MLS2019_tableau_V2.csv',sep=',',index =False)


