# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 10:03:22 2019

@author: kennychuk
"""

import pandas as pd
import numpy as np
from linearmodels import PanelOLS


file_name = 'C:/Users/kennychuk/Documents/Data Science/Twitch/twitch_small_panel_feb2015.txt'
    
twitch_panel = pd.read_csv(file_name,delimiter=",",header=0)
#Find single observation dudes and drop them 

obs_count = twitch_panel.groupby('broadcaster_id').size().reset_index()
obs_count.set_index(['broadcaster_id'], inplace=True)

twitch_panel['obs'] = [obs_count[0][bid] for bid in twitch_panel['broadcaster_id']]
twitch_panel.drop(twitch_panel[twitch_panel['obs']==1].index,inplace=True)

# transmate variables 
twitch_average_views = twitch_panel.groupby('broadcaster_id')['views'].mean()


twitch_panel['average_views'] = [twitch_average_views[x] for x in twitch_panel['broadcaster_id']]
twitch_panel['adj_avg_views'] = (twitch_panel['average_views']- twitch_panel['average_views'].min()) / (twitch_panel['average_views'].max() - twitch_panel['average_views'].min())

twitch_panel['log_views'] = np.log(twitch_panel['views'])
twitch_panel['log_average_views'] = np.log(twitch_panel['average_views'])

twitch_panel['log_other_views']=np.log(twitch_panel['others_views'])
twitch_panel['log_other_views']=twitch_panel['others_views']**2

twitch_panel['adj_others_views'] = (twitch_panel['others_views']- twitch_panel['others_views'].mean()) / ( twitch_panel['others_views'].mean())
twitch_panel['adj_others_views2'] = twitch_panel['adj_others_views']**2

twitch_panel['adj_game_others'] = (twitch_panel['game_others_views']-twitch_panel['game_others_views'].mean())/ (twitch_panel['game_others_views'].mean())
twitch_panel['adj_game_others2'] = twitch_panel['adj_game_others']**2

twitch_panel['view_variation'] = twitch_panel['log_average_views'] - twitch_panel['log_views']

#format for panel 
twitch_panel=twitch_panel.reset_index().set_index(['broadcaster_id','time'])
self_desc =['adj_avg_views']

lang =['lang_en', 'lang_zh', 'lang_ru', 'lang_de', 'lang_fr', 'lang_as']

game = ['game_dota', 'game_lol', 'game_sc2', 'game_hs']
#, \
#        'game_dyinglight','game_csgo','game_talkshow',\
#        'game_l4d2','game_wow','game_minecraft']

meta = ['lang_share', 'adj_others_views', 'adj_others_views2','twitch_hhi',\
        'game_hhi', 'adj_game_others', 'adj_game_others2', \
        'hour_06','hour_12','hour_18']

dependent1 = self_desc+lang+game+meta

#reg = PanelOLS(twitch_panel['view_variation'],\
 #              twitch_panel[dependent1],\
 #              entity_effects=False)

# Add interaction terms
interaction=[]

for x in self_desc:
    for y in ['adj_others_views','adj_others_views2','twitch_hhi', 'hour_06', 'hour_12', 'hour_18']  :
        name = x+'X'+y
        twitch_panel[name] = [xx*yy for xx, yy in zip(twitch_panel[x],twitch_panel[y])]
        interaction.append(name)

for x in lang : 
    for y in ['lang_share','hour_06', 'hour_12', 'hour_18'] : 
        name = x+'X'+y
        twitch_panel[name] = [xx*yy for xx, yy in zip(twitch_panel[x],twitch_panel[y])]
        interaction.append(name)

for x in game : 
    for y in ['game_hhi','adj_game_others', 'adj_game_others2','hour_06', 'hour_12', 'hour_18']+lang : 
        name = x+'X'+y
        twitch_panel[name] = [xx*yy for xx, yy in zip(twitch_panel[x],twitch_panel[y])]
        interaction.append(name)


# Run regression.

dependent2 = dependent1 + interaction

reg=PanelOLS(twitch_panel['view_variation'], twitch_panel[dependent2])
res=reg.fit()
df = pd.DataFrame(res.params)
df.to_csv('twitch_small_panel_results.txt')

