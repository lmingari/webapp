from flask import Blueprint, session
from app.extensions import db
import click

bp = Blueprint('cli', __name__, cli_group='db')
bp.cli.short_help = "Database commands."

@bp.cli.command('clean')
def initialize_database():
    """Initialize a new SQLite database."""
    db.drop_all()
    db.create_all()
    click.echo('Initialized a new SQLite database!')
