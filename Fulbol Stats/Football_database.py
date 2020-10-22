from selenium import webdriver
import time
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

##############################################################################################################
##########################################################
# Reading files

driver = webdriver.Chrome('C:\chromedriver')
url = 'https://www.football-data.co.uk/data.php'
driver.get(url)

for k in range(1,3):
    for j in range(1,20):
        try:
            xpath1 = '/html/body/table[5]/tbody/tr[2]/td[3]/table['+str(k)+']/tbody/tr['+str(j)+']/td[2]'
            driver.find_element_by_xpath(xpath1).click()
            url1 = driver.current_url
            for i in range(2,150):
                try:
                    xpath2 = '/html/body/table[5]/tbody/tr[2]/td[3]/a['+str(i)+']'
                    driver.find_element_by_xpath(xpath2).click()   
                    driver.get(url1)
                except:
                    #print(i,' not found')
                    continue
                
            #time.sleep(5) 
            driver.get(url)
            
        except:
            #print(j,' not found')
            continue
driver.close()

del xpath1, xpath2, url, url1, i,j,k
 
##########################################################
##############################################################################################################


filescsv = []
for file in os.listdir():
    if file.endswith(".csv"):
        filescsv.append(file)   
    
    
filesxls = []
for file in os.listdir():
    if file.endswith(".xlsx"):
        filesxls.append(file)   
     
del file        
             
##############################################################################################################
##########################################################
# CLEANING FILES

for file in filescsv:
    try:
        df1 = pd.read_csv(file,sep=';', header=None, engine='python')
        
        columns = df1.iloc[:,0].apply( lambda x : x.count(',') ).max()
        df1.iloc[:,0] = df1.iloc[:,0].apply(lambda x:   x + (','*( columns - x.count(',') ) ))
        header = df1.iloc[0,0]
        header_list = header.split (",")
        df1[header_list] = df1[0].str.split(pat=',',expand = True)
        df1.columns = df1.iloc[0,:]
        df1 = df1.iloc[1:,1:]
        df1.to_csv(  file,index=False)  
    except:
        print(file,' error ',sys.exc_info()[1])


del df1, header_list, header, columns, file
##########################################################
##############################################################################################################



##############################################################################################################
##########################################################
# JOINING FILES
        
filesE0 = []
for file in os.listdir():
    if file.endswith(".csv"):
        filesE0.append(file)  

  
df = pd.DataFrame()   



for file in filesE0:
    try:
        df2 = pd.read_csv(file,sep=',', engine='python')
        df3 = df2.iloc[0,:]
        df = df.append(df3)
    except:
        print(file,' error ',sys.exc_info()[1])

df = df.iloc[0,:]

for file in filesE0:
    try:
        df2 = pd.read_csv(file,sep=',', engine='python')
        df = df.append(df2)
    except:
        print(file,' error ',sys.exc_info()[1])








del df2,df3, file, filesE0, filescsv


df = df.drop_duplicates()
df.to_csv('all_together.csv' ,index=False) 

df1 = pd.read_csv('all_together.csv',sep=',', header='infer', engine='python')

        
##########################################################
##############################################################################################################
#dfx = df.copy()



# Unifying name columns
replace_list = [    ['FTAG','AG'], 
                    #['AwayTeam','AT'], 
                    ['AwayTeam','Away'],
                    ['HomeTeam','Home'],
                    #['HomeTeam','HT'],
                    ['FTHG','HG'],
                    ['PSA','PA'],
                    ['PSD','PD'],
                    ['PSH','PH']]


for element in replace_list:
    print('filling nulls in', element[0], 'with' , element[1])
    cond = df1.loc[:,element[0]].isna()
    df1.loc[cond,element[0]] = df1.loc[cond,element[1]]
    df1 = df1.drop(element[1],axis=1)



cond = df1.loc[:,'AwayTeam'].notna()
df1 =  df1.loc[cond,:]


cond = df1.loc[:,'Div'].isna() 
df1.loc[cond,'Div'] = df1.loc[cond,'Country'].apply(lambda x : x[:1]+'1' )


dfR = df1.loc[:,('Country','Div')].drop_duplicates()

replace_list = [    ['E','England'], ['F','France'],['S','Spain'],
                    ['B','Belgium'], ['I','Italy'],['T','Turkey'],
                    ['G','Greece'],['N','Netherlands'],['P','Portugal']]

for element in replace_list:
    cond1 = df1.loc[:,'Div'].apply(lambda x : x.startswith(element[0]) )
    cond2 = df1.loc[:,'Country'].isna() 
    df1.loc[cond1&cond2,'Country'] = element[1]


del cond, cond1,cond2,replace_list, element, dfR

##############################################################################################################
##########################################################
# SELECTING COLUMNS

columns = list(df1.columns)

selection = ['AC','AF','AHW','AO','AR','AS','AST','AY','AwayTeam',
             'HC','HF','HHW','HO','HR','HS','HST','HY','HomeTeam',
             'P<2.5','P>2.5','PSA','PSD','PSH','PC<2.5','PC>2.5','PCSA','PCSD','PCSH',
             'B365<2.5','B365>2.5','B365SA','B365SD','B365SH','B365C<2.5','B365C>2.5','B365CSA','B365CSD','B365CSH',
             'Attendance','FTAG','FTHG','FTR','HTAG','HTHG','HTR','Referee','Time','Date',
             'Div','Country','Season','League','Res']

df1 = df1.loc[:,selection]

del columns, selection
##########################################################
##############################################################################################################


##############################################################################################################
##########################################################
# DEEP CLEANING - CONTRY - LEAGUE - DATE

###############################################################################
# Country League

dfR = df1.loc[:,('Country','Div','League')].drop_duplicates()

league ={ 'E0':'Premier League',
          'E1':'Championship',
          'E2':'League 1',
          'E3':'League 2',
          'EC':'Conference',
          'B1':'Jupiler League',
          'G1':'Ethniki Katigoria',
          'J0':'J-League',
          'F0':'Veikkausliiga',
          'I0':'Premier Division',
          'F1':'Le Championnat', 
          'F2':'Division 2',
          'I1':'Serie A',
          'I2':'Serie B',
          'N1':'KPN Eredivisie',
          'P1':'Liga I',
          'SP1':'La Liga',
          'SP2':'La Liga SD',
          'T1' :'Ligi 1'
          }

cond = df1.loc[:,'League'].isna()
df1.loc[cond,'League'] = df1.loc[cond,'Div'].map(league)


dfR = df1.loc[:,('Country','Div','League')].drop_duplicates()

df1.loc[:,'League'] = df1.loc[:,'League'].apply(lambda x: x.strip())

###############################################################################
# Date

df1.loc[:,'Date'] = pd.to_datetime(df1.loc[:,'Date'])

###############################################################################
# Season

cond = df1.loc[:,'Season'].isna()

df1.loc[cond,'Season'] = df1.loc[cond,'Date'].apply(lambda x: x.strftime('%Y') + '-' +  str(int( np.ceil( float(x.strftime('%m') )/6)))  )

###############################################################################
# Res

cond = df1.loc[:,'Res'].isna()

df1.loc[:,'Dif_gol'] = df1.loc[:,'FTHG'] - df1.loc[:,'FTAG']

cond = df1.loc[:,'Dif_gol'] == 0
df1.loc[cond,'FTR'] = 'D'

cond = df1.loc[:,'Dif_gol'] > 0
df1.loc[cond,'FTR'] = 'H'

cond = df1.loc[:,'Dif_gol'] < 0
df1.loc[cond,'FTR'] = 'A'


del cond, league, dfR
##########################################################
##############################################################################################################



##############################################################################################################
##########################################################
# Only final score




selection = ['AwayTeam','HomeTeam',
             'FTAG','FTHG','FTR','Time','Date',
             'Div','Country','Season','League','Res']

df2 = df1.loc[:,selection]

del selection



##########################################################
##############################################################################################################

A = ''
B = ''

x = df2.loc[:,A]
y = df2.loc[:,B]



columns = list(df2.columns)

for col in columns:
    x = df2.loc[:,col]
    plt.hist(x)
    plt.title(col )
    plt.show()


