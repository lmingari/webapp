from app.extensions import db
from sqlalchemy_utils import ChoiceType
import datetime

class ProfileModel(db.Model):
    __tablename__ = 'profiles'

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.Text)

    blocks      = db.relationship('ConfigurationModel',
                                  backref = 'profile')
    def set_default(self):
    
        self.blocks.append(TIME_UTC()) 
        self.blocks.append(GRID()) 
        self.blocks.append(SPECIES()) 

    def __repr__(self):
        return f'<Profile "{self.title}">'

class ConfigurationModel(db.Model):
    __tablename__ = 'block'

    id   = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    prof_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'block',
        'polymorphic_on': 'type'
    }

    def __repr__(self):
        return f'<Block "{self.type}">'


class TIME_UTC (ConfigurationModel):
    __tablename__ = "TIME_UTC"

    id = db.Column(db.Integer, 
                   db.ForeignKey('block.id'), 
                   primary_key=True)

    
    f1 = db.Column(db.Date, 
        
        info = {'label': 'DATE'}, 
        
        default = datetime.date(2008, 4, 29))
    
    
    f2 = db.Column(db.Float, 
        
        info = {'label': 'RUN_START_(HOURS_AFTER_00)'}, 
        
        default = 0)
    
    
    f3 = db.Column(db.Float, 
        
        info = {'label': 'RUN_END_(HOURS_AFTER_00)'}, 
        
        default = 10)
    
    
    f4 = db.Column(ChoiceType([('NONE', 'NONE'), ('INSERTION', 'INSERTION'), ('RESTART', 'RESTART')]), 
        
        info = {'label': 'INITIAL_CONDITION'}, 
        
        default = 'NONE')
    
    
    f5 = db.Column(db.String, 
        
        info = {'label': 'RESTART_FILE'}, 
        
        default = 'Example-8.0.rst.nc')
    
    

    __mapper_args__ = {
        'polymorphic_identity': 'TIME_UTC'
    }

class GRID (ConfigurationModel):
    __tablename__ = "GRID"

    id = db.Column(db.Integer, 
                   db.ForeignKey('block.id'), 
                   primary_key=True)

    
    f1 = db.Column(ChoiceType([('CARTESIAN', 'CARTESIAN'), ('SPHERICAL', 'SPHERICAL')]), 
        
        info = {'label': 'HORIZONTAL_MAPPING'}, 
        
        default = 'SPHERICAL')
    
    
    f2 = db.Column(ChoiceType([('SIGMA_NO_DECAY', 'SIGMA_NO_DECAY'), ('SIGMA_LINEAR_DECAY', 'SIGMA_LINEAR_DECAY'), ('SIGMA_EXPONENTIAL_DECAY', 'SIGMA_EXPONENTIAL_DECAY')]), 
        
        info = {'label': 'VERTICAL_MAPPING'}, 
        
        default = 'SIGMA_LINEAR_DECAY')
    
    
    f3 = db.Column(db.Float, 
        
        info = {'label': 'LONMIN'}, 
        
        default = 14.0)
    
    
    f4 = db.Column(db.Float, 
        
        info = {'label': 'LONMAX'}, 
        
        default = 16.0)
    
    
    f5 = db.Column(db.Float, 
        
        info = {'label': 'LATMIN'}, 
        
        default = 36.5)
    
    
    f6 = db.Column(db.Float, 
        
        info = {'label': 'LATMAX'}, 
        
        default = 38.5)
    
    
    f7 = db.Column(db.Integer, 
        
        info = {'label': 'NX'}, 
        
        default = 50)
    
    f8 = db.Column(db.Boolean, 
        
        info = {'label': 'RESOLUTION'}, 
        
        default = True)
    
    f9 = db.Column(db.Float, 
        
        info = {'label': 'none'}, 
        
        default = 0.1)
    
    
    f10 = db.Column(db.Integer, 
        
        info = {'label': 'NY'}, 
        
        default = 50)
    
    f11 = db.Column(db.Boolean, 
        
        info = {'label': 'RESOLUTION'}, 
        
        default = True)
    
    f12 = db.Column(db.Float, 
        
        info = {'label': 'none'}, 
        
        default = 0.1)
    
    
    f13 = db.Column(db.Integer, 
        
        info = {'label': 'NZ'}, 
        
        default = 10)
    
    
    f14 = db.Column(db.Float, 
        
        info = {'label': 'ZMAX_(M)'}, 
        
        default = 10000)
    
    

    __mapper_args__ = {
        'polymorphic_identity': 'GRID'
    }

class SPECIES (ConfigurationModel):
    __tablename__ = "SPECIES"

    id = db.Column(db.Integer, 
                   db.ForeignKey('block.id'), 
                   primary_key=True)

    
    f1 = db.Column(db.Boolean, 
        
        info = {'label': 'TEPHRA'}, 
        
        default = True)
    
    
    f2 = db.Column(db.Boolean, 
        
        info = {'label': 'DUST'}, 
        
        default = False)
    
    
    f3 = db.Column(db.Boolean, 
        
        info = {'label': 'H2O'}, 
        
        default = False)
    
    f4 = db.Column(db.Float, 
        
        info = {'label': 'MASS_FRACTION_(%)'}, 
        
        default = 2)
    
    
    f5 = db.Column(db.Boolean, 
        
        info = {'label': 'SO2'}, 
        
        default = True)
    
    f6 = db.Column(db.Float, 
        
        info = {'label': 'MASS_FRACTION_(%)'}, 
        
        default = 1)
    
    

    __mapper_args__ = {
        'polymorphic_identity': 'SPECIES'
    }
