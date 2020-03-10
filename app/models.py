import os
import pandas as pd
import numpy as np

from hashlib import md5
from app import db


P = pd.read_csv(os.path.join("weights", "P.csv"))   # Predictions matrix
B = np.load(os.path.join("weights", "B.npy"))       # Context weight matrix


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    events = db.relationship("Event", backref="user", lazy="dynamic")

    def __repr__(self):

        return '#{}: {}'.format(self.id, self.username)

    def get_events(self):

        events = self.events.join(Track, Artist, City, Country).add_columns(Track.name, Track.artist_id, Artist.name,
                                                                            City.name, Country.name).all()

        events = [{
            "id": event[0].id,
            "month": event[0].month,
            "weekend": event[0].weekend,
            "season": event[0].season,
            "rating": event[0].rating,
            "city_id": event[0].city_id,
            "country_id": event[0].country_id,
            "user_id": event[0].user_id,
            "name": event[1],
            "artist_id": event[2],
            "artist": event[3],
            "city": event[4],
            "country": event[5]
        } for event in events]

        return events

    def get_recommendations(self, context=None, num_recommendations=10):

        tracks = [x[0] for x in self.events.with_entities(Event.track_id).all()]    # IDs of tracks already rated

        predictions = P[P["user_id"] == self.id].sort_values(by="prediction", ascending=False)   # Get all user predictions
        predictions = predictions[~predictions["track_id"].isin(tracks)]                         # Remove tracks already seen
        predictions = predictions.dropna()                                                       # Shouldn't be any, but just in case

        if context:

            weight = 0

            for i, key in enumerate(context):

                weight += B[i, context[key]]

            predictions["prediction"] += weight

            print("{} -> {}".format(context, weight))

        predictions = predictions[:num_recommendations]
        predictions["prediction"] = predictions["prediction"].map(lambda x: "{:.3f}".format(x))

        records = []

        # SQLAlchemy is fucking garbage. I don't have a damn clue how this query should be written.
        for i, row in predictions.iterrows():

            track_id = row["track_id"]
            value = row["prediction"]

            track = Track.query.get(track_id)
            artist = Artist.query.get(track.artist_id)

            records.append({
                "track_id": int(track_id),
                "name": track.name,
                "artist": artist.name,
                "value": value
            })

        return records

    def avatar(self, size):

        digest = md5(str(self.id).lower().encode('utf-8')).hexdigest()

        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


class Event(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    country_id = db.Column(db.Integer, db.ForeignKey("country.id"))
    city_id = db.Column(db.Integer, db.ForeignKey("city.id"))
    track_id = db.Column(db.Integer, db.ForeignKey("track.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    month = db.Column(db.Integer)
    weekend = db.Column(db.Integer)
    season = db.Column(db.Integer)
    rating = db.Column(db.Integer)

    def __repr__(self):

        return '#{}: user {} listened to {}'.format(self.id, self.user_id, self.track_id)

    def to_dict(self):

        return {
            "id": self.id,
            "city_id": self.city_id,
            "track_id": self.track_id,
            "country_id": self.country_id,
            "month": self.month,
            "weekend": self.weekend,
            "season": self.season,
            "rating": self.rating
        }


class Country(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))

    def __repr__(self):

        return '{}'.format(self.name)


class City(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))

    def __repr__(self):

        return '#{}: {}'.format(self.id, self.name)


class Track(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id"))
    name = db.Column(db.String(140))

    def __repr__(self):

        return '#{}: {}'.format(self.id, self.name)


class Artist(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))

    def __repr__(self):

        return '#{}: {}'.format(self.id, self.name)
