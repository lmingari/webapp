from flask import Blueprint, render_template, redirect, url_for, flash, session

bp = Blueprint('run', __name__)

@bp.route('/')
def index():
    if not session.get("profile"):
        flash("A profile must be loaded")
        return redirect(url_for('profiles.index'))
    return render_template('run/index.html',
                           profile = session['profile'])
