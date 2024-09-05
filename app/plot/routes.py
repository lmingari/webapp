from flask import Blueprint, render_template, redirect, url_for, session, flash
from app.plot.forms import PlotForm

bp = Blueprint('plot', __name__)


@bp.route('/', methods = ['GET','POST'])
def index():
    if not session.get("profile"):
        flash("A profile must be loaded")
        return redirect(url_for('profiles.index'))
    form = PlotForm()
    form.time.choices = [(1, 'hi'), (2, 'hi2')]
    context = {
            'show_plot': False,
            'form': form,
            }
    if form.validate_on_submit():
        context['show_plot'] = True
    return render_template('plot/index.html', **context)
