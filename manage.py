from app import create_app, db
from flask.cli import FlaskGroup

cli = FlaskGroup(create_app=create_app)

@cli.command("init-db")
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Initialized the database.')
