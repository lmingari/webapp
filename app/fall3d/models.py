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
        self.blocks.append(METEO_DATA()) 
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
    
    
    f6 = db.Column(db.String, 
        
        info = {'label': 'RESTART_ENSEMBLE_BASEPATH'}, 
        
        default = './')
    
    

    __mapper_args__ = {
        'polymorphic_identity': 'TIME_UTC'
    }

class METEO_DATA (ConfigurationModel):
    __tablename__ = "METEO_DATA"

    id = db.Column(db.Integer, 
                   db.ForeignKey('block.id'), 
                   primary_key=True)

    
    f1 = db.Column(ChoiceType([('WRF', 'WRF'), ('GFS', 'GFS'), ('ERA5', 'ERA5'), ('ERA5ML', 'ERA5ML'), ('IFS', 'IFS'), ('CARRA', 'CARRA')]), 
        
        info = {'label': 'METEO_DATA_FORMAT'}, 
        
        default = 'WRF')
    
    
    f2 = db.Column(db.String, 
        
        info = {'label': 'METEO_DATA_DICTIONARY_FILE'}, 
        
        default = 'WRF.tbl')
    
    
    f3 = db.Column(db.String, 
        
        info = {'label': 'METEO_DATA_FILE'}, 
        
        default = 'Example-8.0.wrf.nc')
    
    
    f4 = db.Column(db.String, 
        
        info = {'label': 'METEO_ENSEMBLE_BASEPATH'}, 
        
        default = '')
    
    
    f5 = db.Column(db.String, 
        
        info = {'label': 'METEO_LEVELS_FILE'}, 
        
        default = '../Other/Meteo/Tables/L137_ECMWF.levels')
    
    
    f6 = db.Column(db.Float, 
        
        info = {'label': 'DBS_BEGIN_METEO_DATA_(HOURS_AFTER_00)'}, 
        
        default = 0)
    
    
    f7 = db.Column(db.Float, 
        
        info = {'label': 'DBS_END_METEO_DATA_(HOURS_AFTER_00)'}, 
        
        default = 24)
    
    
    f8 = db.Column(db.Float, 
        
        info = {'label': 'METEO_COUPLING_INTERVAL_(MIN)'}, 
        
        default = 60)
    
    
    f9 = db.Column(db.Integer, 
        
        info = {'label': 'MEMORY_CHUNK_SIZE'}, 
        
        default = 5)
    
    

    __mapper_args__ = {
        'polymorphic_identity': 'METEO_DATA'
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
        
        default = False)
    
    f9 = db.Column(db.Float, 
        
        info = {'label': 'none'}, 
        
        default = 0.1)
    
    
    f10 = db.Column(db.Integer, 
        
        info = {'label': 'NY'}, 
        
        default = 50)
    
    f11 = db.Column(db.Boolean, 
        
        info = {'label': 'RESOLUTION'}, 
        
        default = False)
    
    f12 = db.Column(db.Float, 
        
        info = {'label': 'none'}, 
        
        default = 0.1)
    
    
    f13 = db.Column(db.Integer, 
        
        info = {'label': 'NZ'}, 
        
        default = 10)
    
    
    f14 = db.Column(db.Float, 
        
        info = {'label': 'ZMAX_(M)'}, 
        
        default = 10000)
    
    
    f15 = db.Column(db.Float, 
        
        info = {'label': 'SIGMA_VALUES'}, 
        
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
    
    
    f7 = db.Column(db.Boolean, 
        
        info = {'label': 'CS134'}, 
        
        default = False)
    
    f8 = db.Column(db.Float, 
        
        info = {'label': 'MASS_FRACTION_(%)'}, 
        
        default = 0)
    
    
    f9 = db.Column(db.Boolean, 
        
        info = {'label': 'CS137'}, 
        
        default = False)
    
    f10 = db.Column(db.Float, 
        
        info = {'label': 'MASS_FRACTION_(%)'}, 
        
        default = 0)
    
    
    f11 = db.Column(db.Boolean, 
        
        info = {'label': 'I131'}, 
        
        default = False)
    
    f12 = db.Column(db.Float, 
        
        info = {'label': 'MASS_FRACTION_(%)'}, 
        
        default = 0)
    
    
    f13 = db.Column(db.Boolean, 
        
        info = {'label': 'SR90'}, 
        
        default = False)
    
    f14 = db.Column(db.Float, 
        
        info = {'label': 'MASS_FRACTION_(%)'}, 
        
        default = 0)
    
    
    f15 = db.Column(db.Boolean, 
        
        info = {'label': 'Y90'}, 
        
        default = False)
    
    f16 = db.Column(db.Float, 
        
        info = {'label': 'MASS_FRACTION_(%)'}, 
        
        default = 0)
    
    

    __mapper_args__ = {
        'polymorphic_identity': 'SPECIES'
    }
