# Data analysis using Twitch API

Works on [Python3](https://www.python.org/downloads/)

I Recommend creating a virtual environment before the following steps. [Read more here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

After you have created a virtual environment and activated it, proceed with the following steps.

Clone this repository 

Install requirements with ``pip install requirements.txt``

Go to [this link](https://twitchapps.com/tmi/) to request an auth token for your twitch account. 

Create a new file config.py

Add the following lines to this file :

```python
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

Modify plots.py with the name of the twitch channel you want statistics for, subsequently specify the dates as you wish.

Run the python file plots.py

(Getting logs can take time depending on the activity on a channel. Be patient)

Note : [tcd](https://github.com/PetterKraabol/Twitch-Chat-Downloader) will ask for your client id and client secret when running for the first time.