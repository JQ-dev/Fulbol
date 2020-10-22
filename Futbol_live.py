
from vpython import *
from random import *
import string
import numpy as np
import time 
import pandas as pd
import matplotlib.pyplot as plt

# canvas
def new_screen():
    scene = canvas(title='Soccer Match',width=800, height=600,
                   center = vector(60,40,0), background = vector(0.37,0.5,0.22),
                   resizable = True)
    
    hor_lines = [[0,0,120],[19.85,0,16.5],[19.85,103.5,120],[30.85,0,5.5],[30.85,114.5,120],
                 [49.85,0,5.5],[49.85,114.5,120],[60.15,0,16.5],[60.15,103.5,120],[80,0,120]]
    ver_lines = [[0,0,80],[5.5,30.85,49.85],[16.5,19.85,60.15],[60,0,80],
                 [103.5,19.85,60.15],[114.5,30.85,49.85],[120,0,80]]
    
    for hor in hor_lines:
        static = hor[0]
        p1 = hor[1]
        p2 = hor[2]
        hl = curve(vector(p1,static,0), vector(p2,static,0))
    
    for ver in ver_lines:
        static = ver[0]
        p1 = ver[1]
        p2 = ver[2]
        hl = curve(vector(static,p1,0), vector(static,p2,0))
    
    cr = shapes.circle(pos=[60,40],radius=9.15, np=360)
    for point in cr:
        vect = vector(point[0],point[1],0)
        hl = points(pos=vect, radius=2)
    
    p1 = points(pos=[vector(60,40,0)], radius=3)
    p1 = points(pos=[vector(11,40,0)], radius=3)
    p1 = points(pos=[vector(109,40,0)], radius=3)
    
    ar = shapes.arc(pos=[109,40],radius=9.15, angle1=(pi+0.9258), angle2=(pi-0.9258), np=360)
    for point in ar:
        vect = vector(point[0],point[1],0)
        hl = points(pos=vect, radius=2, color = color.white)
    
    ar = shapes.arc(pos=[11,40],radius=9.15, angle1=(0.9258), angle2=(-0.9258), np=360)
    for point in ar:
        vect = vector(point[0],point[1],0)
        hl = points(pos=vect, radius=2, color = color.white)
    
    del hor_lines, ver_lines, ar, p1, p2 , cr, static, point, hor , ver



########################################################################################################
#period = 1
#colors    
pass_color = [vector(0.5 ,0 ,0.5),vector(1 ,0.5 ,1)]
carry_color = [vector(0.5 ,0 ,0.5),vector(1 ,0.5 ,1)]    
press_color = [vector(0.5 ,0 ,0.5),vector(1 ,0.5 ,1)]    
    
def play_half(period):
    timing = label(text='0.00',box=False, pos= vector(115,85,0), color = color.black)

    ball = sphere(  pos=vector(60,40,1),  radius=1, trail_color = vector(0.57,0.7,0.42),
                  make_trail=True, trail_type = 'points' , trail_radius = 0.1  , 
                  retain=4, texture = textures.wood_old)

    half = ball_move.loc [ ball_move.loc[:,'period'] == period , : ]

    last_is_shot = False
    
    for index in half.index[1:50]:
        
        team = 1 if half.loc[index,'possession_team/name'] == 'England' else 0
        loc1i = half.loc[index,'location/0']
        loc2i = half.loc[index,'location/1']
        loc1f = half.loc[index,'end_location/0']
        loc2f = half.loc[index,'end_location/1']
        pos_ini = vector(loc1i,loc2i,0)
        pos_fin = vector(loc1f,loc2f,0)

        #wait =  half.loc[index,'secs'] - half.loc[index-1,'secs']
        #timing.text = half.loc[index,'game_time']    
        
        if half.loc[index,'type/name'] == 'Pass':
            ball.pos = vector(pos_ini)
            ball.trail_color = pass_color[team]
            pase = curve(pos_ini, pos_fin , color = pass_color[team], radius = 0.2)
            #pase.visible = False
            #ball.visible = False
            
        if half.loc[index,'type/name'] == 'Ball Receipt*':
            ball.pos = vector(pos_ini)
            if half.loc[index,'pass/outcome/name'] == 'Incomplete':
                rec = points(pos=pos_ini, radius=1  , color=color.red )
        
        if half.loc[index,'type/name'] == 'Carry':
            ball.pos = vector(pos_ini)
            carry = curve(pos_ini, pos_fin , color = carry_color[team], radius = 0.2)
            ball.pos = vector(pos_fin)
        
        if half.loc[index,'type/name'] == 'Pressure':
            press = cylinder(pos=pos_ini, axis=vector(0,0,2), radius=1 )
            press.color = press_color[team] 
        
        index += 1
        print(index)
        
        
        
        if half.loc[index,'type/name'] == 'Shot':
           shot_pos = [loc1,loc2]
           shot_team = team
           shoot_player = half.loc[index,'player']
           last_is_shot = True
        elif last_is_shot == True:
           shot = curve(vector(shot_pos[0],shot_pos[1],0), vector(loc1,loc2,0),
                        color=color.yellow)
           shooter = label(text=shoot_player,  box=False, 
                           pos= vector(shot_pos[0],shot_pos[1],0), 
                           color = color.black, heigth = 8)
    
           last_is_shot = False
        time.sleep(wait/120)

    ball.trail_color = vector(0.37,0.5,0.22)
    ball.pos = vector(60,40,1)
    time.sleep(0.5)
    ball.pos = vector(60,39,1)
    time.sleep(0.5)
    ball.pos = vector(60,40,1)
    time.sleep(0.5)
    ball.pos = vector(61,40,1)
    time.sleep(0.5)
    ball.pos = vector(60,40,1)


########################################################################################################

def passes():
    
    p = curve(vector(shot_pos[0],shot_pos[1],0), vector(loc1,loc2,0),color=color.yellow)


########################################################################################################
    
    
    
time.sleep(5)

new_screen()
play_half(1)

time.sleep(5)

new_screen()
play_half(2)


      



