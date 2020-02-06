import pandas as pd

artists = pd.read_csv("datasets/artist_mapping.txt", delimiter="\t", index_col="artist-id")
cities = pd.read_csv("datasets/city_mapping.txt", delimiter="\t", index_col="city-id")
countries = pd.read_csv("datasets/country_mapping.txt", delimiter="\t", index_col="country-id")
tracks = pd.read_csv("datasets/track_mapping.txt", delimiter="\t", index_col="track-id")

data = pd.read_csv("datasets/listening_data.txt", delimiter="\t", encoding="utf-8")

data = data.rename({
    "twitter-id": "user-id",
    "user-id": "month",
    "month": "weekday",
    "weekday": "longitude",
    "longitude": "latitude",
    "latitude": "country-id",
    "country-id": "city-id",
    "city-id": "artist-id",
    "track-id": "drop",
    "artist-id": "track-id"
}, axis=1)

data.index.name = "twitter-id"
data = data.drop("drop", axis=1)

data = data.join(artists, on="artist-id")
data = data.join(cities, on="city-id")
data = data.join(countries, on="country-id")
data = data.join(tracks, on="track-id")

data.to_csv("datasets/data.csv")