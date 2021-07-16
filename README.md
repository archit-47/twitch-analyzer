# Data analysis using Twitch API

Works on Python3 [Link](https://www.python.org/downloads/)

Install requirements with ``pip install requirements.txt``

Go to [Link](https://twitchapps.com/tmi/) to request an auth token for your twitch account. 

Clone this github repo and create a new file config.py

Add the following lines to this file :

```
import requests

client_id='<your_client_id>'
client_secret='<your_client_secret>'

def get_key():
	body={
        'client_id':client_id,
        'client_secret':client_secret,
        'grant_type':'client_credentials'
    }
	r=requests.post('https://id.twitch.tv/oauth2/token', body)
	keys=r.json()
	return keys
```
