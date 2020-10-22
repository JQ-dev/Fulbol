# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 12:25:26 2019

@author: admin
"""


import json
import pandas as pd
import time
import numpy as np


# Recurrently Reduce dict

def jsonflatlist_to_columns(json_flat):
    # list of columns
    columns = {}
    for dict_row in json_flat:
        for key in dict_row.keys():
            columns[key] = None      
    column_list = list(columns.keys())      
    return column_list



def jsonflatlist_to_df(json_flat,selected_columns,all_columns=False):
    # list of columns
    columns = {}
    for dict_row in json_flat:
        for key in dict_row.keys():
            columns[key] = None
    df = pd.DataFrame.from_dict(columns, orient='index').T
    if all_columns == False:
        df = df.loc[:,selected_columns]
    # combining rows
    for dict_row in json_flat:
        # dict_row = json_flat[0]
        df_row = pd.DataFrame.from_dict(dict_row, orient='index').T
        if all_columns == False:
            df_row = df_row.loc[:,selected_columns]
        df = df.append(df_row)
    return df


def json_to_json_flat(json_list):
    new_json = []
    for element in json_list:
        len1 = -1
        len2 = -2
        while len1 != len2:
            len1 = len(element)
            element = split_dict(element)
            len2 = len(element)
        new_json.append(element)
    return new_json


def split_lists(element):
    new_element = {}
    keys = len(element) 
    for key in range(keys):
        new_element[str(key)] = element[key]
    return new_element
            

def split_dict(element):
    keys = list(element.keys()) 
    for key in keys:
        # key = keys[12]
        new_element = element[key]        
        if type(new_element) == list :  
            new_element = split_lists(new_element)        
        if type(new_element) == dict :     
            keys1 = list(new_element.keys())  
            for key1 in keys1:
                # key1 = keys1[0]
                new_key = key + '/' + key1 
                element[new_key] = new_element[key1]
            del element[key]              
    return element


def players_from_json(path):
    json_list = read_json(path)           
    json_flat = json_to_json_flat(json_list)
    df0 = jsonflatlist_to_df(json_flat,selected_columns=[],all_columns=True).T
    df0.columns = ['','team1','team2']
    df0.loc[:,''] = df0.index
    
    df0[['','B','C','D']] = df0.iloc[:,0].str.split(pat='/',expand = True)
    teams = pd.DataFrame()
    teams['name'] =  df0.loc['team_name',:]
    teams['id']   =  df0.loc['team_id',:]
    teams = teams.loc[('team1','team2'),('name','id')]
    
    df0.loc[:,'C'] = (df0.loc[:,'C']).where(df0.loc[:,'D'].isna() , (df0.loc[:,'C'] + '_' + df0.loc[:,'D']))
    df0 = df0.drop('D',axis=1)
    
    
    team1 = df0.loc[ df0.loc[:,'B'].notna() ,('team1','B','C') ]
    team1 = team1.pivot(index='B', columns='C', values='team1')
    
    team2 = df0.loc[:,('team2','B','C')]
    team2 = team2.loc[team2.loc[:,'B'].notna(),:]
    team2 = team2.pivot(index='B', columns='C', values='team2')
    
    players = team1.append(team2)   
    players = players.loc[ players.loc[:,'player_id'].notna() ,:]
    players.index = players.loc[:,'player_id']

    return teams, players


def read_json(path):
    with open(path, 'r', encoding= "utf-8") as myfile:
        data=myfile.read()
    obj = json.loads(data)
    return obj




def read_transform_and_save (file_list):
    
    All_the_games =[]
    count = 0
    for game in file_list:
        count += 1
        print('Reading json file:',game,'.',count,'of',len(file_list))
        #game = 8655   
        path = 'lineups/' + str(game) + '.json'
        teams, players = players_from_json(path)
        del path
        
        
        #players.index = players.loc[:,'player_id']
        players['short_name'] = players['player_name'].where( players['player_nickname'].isna(),players['player_nickname'] )
        players.loc[:,'short_name'] = players.loc[:,'short_name'].apply(lambda x : x.split(' ')[0][0] +' '+ x.split(' ')[-1])
        dict_players = players.loc[:,('short_name')].to_dict()
        
        path = 'events/' + str(game) + '.json'
        json_list = read_json(path)   
        json_flat = json_to_json_flat(json_list)
        column_list = jsonflatlist_to_columns(json_flat)
        
        selected_columns = []
        
        df = jsonflatlist_to_df(json_flat,selected_columns,all_columns=True)
        
        del selected_columns , json_flat, json_list, path, column_list
        
        
        df = df.fillna(np.nan)
        #df = df.loc[:,:]
        
        All_the_games.append(df)
        
    return All_the_games
        #df.to_csv('full_game.csv' ,index=False ) 


######################################################################################################3



WWC = 'matches/72/30.json'


file_list = []
matches = read_json(WWC)           
for match in matches:
    file_list.append( match['match_id']  )
del matches, match, WWC

WWCgame_list = read_transform_and_save(file_list)

WWC_data = pd.DataFrame()
for game in WWCgame_list:
    WWC_data = WWC_data.append(game)




MWC = 'matches/43/3.json'

file_list = []
matches = read_json(MWC)           
for match in matches:
    file_list.append( match['match_id']  )
del matches, match, MWC


MWCgame_list = read_transform_and_save(file_list)

MWC_data = pd.DataFrame()
for game in MWCgame_list:
    MWC_data = MWC_data.append(game)



# Saving files
#MWC_data.to_csv('MWC_data_full_game.csv' ,index=False ) 
#WWC_data.to_csv('WWC_data_full_game.csv' ,index=False ) 

del MWCgame_list, game, file_list























# CLEANING DATAFRAME
MWC_data2 = pd.read_csv('WWC_data_full_game.csv',sep=',')

# Creating tactics
columns = list(MWC_data2.columns)
id_columns = []
for col in columns:
    if ('tactics/' in col):
        id_columns.append(col)
MWC_data2 = MWC_data2.drop(id_columns,axis=1)


# Removing freeze frame
columns = list(MWC_data2.columns)
id_columns = []
for col in columns:
    if ('shot/freeze_frame/' in col):
        id_columns.append(col)
MWC_data2 = MWC_data2.drop(id_columns,axis=1)

# Removing ID duplicates
columns = list(MWC_data2.columns)
id_columns = []
for col in columns:
    if ('/id' in col) and ('player/id' not in col) and ('pass/recipient/id' not in col):
        id_columns.append(col)
MWC_data2 = MWC_data2.drop(id_columns,axis=1)

# Removing Related events
columns = list(MWC_data2.columns)
id_columns = []
for col in columns:
    if ('related_' in col):
        id_columns.append(col)
MWC_data2 = MWC_data2.drop(id_columns,axis=1)

MWC_data2 = MWC_data2.drop('id',axis=1)

C1 = (MWC_data2.loc[:,'location/0'] - MWC_data2.loc[:,'shot/end_location/0'])
C2 = (MWC_data2.loc[:,'location/1'] - MWC_data2.loc[:,'shot/end_location/1'])
H = (C1*C1 + C2*C2)**(0.5)
#S = MWC_data2.loc[:,'shot/lenght'] / MWC_data2.loc[:,'duration'] * (3.6)


MWC_data2['shot/lenght'] = H
#MWC_data2['shot/speed'] = S

C1 = (MWC_data2.loc[:,'location/0'] - MWC_data2.loc[:,'carry/end_location/0'])
C2 = (MWC_data2.loc[:,'location/1'] - MWC_data2.loc[:,'carry/end_location/1'])
H = (C1*C1 + C2*C2)**(0.5)
#S = MWC_data2.loc[:,'carry/lenght'] / MWC_data2.loc[:,'duration'] * (3.6)

MWC_data2['carry/lenght'] = H
#MWC_data2['carry/speed'] = S

#S = MWC_data2.loc[:,'pass/length'] / MWC_data2.loc[:,'duration'] * (3.6)
#MWC_data2['pass/speed'] = S

# Match name
#MWC_data2 = WWC_clean.copy()

MWC_data2.loc[:,'team2/name'] =  MWC_data2.loc[:,'team/name'].shift(-1)
MWC_data2.loc[:,'match'] = MWC_data2.loc[:,'team/name'] + ' - ' + MWC_data2.loc[:,'team2/name']

cond1 = MWC_data2.loc[:,'type/name'] == 'Starting XI'
cond2 = MWC_data2.loc[:,'team2/name'] != MWC_data2.loc[:,'team/name']
cond3 = MWC_data2.loc[:,'period'] == 1
cond = cond1 & cond2 & cond3
MWC_data2.loc[:,'match'] = MWC_data2.loc[:,'match'].where(cond , np.nan)

MWC_data2.loc[:,'match'] = MWC_data2.loc[:,'match'].fillna(method='ffill')

MWC_data2 = MWC_data2.drop('team2/name',axis=1)


del C1,C2,H,col,columns,id_columns,cond1,cond2,cond3,cond




#WWC_clean = MWC_data2.copy()
#WWC_clean.to_csv('WWC_data_games.csv' ,index=False ) 


#MWC_clean = MWC_data2.copy()
#MWC_clean.to_csv('MWC_data_games.csv' ,index=False ) 
del MWC_data2

MWC_clean = pd.read_csv('MWC_data_games.csv',sep=',')
WWC_clean = pd.read_csv('WWC_data_games.csv',sep=',')


# Only relevant - passes
columns = list(MWC_clean.columns)
id_columns = []
for col in columns:
    if ((('duration' in col) or ('goalkeeper/outcome' in col) or
        ('location/' in col)or ('pass/' in col) or ('goalkeeper/end_' in col) or
        ('player/' in col) or ('shot/' in col) or ('team/name' in col) or ('under_p' in col) or
        ('match' in col) or ('type/name' in col) or ('minute' in col) or ('period' in col)) and 
        ('carry' not in col) and ('foul' not in col) and ('duel' not in col) ):
        id_columns.append(col)
        
MWC_cleaner = MWC_clean.loc[:,id_columns]

list(MWC_cleaner.loc[:,'type/name'].drop_duplicates())

remove_type = [ 'Starting XI', 'Half Start', 'Carry', 'Pressure', 'Dribbled Past', 'Dribble', 'Duel',
 'Clearance', 'Ball Recovery', 'Block', 'Camera On', 'Dispossessed', 'Interception', 'Shield',
 'Miscontrol', 'Camera off', 'Foul Committed', 'Foul Won', 'Injury Stoppage', 'Player Off',
 'Player On', 'Half End', 'Substitution', 'Tactical Shift', '50/50', 'Bad Behaviour', 'Error',
 'Offside', 'Referee Ball-Drop', 'Own Goal For', 'Own Goal Against']
for type_name in remove_type:
    try:
        cond = MWC_cleaner.loc[:,'type/name'] != type_name
        MWC_cleaner = MWC_cleaner.loc[cond,:]
    except:
        pass

MWC_cleaner = MWC_cleaner.loc[MWC_cleaner.loc[:,'type/name'].notna(),:]



columns = list(WWC_clean.columns)
id_columns = []
for col in columns:
    if ((('duration' in col) or ('goalkeeper/outcome' in col) or
        ('location/' in col)or ('pass/' in col) or ('goalkeeper/end_' in col) or
        ('player/' in col) or ('shot/' in col) or ('team/name' in col) or ('under_p' in col) or
        ('match' in col) or ('type/name' in col) or ('minute' in col) or ('period' in col)) and 
        ('carry' not in col) and ('foul' not in col) and ('duel' not in col) ):
        id_columns.append(col)
        
WWC_cleaner = WWC_clean.loc[:,id_columns]

list(WWC_cleaner.loc[:,'type/name'].drop_duplicates())

remove_type = [  'Starting XI', 'Half Start', 'Carry', 'Pressure', 'Dribbled Past',
 'Dribble', 'Dispossessed', 'Duel', 'Miscontrol', 'Interception', 'Ball Recovery',
 'Block', 'Clearance', 'Foul Committed', 'Foul Won', 'Half End', 'Substitution',
 'Tactical Shift', 'Error', 'Injury Stoppage', 'Player Off', 'Player On', 'Shield',
 '50/50', 'Offside', 'Referee Ball-Drop', 'Own Goal Against', 'Own Goal For', 'Bad Behaviour']
for type_name in remove_type:
    try:
        cond = WWC_cleaner.loc[:,'type/name'] != type_name
        WWC_cleaner = WWC_cleaner.loc[cond,:]
    except:
        pass

WWC_cleaner = WWC_cleaner.loc[WWC_cleaner.loc[:,'type/name'].notna(),:]


########################


WWC_cleaner.to_csv('WWC_data_tableau.csv' ,index=False ) 

MWC_cleaner.to_csv('MWC_data_tableau.csv' ,index=False ) 

columns = list(MWC_pases.columns)

remove = ['duration', 'goalkeeper/end_location/0', 'goalkeeper/end_location/1', 'goalkeeper/outcome/name',
 'goalkeeper/type/name', 'minute', 'period', 'possession_team/name', 'shot/aerial_won',
 'shot/body_part/name', 'shot/deflected', 'shot/end_location/0', 'shot/end_location/1', 'shot/end_location/2', 'shot/first_time',
 'shot/follows_dribble', 'shot/key_pass_id', 'shot/one_on_one', 'shot/open_goal', 'shot/outcome/name', 'shot/redirect',
 'shot/statsbomb_xg', 'shot/technique/name', 'shot/type/name', 'shot/lenght']

MWC_pases = MWC_cleaner.drop(remove,axis=1)

MWC_pases = MWC_pases.loc[ MWC_pases.loc[:,'type/name'] == 'Pass' , : ]

remove = ['location/0', 'location/1', 'pass/aerial_won', 'pass/angle', 'pass/assisted_shot_id', 'pass/backheel',
 'pass/body_part/name', 'pass/cross', 'pass/cut_back', 'pass/deflected', 'pass/end_location/0', 'pass/end_location/1',
 'pass/goal_assist', 'pass/height/name', 'pass/miscommunication', 'pass/shot_assist', 'pass/switch', 'pass/technique/name',
 'pass/through_ball', 'type/name']

MWC_pases = MWC_pases.drop(remove,axis=1)




MWC_pases['to_pad'] = 1

temp = MWC_pases.copy()
temp['to_pad'] = 49

MWC_pases = MWC_pases.append(temp)
MWC_pases.to_csv('MWC_passes_tableau.csv' ,index=False ) 

'''

columns = list(df.columns)



for row in columns:
    splited_row = []
    splits = row.count('/')
    for i in range(splits-1):
        splited = row.split('/',1)
        splited_row.append(splited[i])
    
    
    multi_columns.append(splited)






ball_move = df.loc[:,('index','location/0','location/1','possession_team/name','player/id',
                      'timestamp','period','team/name', 'type/name','counterpress',
                      'carry/end_location/0','carry/end_location/1','pass/recipient/id',
                      'pass/outcome/name','pass/end_location/0','pass/end_location/1',
                      'goalkeeper/end_location/0','goalkeeper/end_location/1','goalkeeper/type/name',
                      'shot/end_location/0','shot/end_location/1','shot/end_location/2',
                      'duel/outcome/name','duel/type/name','duration','pass/length','pass/cross')]

ball_move.index = ball_move.loc[:,'index']  


ball_move = ball_move.replace('None',np.nan).fillna(np.nan)

ball_move = ball_move.loc[ ball_move.loc[:,'location/0'].notna(), : ]


ball_move.loc[:,'secs'] = ball_move.loc[:,'timestamp'].apply(lambda \
             x : int(x.split(':')[0])*3600+int(x.split(':')[1])*60+float(x.split(':')[2]))



ball_move.loc[:,'game_time'] = ball_move.loc[:,'timestamp'].apply(lambda \
             x : x.split(':')[1] + ':' + x.split(':')[2][:2] )


ball_move['player'] = ball_move.loc[:,'player/id'].map(dict_players)



ball_move.loc[:,'end_location/0'] = ball_move.loc[:,'carry/end_location/0']
ball_move.loc[:,'end_location/1'] = ball_move.loc[:,'carry/end_location/1']

cond = ball_move.loc[:,'end_location/0'].isna()
ball_move.loc[cond,'end_location/0'] = ball_move.loc[cond,'pass/end_location/0']
ball_move.loc[cond,'end_location/1'] = ball_move.loc[cond,'pass/end_location/1']

cond = ball_move.loc[:,'end_location/0'].isna()
ball_move.loc[cond,'end_location/0'] = ball_move.loc[cond,'shot/end_location/0']
ball_move.loc[cond,'end_location/1'] = ball_move.loc[cond,'shot/end_location/1']
ball_move.loc[cond,'end_location/2'] = ball_move.loc[cond,'shot/end_location/2']

cond = ball_move.loc[:,'end_location/0'].isna()
ball_move.loc[cond,'end_location/0'] = ball_move.loc[cond,'goalkeeper/end_location/0']
ball_move.loc[cond,'end_location/1'] = ball_move.loc[cond,'goalkeeper/end_location/1']

cond = ball_move.loc[:,'end_location/0'].isna()
ball_move.loc[cond,'end_location/0'] = ball_move.loc[cond,'location/0']
ball_move.loc[cond,'end_location/1'] = ball_move.loc[cond,'location/1']





team1 = ball_move.loc[:,'team/name'].iloc[0]


ball_move.loc[:,'location/0'] = ball_move.loc[:,'location/0']. \
                                where( ball_move.loc[:,'team/name']==team1 , \
                                120 - ball_move.loc[:,'location/0'] )

ball_move.loc[:,'location/1'] = ball_move.loc[:,'location/1']. \
                                where( ball_move.loc[:,'team/name']==team1 , \
                                80 - ball_move.loc[:,'location/1'] )

                                

ball_move.loc[:,'end_location/0'] = ball_move.loc[:,'end_location/0']. \
                                where( ball_move.loc[:,'team/name']==team1 , \
                                120 - ball_move.loc[:,'end_location/0'] )

ball_move.loc[:,'end_location/1'] = ball_move.loc[:,'end_location/1']. \
                                where( ball_move.loc[:,'team/name']==team1 , \
                                80 - ball_move.loc[:,'end_location/1'] )


del  team1, cond, df, game, columns

ball_move.loc[:,'duration'] = ball_move.loc[:,'duration'].fillna(0)


ball_move = ball_move.drop([ 'carry/end_location/0','carry/end_location/1','index',
                            'pass/end_location/0','pass/end_location/1',
                            'shot/end_location/0','shot/end_location/1','shot/end_location/2',\
                            'goalkeeper/end_location/0','goalkeeper/end_location/1'],axis=1)



ball_move.to_csv('ball_move.csv' ,index=False, ) 

'''
        