from flask import Blueprint, render_template, redirect, url_for, session, flash, current_app, send_file
from app.models import Profiles
from app.plot.forms import PlotForm
from app.fall3d.post import Fall3D
from app.profiles import profile_required
from os.path import join

bp = Blueprint('plot', __name__)

fobj = None

def get_fall3d():
    global fobj
    if fobj is None:
        plabel = session['profile']
        path = join(current_app.config['RUN_FOLDER'],plabel)
        fobj = Fall3D(path,'config.res.nc')
    return fobj

@bp.route('/', methods = ['GET','POST'])
@profile_required
def index():
    form = PlotForm()
    context = { 'form': form }
    id = session['id']
    p = Profiles.query.get_or_404(id)
    f = get_fall3d()
    if f.load():
        form.f1.choices = [(i,i) for i in f.get_vars()]
        form.f2.choices = [(i,str(i)) for i in f.get_times()]
    else:
        flash("Error opening output file...")
    if form.validate_on_submit():
        f.key    = form.f1.data
        it       = form.f2.data
        f.minval = form.f3.data
        f.maxval = form.f4.data
        f.step   = form.f5.data
        f.log    = form.f6.data
        f.auto   = form.f7.data
        context['it'] = it
    return render_template('plot/index.html', **context)

@bp.route('/update/<int:it>')
def update(it):
    # Generate the plot based on the index
    buf = fobj.plot(it)
    return send_file(buf, mimetype='image/png')

@bp.route('/download/<int:it>')
def download(it):
    # Generate the plot based on the index
    buf = fobj.plot(it)
    fname = f'{fobj.key}-{it}.png'
    return send_file(buf, 
                     as_attachment=True, 
                     download_name=fname, 
                     mimetype='image/png')

