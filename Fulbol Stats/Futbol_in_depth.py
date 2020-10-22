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
    
    df0 = df0.iloc[2:,1:]
    
    team1 = df0.loc[:,('team1','B','C')]
    team1 = team1.pivot(index='B', columns='C', values='team1')
    
    team2 = df0.loc[:,('team2','B','C')]
    team2 = team2.pivot(index='B', columns='C', values='team2')
    
    players = team1.append(team2).reset_index(drop=True)

    return teams, players

def read_json(path):
    with open(path, 'r', encoding= "utf-8") as myfile:
        data=myfile.read()
    obj = json.loads(data)
    return obj

######################################################################################################3

game = 7570   

path = 'lineups/' + str(game) + '.json'
teams, players = players_from_json(path)
del path

players.index = players.loc[:,'player_id']
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



columns = list(df.columns)

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


del team1

ball_move.loc[:,'duration'] = ball_move.loc[:,'duration'].fillna(0)


ball_move = ball_move.drop([ 'carry/end_location/0','carry/end_location/1','index',
                            'pass/end_location/0','pass/end_location/1',
                            'shot/end_location/0','shot/end_location/1','shot/end_location/2',\
                            'goalkeeper/end_location/0','goalkeeper/end_location/1'],axis=1)



ball_move.to_csv('ball_move.csv' ,index=False) 


        