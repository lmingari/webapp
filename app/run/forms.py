from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
from app.run.models import RunModel

ModelForm = model_form_factory(FlaskForm)

class RunForm(ModelForm):
    class Meta:
        model = RunModel
