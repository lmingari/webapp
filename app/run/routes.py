from flask import Blueprint, render_template, redirect, url_for, flash, session, current_app
from app.models import ProfileModel
from app.fall3d import config
from app.run.forms import RunForm
import os

bp = Blueprint('run', __name__)

@bp.route('/', methods = ["GET","POST"])
def index():
    if not session.get("profile"):
        flash("A profile must be loaded")
        return redirect(url_for('profiles.index'))
    id = session['profile']
    p = ProfileModel.query.get_or_404(id)
    run_folder = os.path.join(current_app.config['RUN_FOLDER'],p.title)
    form = RunForm()
    if form.validate_on_submit():
        if os.path.exists(run_folder):
            flash("Folder already exists")
        else:
            flash(f"Creating folder {run_folder}")
            try:
                os.makedirs(run_folder)
            except:
                return "Fatall"
        flash("Writing configuration file")
        with open(os.path.join(run_folder,"conf.inp"),"w") as f:
            parsed_template = render_template(
                    'run/config.inp',
                    sections = config)
            f.write(parsed_template)
    return render_template('run/index.html',
                           sections = config,
                           form    = form,
                           profile = p.title)
