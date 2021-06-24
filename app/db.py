import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

# Create a connection to SQLite database.
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# close SQLite database connection after the work is finished
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Python functions that will run schema.sql commands
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f: #opens a file relative to the flaskr package
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

# Function to register close_db and init_db command with the application instance
def init_app(app):
    app.teardown_appcontext(close_db) # app.teardown_appcontext call function when cleaning up after returning the response
    app.cli.add_command(init_db_command) # adds a new command that can be called with flask command
