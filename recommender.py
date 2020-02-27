import pandas as pd
import requests

from config import IPINFO_TOKEN


df = pd.read_csv("datasets/data.csv", index_col="twitter-id")

r = requests.get("https://ipinfo.io?", headers={
    "Authorization": "Bearer {}".format(IPINFO_TOKEN),
    "Accept": "application/json"
})

location = r.json()

print(location)
