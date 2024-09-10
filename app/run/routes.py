from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.models import ProfileModel

bp = Blueprint('run', __name__)

@bp.route('/')
def index():
    if not session.get("profile"):
        flash("A profile must be loaded")
        return redirect(url_for('profiles.index'))
    id = session['profile']
    p = ProfileModel.query.get_or_404(id)
    return render_template('run/index.html',
                           profile = p.title)
