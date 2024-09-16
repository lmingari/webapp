from flask import Blueprint, render_template, redirect, url_for, flash, session, current_app
from app.models import Profiles
from app.run.models import RunModel
from app.run.forms import RunForm
from app.profiles import profile_required
import os

bp = Blueprint('run', __name__)

@bp.route('/', methods = ["GET","POST"])
@profile_required
def index():
    id = session['id']
    p = Profiles.query.get_or_404(id)
    run_folder = os.path.join(current_app.config['RUN_FOLDER'],p.label)
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
        render_files(run_folder,p.sections,form)
#        res = run_script(run_folder)
    return render_template('run/index.html',
                           sections = p.sections,
                           form     = form)

def render_files(path,sections,form):
    flash("Writing configuration file")
    fname = os.path.join(path,"config.inp")
    with open(fname,"w") as f:
        parsed_template = render_template(
                'run/config.inp',
                sections = sections)
        f.write(parsed_template)

    flash("Writing launching script")
    fname = os.path.join(path,"launch.sh")
    with open(fname,"w") as f:
        parsed_template = render_template(
                'run/launch.sh',
                form = form,
                path = path)
        f.write(parsed_template)
    os.chmod(fname,0o774)

def run_script(path):
    import subprocess
    fname = os.path.join(path,"launch.sh")
    print("+++++++launching")
    flash("Running...")
    p = subprocess.Popen([fname])
    print("+++++++stop")
    return p
