import requests

from config import IPINFO_TOKEN

r = requests.get("https://ipinfo.io?", headers={
    "Authorization": "Bearer {}".format(IPINFO_TOKEN),
    "Accept": "application/json"
})

location = r.json()
