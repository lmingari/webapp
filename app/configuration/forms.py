from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory

ModelForm = model_form_factory(FlaskForm)

def getForm(obj):
    ModelClass = type(obj)
    class FormClass(ModelForm):
        class Meta:
            model = ModelClass
            exclude=['type']
    form = FormClass(obj=obj)
    return form
