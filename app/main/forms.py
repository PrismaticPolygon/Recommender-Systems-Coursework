import datetime

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectMultipleField
from wtforms.validators import DataRequired

from load import season, weekend
from location import get_location

from app.models import Country


class ContextForm(FlaskForm):

    countries = [(14, 'Mexico'), (12, 'Japan'), (5, 'El Salvador'), (11, 'Italy'), (1, 'Canada'), (7, 'France'),
                 (9, 'Greece'), (20, 'The Netherlands'), (0, 'Brazil'), (17, 'Spain'), (3, 'China'),
                 (10, 'Indonesia'), (8, 'Germany'), (23, 'United States'), (18, 'Sri Lanka'), (19, 'Thailand'),
                 (22, 'United Kingdom'), (6, 'Finland'), (4, 'Ecuador'), (16, 'Russia'), (2, 'Chile'), (13, 'Malaysia'),
                 (15, 'Portugal'), (21, 'Turkey')]  # Taken from recommender.py country cat codes

    seasons = [(1, "Spring"), (2, "Summer"), (3, "Autumn"), (0, "Winter")]   # See load.py
    weekends = [(1, "True"), (0, "False")]

    countries.sort(key=lambda x: x[1])

    dt = datetime.datetime.today()

    x = get_location()
    country_id = None

    for country in countries:

        if country[1] == x:

            country_id = country[0]

    if country_id is None:  # Default to UK

        country_id = 2

    country_options = SelectMultipleField(
         u'Select country', choices=countries, coerce=int, validators=[DataRequired()], default=[country_id]
    )

    season_options = SelectMultipleField(
        u'Select season', choices=seasons, coerce=int, validators=[DataRequired()], default=[season(dt.month)]
    )

    weekend_options = SelectMultipleField(
        u'Select weekend', choices=weekends, coerce=int, validators=[DataRequired()], default=[weekend(dt.weekday())]
    )

    submit = SubmitField('Submit')

    def to_context(self):

        return {
            "country": self.country_options.data[0],
            "season": self.season_options.data[0],
            "weekend": self.weekend_options.data[0]
        }


