import os
import datetime
import requests
import config

class user_auth:
	def __init__(self):
		self.client_id=config.client_id
		self.key=config.get_key()


class twitch_channel:
	def __init__(self,name):
		self.name=name
		self.user=user_auth()
		self.id=self.get_channel_id()
		self.vod_id_list=[]
		self.voddict_by_id={}
		self.voddict_by_date={}

	def get_channel_id(self):
		headers={
	    	'Client-ID': self.user.client_id,
	    	'Authorization':'Bearer '+self.user.key['access_token']
		}
		query={
		    'login':self.name
		}
		response = requests.get('https://api.twitch.tv/helix/users',headers=headers,params=query).json()
		channelID = None
		if len(response['data']): #check if there exists a channel like this 
			channel_id = response['data'][0]['id'] #returned channel id in the response
			return channel_id
		else:
		    return -1

	def get_vod_by_datelist(self,datelist):
		headers={
	    	'Client-ID': self.user.client_id,
	    	'Authorization':'Bearer '+self.user.key['access_token']
		}
		query={
			'user_id':self.id,
			'first':100
		}
		response = requests.get('https://api.twitch.tv/helix/videos',headers=headers,params=query).json()
		for x in response['data']:
			if x['created_at'][0:10] in datelist:
				self.vod_id_list.append(x['id'])
				self.voddict_by_id[x['id']]=x
				if x['created_at'][0:10] not in self.voddict_by_date.keys():
					self.voddict_by_date[x['created_at'][0:10]]={'id':[]}
					self.voddict_by_date[x['created_at'][0:10]]['id'].append(x['id'])
				else:
					self.voddict_by_date[x['created_at'][0:10]]['id'].append(x['id'])
		

streamer = twitch_channel('fl0m');
print(streamer.name)
print(streamer.id)
streamer.get_vod_by_datelist(['2021-07-12','2021-07-13','2021-07-14','2021-07-15','2021-07-16','2021-07-17','2021-07-18',])
print(streamer.vod_id_list)
print(streamer.voddict_by_date)
