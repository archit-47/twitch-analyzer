import os
import requests
import pandas as pd
import datetime
import Twitch_data as ttv

streamer = ttv.twitch_channel('fl0m') #channel name here
print(streamer.name)
print(streamer.id)

#two options either range of dates or a list
date_list = pd.date_range(start="2022-01-31",end="2022-02-07") #range of dates
# date_list = ['2021-07-26','2021-07-27','2021-07-28']  #individual date list
print(date_list)

streamer.get_vod_by_datelist(date_list) #modify these dates ('yyyy-mm-dd')
streamer.vod_id_list.reverse()
print("IDs of requested VODs :"+",".join(streamer.vod_id_list)) 
streamer.get_vod_logs()

logs_list=[]

for log in streamer.vod_id_list:
	if not os.path.exists(os.getcwd()+"\\formatted_logs\\"):
		try:
			os.makedirs(os.getcwd()+"\\formatted_logs\\")
		except OSError as error:
			print(error)
	f_original=open(os.getcwd()+"\\logs\\"+log+".txt",encoding='utf-8',mode='r')
	f_modified=open(os.getcwd()+"\\formatted_logs\\"+log+".txt",encoding='utf-8',mode='w+')

	for line in f_original.read().split('\n'):
		line=line.split(' ')
		try:
			f_modified.write(line[0][1:-1]+"\t"+line[1][1:-1]+"\t"+" ".join(line[2:])+"\n")
		except:
			pass
	f_original.close()
	f_modified.close()
	logs_list.append(pd.read_csv(os.getcwd()+"\\formatted_logs\\"+log+".txt",sep='\t',names=['Timestamp','Username','Message'],dtype={'Timestamp':str,'Username':str,'Message':str},encoding='utf-8',keep_default_na=False))

# Filter bot messages
df=pd.concat(logs_list, axis=0, ignore_index=True)
df2=df.loc[df.Username!='Techno']
df3=df2.loc[df.Username!='Nightbot']
df4=df3.loc[df.Username!='Moobot'] 

freq=df4.groupby('Username').Username.count()
print("Most active users in the given time period!")
print(freq.sort_values(ascending=False)[0:20])

bttv_emotes=requests.get('https://twitch.center/customapi/bttvemotes?channel='+streamer.name) #request to get bttv emotes via API endpoint
bttv_dict = {}    
bttv_emotes=bttv_emotes.text.split(' ')
for emote in bttv_emotes:
    bttv_dict[emote]=0
    
ffz_emotes=requests.get('https://api.frankerfacez.com/v1/room/id/'+streamer.id).json() #request to get ffz emotes via API endpoint
ffz_dict={}
ffz_keys=list(ffz_emotes['sets'].keys())
for emote in ffz_emotes['sets'][ffz_keys[0]]['emoticons']:
    ffz_dict[emote['name']]=0

emotes_7tv=requests.get('https://emotes.adamcy.pl/v1/channel/'+str(streamer.id)+'/emotes/7tv').json() #request to get bttv emotes via API endpoint
dict_7tv = {}
for x in emotes_7tv:
    dict_7tv[x['code']]=0

channel_emotes_dict={}
headers={
   	'Client-ID': streamer.user.client_id,
   	'Authorization':'Bearer '+streamer.user.key['access_token']
}
query={
	'broadcaster_id':streamer.id
}
response = requests.get('https://api.twitch.tv/helix/chat/emotes',headers=headers,params=query).json() #request to get channel emotes via Twitch API 
for emote in response['data']:
	channel_emotes_dict[emote['name']]=0
	
message_dict={}
BotMessages=0
copypasta={}

for index,row in df.iterrows():
	message=row['Message']
	user=row['Username']
	if user in ['Nightbot','Moobot','HLBot','Techno']:
		BotMessages+=1
		continue
	message=message.strip()
	if message not in message_dict:
		message_dict[message]=1
	else:
		message_dict[message]+=1
	if len(message.split(' '))>2:
		if message in copypasta.keys():
			copypasta[message]+=1
		else:
			copypasta[message]=1
	message=message.split(' ')
	for word in message:
		if word in bttv_dict.keys():
			bttv_dict[word]+=1
		elif word in ffz_dict.keys():
			ffz_dict[word]+=1
		elif word in channel_emotes_dict.keys():
			channel_emotes_dict[word]+=1
		elif word in dict_7tv.keys():
			dict_7tv[word]+=1


print("\nStats on chat messages:")
print("\nTotal Messages : "+str(df.shape[0]))
print("\nUnique Messages : "+str(len(message_dict)))
print("\nDuplicate Messages : "+str(df.shape[0]-len(message_dict)))
print("\nBot Messages : "+str(BotMessages))

print("\nBTTV Emote stats:")
bttv_list=sorted(bttv_dict,key=bttv_dict.__getitem__)
for x in bttv_list:
    print(x+"\t"+str(bttv_dict[x]))

print("\nFFZ Emote stats:")
ffz_list=sorted(ffz_dict,key=ffz_dict.__getitem__)
for x in ffz_list:
    print(x+"\t"+str(ffz_dict[x]))

print("\n7TV Emote stats:")
list_7tv=sorted(dict_7tv,key=dict_7tv.__getitem__)
for x in list_7tv:
    print(x+"\t"+str(dict_7tv[x]))

print("\nChannel Emote stats:")
channel_emotes_list=sorted(channel_emotes_dict,key=channel_emotes_dict.__getitem__)
for x in channel_emotes_list:
    print(x+"\t"+str(channel_emotes_dict[x])) 

copy_pasta_list=sorted(copypasta,key=copypasta.__getitem__)
for x in copy_pasta_list[-11:-1]:
	print(x+ " : " + str(copypasta[x]))