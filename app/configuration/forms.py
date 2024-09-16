from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory

BaseForm = model_form_factory(FlaskForm)

def getForm(obj):
    ModelClass = type(obj)
    class FormClass(BaseForm):
        class Meta:
            model = ModelClass
            exclude=['label']
    form = FormClass(obj=obj)
    return form
