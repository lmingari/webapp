from flask import current_app
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms_alchemy import model_form_factory
from app.models import Profiles
import pandas as pd

# Initialize an empty list to store choices
choices_list = []

def load_choices():
    global choices_list
    if not choices_list:
        with current_app.open_resource('static/volcano_list.pkl') as f:
            df = pd.read_pickle(f)
        choices_list = [("","")]
        choices_list += [(index, row['Volcano Name']) for index, row in df.iterrows()]
    return choices_list

BaseForm = model_form_factory(FlaskForm)

class ProfileForm(BaseForm):
    class Meta:
        model = Profiles

    volcano = SelectField(u'Volcano')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # Populate the choices using the cached choices
        self.volcano.choices = load_choices()
        self._fields.move_to_end('volcano')
