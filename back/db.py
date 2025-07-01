import os
import click
import traceback
import mysql.connector
from dotenv import load_dotenv
from flask import current_app, g

load_dotenv()

def get_db():
    if 'db' not in g:
        try:
            g.db_conn = mysql.connector.connect(
                host=os.getenv('HOST_NAME'),
                user=os.getenv('USER_NAME'),
                password=os.getenv('PASSWORD'),
                database=os.getenv('DATABASE'),
                port=os.getenv('PORT')
            )
            g.db = g.db_conn.cursor(dictionary=True)
            g.db_conn.autocommit = True
            # initialize db selection
            g.db.execute(f"USE `{os.getenv('DATABASE')}`")
            g.db.fetchall()
            return g.db
        except Exception as e:
            print('ERROR:', e)
            traceback.print_exc()
    
def close_db(e=None):
    db = g.pop('db', None)
    db_conn = g.pop('db_conn', None)

    if db is not None:
        db.fetchall()
        db.close()
    if db_conn is not None:
        db_conn.close()


def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)