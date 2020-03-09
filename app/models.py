import os
import pandas as pd
import numpy as np

from hashlib import md5
from app import db
from config import Config


P = pd.read_csv(os.path.join("weights", "P.csv"), index_col="user_id")
B = np.load(os.path.join("weights", "B.npy"))

# config = Config()


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    events = db.relationship("Event", backref="user", lazy="dynamic")

    def __repr__(self):

        return '#{}: {}'.format(self.id, self.username)

    # Nah. Too long. I'd have to maintain a sparse matrix in the background.
    # Perhaps I could just update rows? No: it's not important.
    # As we're not going to be adding new tracks or users, it's all Gucci.
    # And I could, in fact, update R.
    # Load up R.


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

        # events = pd.read_sql(self.events, config.SQLALCHEMY_DATABASE_URI)
        events = pd.DataFrame([event.to_dict() for event in self.events.all()])

        # Bruh

        predictions = pd.DataFrame(P.iloc[self.id].sort_values(ascending=False)).reset_index()  # Get predictions for that user.


        # Strange.

        print(predictions)

        # # Then merge onto event details. Not ideal having these backing DFs!
        #
        # # So what's the purpose of events again?
        #
        # if context:     # Otherwise multiply with context-weight matrix
        #
        #     pass
        #
        # predictions = predictions.dropna()
        #
        # return predictions[:num_recommendations]

    #
    #     ratings = pd.DataFrame([rating.to_dict() for rating in self.ratings.all()])
    #
    #     if ratings.empty:    # Return some random books
    #
    #         recommendations = books_df.sample(n=num_recommendations)
    #
    #         recommendations["value"] = "No data available"
    #         recommendations["genres"] = recommendations["genres"].str.replace("|", ", ")
    #
    #         return recommendations.to_dict("records")
    #
    #     user_predictions = pd.DataFrame(predictions_df.iloc[self.id - 1].sort_values(ascending=False)).reset_index()
    #     user_predictions.columns = ["book_id", "value"]
    #
    #
    #     print("USER PREDICTIONS\n")
    #     print(user_predictions)
    #
    #     user_full = ratings.merge(books_df, how='left', on='book_id').sort_values('value', ascending=False)
    #
    #     # Remove books that the user has already rated
    #     books_df = books_df[~books_df['book_id'].isin(user_full['book_id'])]
    #
    #     print("BOOKS\n")
    #     print(books_df)
    #
    #     recommendations = books_df.merge(user_predictions, how='left', on='book_id').sort_values('value', ascending=False)
    #     recommendations = recommendations[~recommendations["value"].isna()].iloc[:num_recommendations]
    #     recommendations["genres"] = recommendations["genres"].str.replace("|", ", ")
    #     recommendations["value"] = recommendations["value"].map(lambda x: "{0:.2f}".format(x))
    #
    #     print("RECOMMENDATIONS\n")
    #     print(recommendations)
    #
    #     return recommendations.to_dict("records")

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
