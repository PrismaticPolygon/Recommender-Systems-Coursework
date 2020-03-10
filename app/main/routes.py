
from flask import render_template
from app.models import Track, User
from app.main import bp
from app.main.forms import ContextForm


@bp.route('/')
def index():

    tracks = Track.query.all()

    return render_template('index.html', title='Home', tracks=tracks)


@bp.route('/user/<id>', methods=["GET", "POST"])
def user(id):

    user = User.query.filter_by(id=id).first_or_404()

    context_form = ContextForm()

    events = user.get_events()
    recommendations = user.get_recommendations(context_form.to_context())   # Always use current value of context form

    return render_template('user.html',
                           title=user.id,
                           user=user,
                           recommendations=recommendations,
                           context_form=context_form,
                           events=events)
