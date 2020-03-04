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

artists = pd.read_table("datasets/artist_mapping.txt", index_col="artist-id")
cities = pd.read_table("datasets/city_mapping.txt", index_col="city-id")
countries = pd.read_table("datasets/country_mapping.txt", index_col="country-id")
tracks = pd.read_table("datasets/track_mapping.txt", index_col="track-id")

# Use index_col to fix malformed file (delimiters at the end of each line)
df = pd.read_table("datasets/listening_data.txt", index_col=False)

# Merge on respective IDs
df = df.join(cities, on="city-id")
df = df.join(countries, on="country-id")
df = df.join(artists, on="artist-id")
df = df.join(tracks, on="track-id")

# Remove null columns and duplicates
df = df.dropna()
df = df.drop_duplicates()

# Sort by frequency: https://stackoverflow.com/questions/44363585/sort-by-frequency-of-values-in-a-column-pandas
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
df = df[["user_id", "track_id", "rating", "artist_id", "city_id", "track", "artist", "country", "city", "month",
         "season", "weekend"]]

# Re-number user and track IDs from 0 - n for use in SVD
df["user_id"] = df["user_id"].map(index("user_id"))
df["track_id"] = df["track_id"].map(index("track_id"))

# Save to CSV sans columns
df.to_csv(os.path.join("datasets", "data.csv"), index=False)
