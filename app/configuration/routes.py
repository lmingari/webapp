from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.extensions import db
from app.models import Profiles
from app.configuration.forms import getForm
from app.profiles import profile_required

bp = Blueprint('configuration', __name__)

@bp.route('/')
@profile_required
def index():
    id = session['id']
    p = Profiles.query.get_or_404(id)
    s = p.sections[0].label
    return redirect(url_for('configuration.set',section=s))

@bp.route('/<section>', methods=('GET','POST'))
def set(section):
    id = session['id']
    p = Profiles.query.get_or_404(id)
    sdic = {s.label: s for s in p.sections}
    sobj = sdic.get(section)
    if sobj is None:
        return "Error: not found section"
    form = getForm(sobj)
    if form.validate_on_submit():
        form.populate_obj(sobj)
        db.session.commit()
        flash(f"Updated section: {section}")
    return render_template('configuration/index.html',
                           form     = form, 
                           slabels  = sdic.keys(),
                           sobj     = sobj,
                           sactive  = section,
                           )
