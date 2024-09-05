#from flask_wtf import FlaskForm
#from wtforms_sqlalchemy.orm import model_form
#
#def getForm(obj):
#    ModelClass = type(obj)
#    FormClass = model_form(ModelClass,
#                      base_class = FlaskForm,
#                      exclude=['profile','type'] )
#    form = FormClass(obj=obj)
#    return form

#from flask.ext.wtf import Form
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
