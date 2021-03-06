import requests

from config import Config

config = Config()


def get_location():

    r = requests.get("https://ipinfo.io?", headers={
        "Authorization": "Bearer {}".format(config.IPINFO_TOKEN),
        "Accept": "application/json"
    })

    country = r.json()["country"]

    if country == "GB":

        return "United Kingdom"

    return country
