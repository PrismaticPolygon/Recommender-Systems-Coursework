from app import create_app, db
from app.models import User, Event, City, Country, Track, Artist

app = create_app()


@app.shell_context_processor
def make_shell_context():

    return {'db': db, 'User': User, 'Event': Event, 'City': City, 'Country': Country, 'Track': Track, 'Artist': Artist}
