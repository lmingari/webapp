from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.extensions import db
from app.models import ProfileModel
from app.configuration.forms import getForm
from app.fall3d import config

bp = Blueprint('configuration', __name__)

@bp.route('/')
def index():
    if not session.get("profile"):
        flash("A profile must be loaded")
        return redirect(url_for('profiles.index'))
    id = session['profile']
    p = ProfileModel.query.get_or_404(id)
    block = p.blocks[0].type
    return redirect(url_for('configuration.set',block=block))

@bp.route('/<block>', methods=('GET','POST'))
def set(block):
    if not session.get("profile"):
        flash("A profile must be loaded")
        return redirect(url_for('profiles.index'))
    id = session['profile']
    p = ProfileModel.query.get_or_404(id)
    blocks = [item.type for item in p.blocks]
    if block in blocks:
        block_obj = next(x for x in p.blocks if x.type==block)
        form = getForm(block_obj)
    else:
        return "incorrect block"
    if form.validate_on_submit():
        form.populate_obj(block_obj)
        db.session.commit()
        flash(f"Updated block: {block}")
    return render_template('configuration/index.html',
                           form    = form, 
                           profile = p.title,
                           blocks  = blocks,
                           block   = block)
