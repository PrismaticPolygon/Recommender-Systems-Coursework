from datetime import datetime
from flask import render_template, redirect, url_for, g
from flask_login import current_user, login_required, logout_user
from flask_babel import _, get_locale
from app import db
# from app.main.forms import RateBookForm, DeleteRatingForm
from app.models import Track
from app.main import bp
# from app.auth.forms import DeleteUserForm


@bp.route('/')
def index():

    tracks = Track.query.all()

    return render_template('index.html', title='Home', tracks=tracks)

#
# @bp.route('/user/<username>', methods=["GET", "POST"])
# def user(username):
#
#     user = User.query.filter_by(username=username).first_or_404()
#
#     # edit_form = RateBookForm()
#     # delete_form = DeleteRatingForm()
#     # delete_user_form = DeleteUserForm()
#     #
#     # delete_form.set_user_id(current_user.id)
#
#     # if edit_form.validate_on_submit():  # Creating or updating a rating
#     #
#     #     user_id = current_user.id
#     #     book_id = edit_form.book_id
#     #
#     #     rating = Rating.query.filter_by(book_id=book_id, user_id=user_id).first()
#     #
#     #     if rating is None:
#     #
#     #         rating = Rating(book_id=book_id, user_id=user_id, value=edit_form.rating.data)
#     #
#     #         db.session.add(rating)
#     #
#     #     else:
#     #
#     #         rating.value = edit_form.rating.data
#     #
#     #     db.session.commit()
#     #
#     #     return redirect(url_for('main.user', username=user.username))
#     #
#     # if delete_form.validate_on_submit():    # Deleting a rating
#     #
#     #     rating_id = delete_form.rating_id
#     #
#     #     Rating.query.filter_by(id=rating_id).delete()
#     #
#     #     db.session.commit()
#     #
#     #     return redirect(url_for('main.user', username=user.username))
#     #
#     # if delete_user_form.validate_on_submit():   # Deleting a user
#     #
#     #     user_id = current_user.id
#     #
#     #     logout_user()
#     #
#     #     Rating.query.filter_by(user_id=user_id).delete()
#     #     User.query.filter_by(id=user_id).delete()
#     #
#     #     db.session.commit()
#     #
#     #     return redirect(url_for('main.index'))
#
#     events = user.get_ratings()
#
#     for event in events:
#
#         print(events)
#
#     # recommendations = user.get_recommendations()
#
#     return render_template('user.html',
#                            title=user.id,
#                            user=user,
#                            events=events)
#                            # recommendations=recommendations,
#                            # edit_form=edit_form,
#                            # delete_user_form=delete_user_form,
#                            # delete_form=delete_form)