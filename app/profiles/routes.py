from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.extensions import db
from app.models import Profiles
from app.profiles.forms import ProfileForm

bp = Blueprint('profiles', __name__)

@bp.route('/', methods=('GET','POST'))
def index():
    form = ProfileForm()
    p_all = Profiles.query.all()
    if form.validate_on_submit():
        p = Profiles()
        form.populate_obj(p)
        db.session.add(p)
        db.session.commit()
        flash(f"Added new profile: {p}")
        return redirect(url_for('profiles.index'))
    return render_template('profiles/index.html', 
                           form = form,
                           profiles = p_all)

@bp.route('/delete/<int:id>')
def delete(id):
    p = Profiles.query.get_or_404(id)
    try:
        db.session.delete(p)
        db.session.commit()
    except:
        return "Error....."
    if session.get('id')==id: 
        del session['profile']
        del session['id']
    flash(f"Deleted profile: {p}")
    return redirect(url_for('profiles.index'))

@bp.route('/load/<int:id>')
def load(id):
    p = Profiles.query.get_or_404(id)
    session["profile"] = p.label
    session["id"] = id
    flash(f"Loaded profile {p}")
    return redirect(url_for('profiles.index'))
