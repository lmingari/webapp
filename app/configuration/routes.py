from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.extensions import db
from app.models import ProfileModel
from app.configuration.forms import getForm

bp = Blueprint('configuration', __name__)

@bp.route('/')
def index():
    if not session.get("profile"):
        flash("A profile must be loaded")
        return redirect(url_for('profiles.index'))
    else:
        return redirect(url_for('configuration.set'))

@bp.route('/set/<block>', methods=('GET','POST'))
@bp.route('/set', methods=('GET','POST'))
def set(block=None):
    p = ProfileModel.query.filter_by(title=session['profile']).first()
    blocks = [item.type for item in p.blocks]
    if block in blocks:
        block_obj = next(x for x in p.blocks if x.type==block)
    else:
        block_obj = p.blocks[0]
        block = block_obj.type
    form = getForm(block_obj)
    if form.validate_on_submit():
        form.populate_obj(block_obj)
        db.session.commit()
        flash(f"Updated block: {block}")
    return render_template('configuration/index.html',
                           form    = form, 
                           profile = session['profile'],
                           blocks  = blocks,
                           block   = block)
