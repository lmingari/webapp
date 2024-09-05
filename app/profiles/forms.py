from flask_wtf import FlaskForm
from wtforms_sqlalchemy.orm import model_form
from app.models import ProfileModel

ProfileForm = model_form(ProfileModel, 
                         base_class = FlaskForm, 
                         exclude = {'blocks'})
