import os
import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt

import Twitch_data as ttv

streamer = ttv.twitch_channel('fl0m'); #channel name here
print(streamer.name)
print(streamer.id)
date_list = pd.date_range(start="2022-02-14",end="2022-02-21") #range of dates
# date_list = ['2021-07-26','2021-07-27','2021-07-28']  #individual date list
print(date_list)
streamer.get_vod_by_datelist(date_list) #modify these dates ('yyyy-mm-dd')
streamer.get_datelist_data()
print("IDs of requested vods :"+",".join(streamer.vod_id_list))

streamer.get_vod_logs()
print("Raw Data : ")
print(streamer.voddict_by_date)
print("\n\n")
df=pd.DataFrame(streamer.voddict_by_date).T
df=df.reindex(index=df.index[::-1])

fig = plt.figure()
names=df.index
y=df["total_duration"].dt.seconds/3600
plt.bar(names,y,width=0.6)
plt.ylabel('Hours-Streamed')
plt.xlabel('Date')
plt.title('Hours-Streamed on specific dates')

fig=plt.figure()
y2=df["message_count"]
plt.bar(names,y2,width=0.6)
plt.xlabel('Date')
plt.ylabel('Total Messages')
plt.title('Number of chat messages on specific dates')

fig=plt.figure()
y3=y2/y
plt.bar(names,y3,width=0.6)
plt.xlabel('Date')
plt.ylabel('Total Messages per hour (average)')
plt.title('Number of chat messages per hour (average) by date')
plt.show()