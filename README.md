# TDI Challenge Project: "When and What to Stream on Twitch.tv ? " 

Twitch.tv boasts over 2 million unique user views per day, and more than 100 thousand channels that entertain the users. How should new streamers stand out from more established names and gather a larger audience? 

Using viewership data from Twitch.tv, I develop a model to help streamers make informed choices on choice of time, game and target language audience. I specifically consider the interaction between these choices, answering such as "When is the best time to stream League of Legends for a given language?" or  "I am a Russian language streamer, what game attracts most audience?"  

Additionally, I describe the whether streamers should stream when avoids time slots with more existing channels. This involves studying whether streamers has synergy with each other, despite acting as competitors by choosing to streaming similar content, together they might attract more viewers than when they stream different types of content. 

Final project target is an application which is trained using historical twitch data, powered by immediate data from the Twitch API. The application offers the best selection of streaming choices under current twitch environment. Answering the questions "I want to gather the most viewships. What game in what language and when should i stream?" 


Original datasource : https://clivecast.github.io

Content:
1. twitch_panel_fixedeffect.py : Panel Regression Model. Data Source 250 MB> 25MB limit, not included.
                                 creates regression data results 'twitch_small_panel_results.txt'

2. twitch_plot.py : Plots graphs using 'twitch_small_panel_results.txt'

3. twitch_small_panel_results.tx : contains regression results generated from twitch_panel_fixedeffect.py
