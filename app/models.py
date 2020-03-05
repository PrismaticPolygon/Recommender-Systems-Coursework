from hashlib import md5
from app import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    events = db.relationship("Event", backref="user", lazy="dynamic")

    def __repr__(self):

        return '#{}: {}'.format(self.id, self.username)

    def get_events(self):

        events = self.events.order_by(Event.value.desc()).join(Track).add_columns(Track.name, Track.id).all()

        print(events)

        events = [{
            "value": event[0].value,
            "title": event[1],
            "genres": event[2].replace("|", ", "),
            "book_id": event[3]
        } for event in events]

        return events

    # @staticmethod
    # def build_matrices():
    #
    #     # Convert Book to a DataFrame
    #     books_df = pd.DataFrame([book.to_dict() for book in Book.query.all()])
    #     books_df = books_df.rename({"id": "book_id"}, axis=1)
    #
    #     print("BOOKS\n")
    #     print(books_df)
    #
    #     # Convert Rating to a DataFrame
    #     ratings_df = pd.DataFrame([rating.to_dict() for rating in Rating.query.all()])
    #     ratings_df = ratings_df.drop("id", axis=1)
    #
    #     print("RATINGS\n")
    #     print(ratings_df)
    #
    #     R_df = ratings_df.pivot(index="user_id", columns="book_id", values="value")
    #
    #     user_ratings_mean = np.array(R_df.mean(axis=1))
    #
    #     R_demeaned = R_df.sub(R_df.mean(axis=1), axis=0).fillna(0).values
    #
    #     k = min(R_demeaned.shape[0] - 1, 25)
    #
    #     U, sigma, Vt = svds(R_demeaned, k=k)
    #     sigma = np.diag(sigma)
    #
    #     predictions = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
    #     predictions_df = pd.DataFrame(predictions, columns=R_df.columns)
    #
    #     return predictions_df, books_df
    #
    #
    # def get_recommendations(self, num_recommendations=10):
    #
    #     predictions_df, books_df = User.build_matrices()
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

        digest = md5(self.id.lower().encode('utf-8')).hexdigest()

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


class Country(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))

    def __repr__(self):

        return '#{}: {}'.format(self.id, self.name)


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
