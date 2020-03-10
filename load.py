import pandas as pd
import requests
import os

from io import BytesIO
from zipfile import ZipFile

raw = os.path.join("data", "raw")

if not os.path.exists(raw):

    os.makedirs(raw)

    response = requests.get("http://www.cp.jku.at/people/schedl/data/MusicMicro/11.11-09.12/musicmicro.zip")
    fileobj = BytesIO(response.content)

    with ZipFile(fileobj) as zipfile:

        zipfile.extractall(raw)

artists = pd.read_table(os.path.join(raw, "artist_mapping.txt"), index_col="artist-id")
cities = pd.read_table(os.path.join(raw, "city_mapping.txt"), index_col="city-id")
countries = pd.read_table(os.path.join(raw, "country_mapping.txt"), index_col="country-id")
tracks = pd.read_table(os.path.join(raw, "track_mapping.txt"), index_col="track-id")

# Use index_col to fix malformed file (delimiters at the end of each line)
df = pd.read_table(os.path.join(raw, "listening_data.txt"), index_col=False)

# Merge on respective IDs
df = df.join(cities, on="city-id")
df = df.join(countries, on="country-id")
df = df.join(artists, on="artist-id")
df = df.join(tracks, on="track-id")

# Remove null columns and duplicates
df = df.dropna()
df = df.drop_duplicates()

# Sort by frequency: https://stackoverflow.com/questions/44363585/sort-by-frequency-of-values-in-a-column-pandas
# This is much faster than the top answer
frequencies = df["user-id"].value_counts().to_dict()
df["frequency"] = df["user-id"].map(frequencies)
df = df.sort_values("frequency", ascending=False)

# Remove redundant columns
df = df.drop(["twitter-id", "frequency", "latitude", "longitude"], axis=1)

# Rename columns to use underscores
df = df.rename(lambda name: name.replace("-", "_"), axis=1)


def season(month):

    if month in [11, 12, 1]:

        return 0    # Winter

    elif month in [2, 3, 4]:

        return 1    # Spring

    elif month in [5, 6, 7]:

        return 2    # Summer

    elif month in [8, 9, 10]:

        return 3    # Autumn


def weekend(weekday):

    return 0 if weekday < 5 else 1


def index(column):

    return {x: i for (i, x) in enumerate(df[column].unique())}


df["season"] = df["month"].map(season)
df["weekend"] = df["weekday"].map(weekend)
df["rating"] = 1

# Re-order columns for cleaner recommender code
df = df[["user_id", "track_id", "rating", "artist_id", "country_id", "city_id", "track", "artist", "country", "city",
         "month", "season", "weekend"]]

# Re-number user, track, and artist IDs from 0 - n for use in SVD and DB
df["user_id"] = df["user_id"].map(index("user_id"))
df["track_id"] = df["track_id"].map(index("track_id"))
df["artist_id"] = df["artist_id"].map(index("artist_id"))

# Save just the used tracks to CSV for use in DB
tracks = df[["track_id", "track", "artist_id"]]
tracks = tracks.rename({"track": "name"}, axis=1)
tracks = tracks.set_index("track_id")
tracks = tracks.sort_index()
tracks = tracks.drop_duplicates()

tracks.to_csv(os.path.join("data", "tracks.csv"))

# Save just the used artists to CSV for use in DB
artists = df[["artist_id", "artist"]]
artists = artists.rename({"artist": "name"}, axis=1)
artists = artists.set_index("artist_id")
artists = artists.sort_index()
artists = artists.drop_duplicates()

artists.to_csv(os.path.join("data", "artists.csv"))

# Save countries
countries = df[["country_id", "country"]]
countries = countries.rename({"country": "name"}, axis=1)
countries = countries.set_index("country_id")
countries = countries.sort_index()
countries = countries.drop_duplicates()

countries.to_csv(os.path.join("data", "countries.csv"))

# Save cities
cities = df[["city_id", "city"]]
cities = cities.rename({"city": "name"}, axis=1)
cities = cities.set_index("city_id")
cities = cities.sort_index()
cities = cities.drop_duplicates()

cities.to_csv(os.path.join("data", "cities.csv"))

# And finally, save users
users = df[["user_id"]]
users = users.drop_duplicates()
users.to_csv(os.path.join("data", "users.csv"), index=False)

# Save to CSV sans columns
df.to_csv(os.path.join("data", "events.csv"), index=False)
