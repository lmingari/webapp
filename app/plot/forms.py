from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
from app.plot.models import PlotModel

ModelForm = model_form_factory(FlaskForm)

class PlotForm(ModelForm):
    class Meta:
        model = PlotModel

