from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectMultipleField
# from wtforms.validators import ValidationError, DataRequired, NumberRange
from app.models import Country

class CountryForm(FlaskForm):

    # countries = Country.query.order_by(Country.name.asc()).with_entities(Country.name, Country.id).all()

    countries = [("UK", 2)]

    options = SelectMultipleField(
         u'Select country', choices=countries
    )

    submit = SubmitField('Submit')



