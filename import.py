import time
import os
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User, Track, Artist, City, Country, Event
from config import Config

# I think that that just leaves us with the users. And what, after all, should their data be?

def users():

    df = pd.read_csv(os.path.join("data", "users.csv"))
    users = list()

    for _, (user_id,) in df.iterrows():

        user = User(id=user_id)
        users.append(user)

    return users


def countries():

    df = pd.read_csv(os.path.join("data", "countries.csv"))
    countries = list()

    for _, (country_id, name) in df.iterrows():

        country = Country(id=country_id, name=name)
        countries.append(country)

    return countries


def cities():

    df = pd.read_csv(os.path.join("data", "cities.csv"))
    cities = list()

    for _, (city_id, name) in df.iterrows():

        city = City(id=city_id, name=name)
        cities.append(city)

    return cities


def tracks():

    df = pd.read_csv(os.path.join("data", "tracks.csv"))
    tracks = list()

    for _, (track_id, name, artist_id) in df.iterrows():

        track = Track(id=track_id, name=name, artist_id=artist_id)
        tracks.append(track)

    return tracks


def artists():

    df = pd.read_csv(os.path.join("data", "artists.csv"))
    artists = list()

    for _, (artist_id, name) in df.iterrows():

        artist = Artist(id=artist_id, name=name)
        artists.append(artist)

    return artists


def events():

    df = pd.read_csv(os.path.join("data", "events.csv"))
    events = list()

    for _, (user_id, track_id, rating, artist_id, country_id, city_id, _, _, _ , _, month, season, weekend) in df.iterrows():

        event = Event(country_id=country_id, city_id=city_id, track_id=track_id, user_id=user_id, rating=rating,
                      month=month, weekend=weekend, season=season)
        events.append(event)

    return events


if __name__ == "__main__":

    config = Config()
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)

    generators = [
        users,
        tracks,
        artists,
        countries,
        cities,
        events
    ]

    for generator in generators:

        print("Importing " + generator.__name__ + "...", end="")

        start = time.time()

        # Create the session
        session = sessionmaker()
        session.configure(bind=engine)
        s = session()

        try:

            data = generator()

            s.bulk_save_objects(data)

            s.commit()

        except Exception as e:

            print("ERROR: ", e)

        finally:

            s.close()

        print(" DONE ({:.2f}s)".format(time.time() - start))
