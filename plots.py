import os
import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt

import Twitch_data as ttv

streamer = ttv.twitch_channel('pokimane'); #channel name here
print(streamer.name)
print(streamer.id)
streamer.get_vod_by_datelist(['2021-07-12','2021-07-13','2021-07-14','2021-07-15','2021-07-16','2021-07-17','2021-07-18']) #modify these dates ('yyyy-mm-dd')
streamer.get_datelist_data()
print("IDs of requested vods :"streamer.vod_id_list)

streamer.get_vod_logs()
print("Raw Data : ")
print(streamer.voddict_by_date)
print("\n\n")
df=pd.DataFrame(streamer.voddict_by_date).T

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