from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.extensions import db
from app.models import ProfileModel
from app.profiles.forms import ProfileForm

bp = Blueprint('profiles', __name__)

@bp.route('/', methods=('GET','POST'))
def index():
    form = ProfileForm()
    context = {
            'form': form,
            'profiles': ProfileModel.query.all(),
            'active' : session.get('profile'),
            }
    if form.validate_on_submit():
        new_row = ProfileModel()
        form.populate_obj(new_row)
        new_row.set_default()
        db.session.add(new_row)
        db.session.commit()
        flash(f"Added new profile: {new_row.title}")
        return redirect(url_for('profiles.index'))
    return render_template('profiles/index.html', **context)

@bp.route('/delete/<int:id>')
def delete(id):
    p = ProfileModel.query.get_or_404(id)
    try:
        if session.get('profile')==id: del session['profile']
        db.session.delete(p)
        db.session.commit()
        flash(f"Deleted profile: {p.title}")
        return redirect(url_for('profiles.index'))
    except:
        return "Error....."

@bp.route('/load/<int:id>')
def load(id):
    p = ProfileModel.query.get_or_404(id)
    session["profile"] = id
    flash(f"Loaded profile {p.title}")
    return redirect(url_for('profiles.index'))
