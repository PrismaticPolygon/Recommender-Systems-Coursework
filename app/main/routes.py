from datetime import datetime
from flask import render_template, redirect, url_for, g
from flask_login import current_user, login_required, logout_user
from flask_babel import _, get_locale
from app import db
# from app.main.forms import RateBookForm, DeleteRatingForm
from app.models import Track, User, Country
from app.main import bp
from app.main.forms import CountryForm
from load import weekend, season
from location import get_location
# from app.auth.forms import DeleteUserForm


@bp.route('/')
def index():

    tracks = Track.query.all()

    return render_template('index.html', title='Home', tracks=tracks)


@bp.route("/compare/", methods=["GET"])
def compare():

    pass

    # tests = request.args.getlist('tests')




@bp.route('/user/<id>', methods=["GET", "POST"])
def user(id):

    user = User.query.filter_by(id=id).first_or_404()

    country_form = CountryForm()

    if country_form.validate_on_submit():

        country_choice = country_form.options.data

        print(country_choice)

    events = user.get_events()


    recommendations = user.get_recommendations(None)

    return render_template('user.html',
                           title=user.id,
                           user=user,
                           country_form=country_form,
                           events=events)
