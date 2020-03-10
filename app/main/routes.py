from datetime import datetime
from flask import render_template, redirect, url_for, g
from flask_login import current_user, login_required, logout_user
from flask_babel import _, get_locale
from app import db
# from app.main.forms import RateBookForm, DeleteRatingForm
from app.models import Track, User, Country
from app.main import bp
from app.main.forms import ContextForm
from load import weekend, season
from location import get_location
# from app.auth.forms import DeleteUserForm


@bp.route('/')
def index():

    tracks = Track.query.all()

    return render_template('index.html', title='Home', tracks=tracks)


@bp.route('/user/<id>', methods=["GET", "POST"])
def user(id):

    user = User.query.filter_by(id=id).first_or_404()

    context_form = ContextForm()

    # Not a valid choice for this field? That doesnt' make sense.

    if context_form.validate_on_submit():

        context = {
            "country": context_form.country_options.data[0],
            "season": context_form.season_options.data[0],
            "weekend": context_form.weekend_options.data[0]
        }

        recommendations = user.get_recommendations(context)

    # I don't want to reload the page, though.

    events = user.get_events()

    recommendations = user.get_recommendations()

    return render_template('user.html',
                           title=user.id,
                           user=user,
                           recommendations=recommendations,
                           context_form=context_form,
                           events=events)
