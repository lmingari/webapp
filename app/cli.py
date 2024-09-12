from flask import Blueprint
from app.extensions import db
import click

bp = Blueprint('cli', __name__, cli_group=None)

@bp.cli.command('clean_db')
def initialize_database():
    """Initialize the SQLite database."""
    db.drop_all()
    db.create_all()
    click.echo('Initialized the SQLite database!')
