from flask import Blueprint, render_template, redirect, url_for, session, flash
from app.plot.forms import PlotForm
from app.profiles import profile_required

bp = Blueprint('plot', __name__)


@bp.route('/', methods = ['GET','POST'])
@profile_required
def index():
    form = PlotForm()
    context = {
            'show_plot': False,
            'form': form,
            }
    if form.validate_on_submit():
        context['show_plot'] = True
        form.time.choices = [(1, 'hi'), (2, 'hi2')]
    return render_template('plot/index.html', **context)
