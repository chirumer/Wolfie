import os
from dotenv import load_dotenv
    # to load env variables from file
load_dotenv()
app_id = os.getenv('dictionary_id')
app_key = os.getenv('dictionary_secret')
print(app_id, app_key)
import json
import requests
endpoint = "entries"
language_code = "en-us"
word_id = "example"
url = "https://od-api.oxforddictionaries.com/api/v2/" + endpoint + "/" + language_code + "/" + word_id.lower()
r = requests.get(url, headers = {"app_id": app_id, "app_key": app_key})
print("code {}\n".format(r.status_code))
print("text \n" + r.text)
print("json \n" + json.dumps(r.json()))
