import pandas as pd
import requests
import os

from io import BytesIO
from zipfile import ZipFile

if not os.path.exists("datasets"):

    os.mkdir("datasets")

    response = requests.get("http://www.cp.jku.at/people/schedl/data/MusicMicro/11.11-09.12/musicmicro.zip")
    fileobj = BytesIO(response.content)

    with ZipFile(fileobj) as zipfile:

        zipfile.extractall("datasets")

# I do want to reset the indexes for all

def index(column):

    indices = dict()

    for value in column:

        if value not in indices:

            indices[value] = len(indices)

    return indices


# Re-index artists from 0 - n
artists = pd.read_csv("datasets/artist_mapping.txt", delimiter="\t")
artist_index_map = index(artists["artist-id"])

artists["artist_id"] = artists["artist-id"].map(artist_index_map)
artists = artists.drop("artist-id", axis=1)
artists = artists.set_index("artist_id")

# Cities and countries are already indexed 0 - n
cities = pd.read_csv("datasets/city_mapping.txt", delimiter="\t", index_col="city-id")
countries = pd.read_csv("datasets/country_mapping.txt", delimiter="\t", index_col="country-id")

# Re-index tracks from 0 - n
tracks = pd.read_csv("datasets/track_mapping.txt", delimiter="\t")
track_index_map = index(tracks["track-id"])

tracks["track_id"] = tracks["track-id"].map(track_index_map)
tracks = tracks.drop("track-id", axis=1)
tracks = tracks.set_index("track_id")

# Use index_col to fix malformed file (delimiters at the end of each line)
data = pd.read_table("datasets/listening_data.txt", index_col=False)

# Map user_id from 0 to n
user_index_map = index(data["user-id"])

data["user_id"] = data["user-id"].map(user_index_map)
data = data.drop("user-id", axis=1)

# Replace artist-id and track-id with mappings
data["artist_id"] = data["artist-id"].map(artist_index_map)
data["track_id"] = data["track-id"].map(track_index_map)

data = data.drop(["track-id", "artist-id", "twitter-id"], axis=1)

# Drop NaN values. Some of the tracks and artists in listening_data.txt don't have equivalents in artist_mapping / track_mapping
data = data.dropna()

data = data.reset_index(drop=True)

# I won't do any of the other shit.
# There isn't much point, after all.

print(data.columns)

print(data)

data = data.join(cities, on="city_id")
data = data.join(countries, on="country_id")
data = data.join(artists, on="artist_id")
data = data.join(tracks, on="track_id")

# Let's just do a bit.

data.to_csv("datasets/raw.csv")