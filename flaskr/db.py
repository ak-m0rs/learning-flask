'''import sqlite3
from datetime import datetime
import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

sqlite3.register_converter(
"timestamp", lambda v: datetime.fromisoformat(v.decode()))

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)'''
from datetime import datetime
import click
import mysql.connector
from mysql.connector import Error
from flask import current_app, g

def get_db():
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(
                host=current_app.config['MYSQL_HOST'],        # Correct key for host
                user=current_app.config['MYSQL_USER'],        # Correct key for user
                password=current_app.config['MYSQL_PASSWORD'], # Correct key for password
                database=current_app.config['MYSQL_DB'] 
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
    cursor = db.cursor()

    with current_app.open_resource('schema.sql') as f:
        sql_statements = f.read().decode('utf8').split(';')  # Split statements by semicolon

    for statement in sql_statements:
        statement = statement.strip()  # Remove extra whitespace
        if statement:  # Skip empty statements
            print(f"Executing SQL: {statement}")  # Debugging output
            try:
                cursor.execute(statement)
            except mysql.connector.Error as e:
                print(f"SQL execution failed: {e}")
                raise

    db.commit()
    cursor.close()

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

