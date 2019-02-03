# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 16:31:45 2019

@author: kennychuk
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

# PLOT 1 Best Best Time/Language to stream a given Game! 
file_name = 'C:/Users/kennychuk/Documents/Data Science/Twitch/twitch_small_panel_results.txt'
twitch = pd.read_csv(file_name,delimiter=",",header=0)
twitch.columns = ['param','result']
twitch.index=twitch['param']
twitch.drop(columns=['param'], inplace=True)

lang = ['lang_en','lang_zh','lang_ru','lang_de']
time =['00','06','12','18']
game = ['game_dota', 'game_lol','game_hs','game_sc2']
game_name={'game_dota' : 'Dota 2', 'game_lol' : 'League of Legends', \
           'game_hs' : 'Hearthstone', 'game_sc2' : 'StarCraft 2'}
i=0
fig= plt.figure(figsize=[12,12])
fig.suptitle('Best Time/Language to Stream Game')
for g in game :
    g_array, t_array =[], []
    i+=1
    for t0 in time:
        for l in lang: 
            t = 'hour_'+t0
            if t0=='00':
                effect = twitch.loc[[l,g+'X'+l,g]].sum()
            else : 
                effect = twitch.loc[[g+'X'+l,g,l,t,g+'X'+t]].sum()
            #print("LANG:", l, "TIME:", t)
            t_array.append(effect)
            
        g_array.append(t_array)
        t_array=[]
    g_array = np.array(g_array).reshape([len(lang),len(time)])
    plt.subplot(2,2,i)   
    
    sns.heatmap(g_array)
    plt.title(game_name[g])
    plt.xticks(np.arange(len(time))+0.5,['00-06','06-12','12-18','18-24'])
    plt.yticks(np.arange(len(lang))+0.5,['ENG','CHN','RUS','GER'])
    plt.xlabel('Time-Slot (PST)')
    plt.ylabel('Language')

### PLOT 2 DO I want to avoid traffic?? 

game = ['game_dota', 'game_lol', 'game_hs']
game_name={'game_dota' : 'Dota 2', 'game_lol' : 'League of Legends', \
           'game_hs' : 'Hearthstone', 'game_sc2' : 'StarCraft 2','game_others' : 'Others'}

views_var = np.arange(-0.1,0.1,0.01)
impact=[]
ag,bg = twitch.loc[['adj_game_others','adj_game_others2']]['result']
for g in game :
    a,b,c = twitch.loc[[g+'Xadj_game_others2', g+'Xadj_game_others' , g]]['result']
    impact.append((a+ag) * views_var**2 +(b+bg) * views_var + c )

game.append('game_others')
impact.append((ag) * views_var**2 +(bg) * views_var)

impact = list(map(list, zip(*impact)))

fig = plt.figure(figsize=(8,6))

plt.plot(views_var,impact)

plt.xlim(-0.1,0.1)
plt.axvline(0, color='gray')
plt.legend([game_name[g] for g in game])
plt.title('Streamer Synergy/Competition Across Games')
plt.xlabel('Normalized Deviation from Mean Game Viewweship')
plt.ylabel('Impact on Individual Stream Viewship')

