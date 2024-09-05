
from app.extensions import db
from sqlalchemy_utils import ChoiceType

class ProfileModel(db.Model):
    __tablename__ = 'profiles'

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.Text)

    blocks      = db.relationship('ConfigurationModel',
                                  backref = 'profile')
    def set_default(self):
    
        self.blocks.append(TIME_UTC()) 
        self.blocks.append(INSERTION_DATA()) 
        self.blocks.append(METEO_DATA()) 
        self.blocks.append(GRID()) 
        self.blocks.append(SPECIES()) 
        self.blocks.append(SPECIES_TGSD()) 
        self.blocks.append(PARTICLE_AGGREGATION()) 
        self.blocks.append(SOURCE()) 
        self.blocks.append(ENSEMBLE()) 
        self.blocks.append(ENSEMBLE_POST()) 
        self.blocks.append(MODEL_PHYSICS()) 
        self.blocks.append(MODEL_OUTPUT()) 
        self.blocks.append(MODEL_VALIDATION()) 

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
    
    f1 = db.Column('YEAR', db.Integer, info = {'label': 'YEAR'}, default = 2008)
    f2 = db.Column('MONTH', db.Integer, info = {'label': 'MONTH'}, default = 4)
    f3 = db.Column('DAY', db.Integer, info = {'label': 'DAY'}, default = 29)
    f4 = db.Column('RUN_START_(HOURS_AFTER_00)', db.Float, info = {'label': 'RUN_START_(HOURS_AFTER_00)'}, default = 0)
    f5 = db.Column('RUN_END_(HOURS_AFTER_00)', db.Float, info = {'label': 'RUN_END_(HOURS_AFTER_00)'}, default = 10)
    f6 = db.Column('INITIAL_CONDITION', ChoiceType([('NONE', 'NONE'), ('INSERTION', 'INSERTION'), ('RESTART', 'RESTART')]), info = {'label': 'INITIAL_CONDITION'})
    f7 = db.Column('RESTART_FILE', db.String, info = {'label': 'RESTART_FILE'}, default = "Example-8.0.rst.nc")
    f8 = db.Column('RESTART_ENSEMBLE_BASEPATH', db.String, info = {'label': 'RESTART_ENSEMBLE_BASEPATH'}, default = "./")

    __mapper_args__ = {
        'polymorphic_identity': 'TIME_UTC'
    }

class INSERTION_DATA (ConfigurationModel):
    __tablename__ = "INSERTION_DATA"

    id = db.Column(db.Integer, 
                   db.ForeignKey('block.id'), 
                   primary_key=True)
    
    f1 = db.Column('INSERTION_FILE', db.String, info = {'label': 'INSERTION_FILE'}, default = "Example-8.0.sat.nc")
    f2 = db.Column('INSERTION_DICTIONARY_FILE', db.String, info = {'label': 'INSERTION_DICTIONARY_FILE'}, default = "Sat.tbl")
    f3 = db.Column('INSERTION_TIME_SLAB', db.Integer, info = {'label': 'INSERTION_TIME_SLAB'}, default = 4)
    f4 = db.Column('DIAMETER_CUT_OFF_(MIC)', db.Float, info = {'label': 'DIAMETER_CUT_OFF_(MIC)'}, default = 64)

    __mapper_args__ = {
        'polymorphic_identity': 'INSERTION_DATA'
    }

class METEO_DATA (ConfigurationModel):
    __tablename__ = "METEO_DATA"

    id = db.Column(db.Integer, 
                   db.ForeignKey('block.id'), 
                   primary_key=True)
    
    f1 = db.Column('METEO_DATA_FORMAT', ChoiceType([('WRF', 'WRF'), ('GFS', 'GFS'), ('ERA5', 'ERA5'), ('ERA5ML', 'ERA5ML'), ('IFS', 'IFS'), ('CARRA', 'CARRA')]), info = {'label': 'METEO_DATA_FORMAT'})
    f2 = db.Column('METEO_DATA_DICTIONARY_FILE', db.String, info = {'label': 'METEO_DATA_DICTIONARY_FILE'}, default = "WRF.tbl")
    f3 = db.Column('METEO_DATA_FILE', db.String, info = {'label': 'METEO_DATA_FILE'}, default = "Example-8.0.wrf.nc")
    f4 = db.Column('METEO_ENSEMBLE_BASEPATH', db.String, info = {'label': 'METEO_ENSEMBLE_BASEPATH'}, default = "./")
    f5 = db.Column('METEO_LEVELS_FILE', db.String, info = {'label': 'METEO_LEVELS_FILE'}, default = "ERA5.hyb")
    f6 = db.Column('DBS_BEGIN_METEO_DATA_(HOURS_AFTER_00)', db.Float, info = {'label': 'DBS_BEGIN_METEO_DATA_(HOURS_AFTER_00)'}, default = 0)
    f7 = db.Column('DBS_END_METEO_DATA_(HOURS_AFTER_00)', db.Float, info = {'label': 'DBS_END_METEO_DATA_(HOURS_AFTER_00)'}, default = 24)
    f8 = db.Column('METEO_COUPLING_INTERVAL_(MIN)', db.Float, info = {'label': 'METEO_COUPLING_INTERVAL_(MIN)'}, default = 60)
    f9 = db.Column('MEMORY_CHUNK_SIZE', db.Integer, info = {'label': 'MEMORY_CHUNK_SIZE'}, default = 5)

    __mapper_args__ = {
        'polymorphic_identity': 'METEO_DATA'
    }

class GRID (ConfigurationModel):
    __tablename__ = "GRID"

    id = db.Column(db.Integer, 
                   db.ForeignKey('block.id'), 
                   primary_key=True)
    
    f1 = db.Column('HORIZONTAL_MAPPING', ChoiceType([('CARTESIAN', 'CARTESIAN'), ('SPHERICAL', 'SPHERICAL')]), info = {'label': 'HORIZONTAL_MAPPING'})
    f2 = db.Column('VERTICAL_MAPPING', ChoiceType([('SIGMA_NO_DECAY', 'SIGMA_NO_DECAY'), ('SIGMA_LINEAR_DECAY', 'SIGMA_LINEAR_DECAY'), ('SIGMA_EXPONENTIAL_DECAY', 'SIGMA_EXPONENTIAL_DECAY')]), info = {'label': 'VERTICAL_MAPPING'})
    f3 = db.Column('LONMIN', db.Float, info = {'label': 'LONMIN'}, default = 14.0)
    f4 = db.Column('LONMAX', db.Float, info = {'label': 'LONMAX'}, default = 16.0)
    f5 = db.Column('LATMIN', db.Float, info = {'label': 'LATMIN'}, default = 36.5)
    f6 = db.Column('LATMAX', db.Float, info = {'label': 'LATMAX'}, default = 38.5)
    f7 = db.Column('NX', ChoiceType([('integer', 'integer'), ('RESOLUTION float', 'RESOLUTION float')]), info = {'label': 'NX'})
    f8 = db.Column('NY', ChoiceType([('integer', 'integer'), ('RESOLUTION float', 'RESOLUTION float')]), info = {'label': 'NY'})
    f9 = db.Column('NZ', db.Integer, info = {'label': 'NZ'}, default = 10)
    f10 = db.Column('ZMAX_(M)', db.Float, info = {'label': 'ZMAX_(M)'}, default = 10000)
    f11 = db.Column('SIGMA_VALUES', db.String, info = {'label': 'SIGMA_VALUES'}, default = "[0.0, 0.01, 0.025, 0.05, 0.1]")

    __mapper_args__ = {
        'polymorphic_identity': 'GRID'
    }

class SPECIES (ConfigurationModel):
    __tablename__ = "SPECIES"

    id = db.Column(db.Integer, 
                   db.ForeignKey('block.id'), 
                   primary_key=True)
    
    f1 = db.Column('TEPHRA', db.Boolean, info = {'label': 'TEPHRA'})
    f2 = db.Column('DUST', db.Boolean, info = {'label': 'DUST'})
    f3 = db.Column('H2O', ChoiceType([('ON MASS_FRACTION_(%) = float', 'ON MASS_FRACTION_(%) = float'), ('OFF', 'OFF')]), info = {'label': 'H2O'})
    f4 = db.Column('SO2', ChoiceType([('ON MASS_FRACTION_(%) = float', 'ON MASS_FRACTION_(%) = float'), ('OFF', 'OFF')]), info = {'label': 'SO2'})
    f5 = db.Column('CS134', ChoiceType([('ON MASS_FRACTION_(%) = float', 'ON MASS_FRACTION_(%) = float'), ('OFF', 'OFF')]), info = {'label': 'CS134'})
    f6 = db.Column('CS137', ChoiceType([('ON MASS_FRACTION_(%) = float', 'ON MASS_FRACTION_(%) = float'), ('OFF', 'OFF')]), info = {'label': 'CS137'})
    f7 = db.Column('I131', ChoiceType([('ON MASS_FRACTION_(%) = float', 'ON MASS_FRACTION_(%) = float'), ('OFF', 'OFF')]), info = {'label': 'I131'})
    f8 = db.Column('SR90', ChoiceType([('ON MASS_FRACTION_(%) = float', 'ON MASS_FRACTION_(%) = float'), ('OFF', 'OFF')]), info = {'label': 'SR90'})
    f9 = db.Column('Y90', ChoiceType([('ON MASS_FRACTION_(%) = float', 'ON MASS_FRACTION_(%) = float'), ('OFF', 'OFF')]), info = {'label': 'Y90'})

    __mapper_args__ = {
        'polymorphic_identity': 'SPECIES'
    }

class SPECIES_TGSD (ConfigurationModel):
    __tablename__ = "SPECIES_TGSD"

    id = db.Column(db.Integer, 
                   db.ForeignKey('block.id'), 
                   primary_key=True)
    
    f1 = db.Column('NUMBER_OF_BINS', db.Integer, info = {'label': 'NUMBER_OF_BINS'}, default = 6)
    f2 = db.Column('FI_RANGE', db.String, info = {'label': 'FI_RANGE'}, default = "[-2, 8]")
    f3 = db.Column('DENSITY_RANGE', db.String, info = {'label': 'DENSITY_RANGE'}, default = "[1200, 2300]")
    f4 = db.Column('SPHERICITY_RANGE', db.String, info = {'label': 'SPHERICITY_RANGE'}, default = "[0.9, 0.9]")
    f5 = db.Column('DISTRIBUTION', ChoiceType([('GAUSSIAN', 'GAUSSIAN'), ('BIGAUSSIAN', 'BIGAUSSIAN'), ('WEIBULL', 'WEIBULL'), ('BIWEIBULL', 'BIWEIBULL'), ('CUSTOM', 'CUSTOM'), ('ESTIMATE', 'ESTIMATE')]), info = {'label': 'DISTRIBUTION'})

    __mapper_args__ = {
        'polymorphic_identity': 'SPECIES_TGSD'
    }

class PARTICLE_AGGREGATION (ConfigurationModel):
    __tablename__ = "PARTICLE_AGGREGATION"

    id = db.Column(db.Integer, 
                   db.ForeignKey('block.id'), 
                   primary_key=True)
    
    f1 = db.Column('PARTICLE_CUT_OFF', ChoiceType([('NONE', 'NONE'), ('FI_LOWER_THAN float', 'FI_LOWER_THAN float'), ('FI_LARGER_THAN float', 'FI_LARGER_THAN float'), ('D_(MIC)_LARGER_THAN float', 'D_(MIC)_LARGER_THAN float'), ('D_(MIC)_LOWER_THAN float', 'D_(MIC)_LOWER_THAN float')]), info = {'label': 'PARTICLE_CUT_OFF'})
    f2 = db.Column('AGGREGATION_MODEL', ChoiceType([('NONE', 'NONE'), ('CORNELL', 'CORNELL'), ('COSTA', 'COSTA'), ('PERCENTAGE', 'PERCENTAGE')]), info = {'label': 'AGGREGATION_MODEL'})
    f3 = db.Column('NUMBER_OF_AGGREGATE_BINS', db.Integer, info = {'label': 'NUMBER_OF_AGGREGATE_BINS'}, default = 2)
    f4 = db.Column('DIAMETER_AGGREGATES_(MIC)', db.String, info = {'label': 'DIAMETER_AGGREGATES_(MIC)'}, default = "[300.0, 200.0]")
    f5 = db.Column('DENSITY_AGGREGATES_(KGM3)', db.String, info = {'label': 'DENSITY_AGGREGATES_(KGM3)'}, default = "[350.0, 250.0]")
    f6 = db.Column('PERCENTAGE_(%)', db.String, info = {'label': 'PERCENTAGE_(%)'}, default = "[20.0, 10.0]")
    f7 = db.Column('VSET_FACTOR', db.Float, info = {'label': 'VSET_FACTOR'}, default = 0.5)
    f8 = db.Column('FRACTAL_EXPONENT', db.Float, info = {'label': 'FRACTAL_EXPONENT'}, default = 2.99)

    __mapper_args__ = {
        'polymorphic_identity': 'PARTICLE_AGGREGATION'
    }

class SOURCE (ConfigurationModel):
    __tablename__ = "SOURCE"

    id = db.Column(db.Integer, 
                   db.ForeignKey('block.id'), 
                   primary_key=True)
    
    f1 = db.Column('SOURCE_TYPE', ChoiceType([('POINT', 'POINT'), ('SUZUKI', 'SUZUKI'), ('TOP-HAT', 'TOP-HAT'), ('PLUME', 'PLUME'), ('RESUSPENSION', 'RESUSPENSION')]), info = {'label': 'SOURCE_TYPE'})
    f2 = db.Column('SOURCE_START_(HOURS_AFTER_00)', db.String, info = {'label': 'SOURCE_START_(HOURS_AFTER_00)'}, default = "0")
    f3 = db.Column('SOURCE_END_(HOURS_AFTER_00)', db.String, info = {'label': 'SOURCE_END_(HOURS_AFTER_00)'}, default = "10")
    f4 = db.Column('LON_VENT', db.Float, info = {'label': 'LON_VENT'}, default = 15.0)
    f5 = db.Column('LAT_VENT', db.Float, info = {'label': 'LAT_VENT'}, default = 37.75)
    f6 = db.Column('VENT_HEIGHT_(M)', db.Float, info = {'label': 'VENT_HEIGHT_(M)'}, default = 3000.0)
    f7 = db.Column('HEIGHT_ABOVE_VENT_(M)', db.String, info = {'label': 'HEIGHT_ABOVE_VENT_(M)'}, default = "6000.0")
    f8 = db.Column('MASS_FLOW_RATE_(KGS)', ChoiceType([('float_list', 'float_list'), ('ESTIMATE-MASTIN', 'ESTIMATE-MASTIN'), ('ESTIMATE-WOODHOUSE', 'ESTIMATE-WOODHOUSE'), ('ESTIMATE-DEGRUYTER', 'ESTIMATE-DEGRUYTER')]), info = {'label': 'MASS_FLOW_RATE_(KGS)'})
    f9 = db.Column('ALFA_PLUME', db.Float, info = {'label': 'ALFA_PLUME'}, default = 0.1)
    f10 = db.Column('BETA_PLUME', db.Float, info = {'label': 'BETA_PLUME'}, default = 0.5)
    f11 = db.Column('EXIT_TEMPERATURE_(K)', db.Float, info = {'label': 'EXIT_TEMPERATURE_(K)'}, default = 1200.0)
    f12 = db.Column('EXIT_WATER_FRACTION_(%)', db.Float, info = {'label': 'EXIT_WATER_FRACTION_(%)'}, default = 0.0)

    __mapper_args__ = {
        'polymorphic_identity': 'SOURCE'
    }

class ENSEMBLE (ConfigurationModel):
    __tablename__ = "ENSEMBLE"

    id = db.Column(db.Integer, 
                   db.ForeignKey('block.id'), 
                   primary_key=True)
    
    f1 = db.Column('RANDOM_NUMBERS_FROM_FILE', db.Boolean, info = {'label': 'RANDOM_NUMBERS_FROM_FILE'})
    f2 = db.Column('PERTURBATE_COLUMN_HEIGHT', ChoiceType([('NO', 'NO'), ('RELATIVE', 'RELATIVE'), ('ABSOLUTE', 'ABSOLUTE')]), info = {'label': 'PERTURBATE_COLUMN_HEIGHT'})
    f3 = db.Column('PERTURBATE_MASS_FLOW_RATE', ChoiceType([('NO', 'NO'), ('RELATIVE', 'RELATIVE'), ('ABSOLUTE', 'ABSOLUTE')]), info = {'label': 'PERTURBATE_MASS_FLOW_RATE'})
    f4 = db.Column('PERTURBATE_SOURCE_START', ChoiceType([('NO', 'NO'), ('RELATIVE', 'RELATIVE'), ('ABSOLUTE', 'ABSOLUTE')]), info = {'label': 'PERTURBATE_SOURCE_START'})
    f5 = db.Column('PERTURBATE_SOURCE_DURATION', ChoiceType([('NO', 'NO'), ('RELATIVE', 'RELATIVE'), ('ABSOLUTE', 'ABSOLUTE')]), info = {'label': 'PERTURBATE_SOURCE_DURATION'})
    f6 = db.Column('PERTURBATE_TOP-HAT_THICKNESS', ChoiceType([('NO', 'NO'), ('RELATIVE', 'RELATIVE'), ('ABSOLUTE', 'ABSOLUTE')]), info = {'label': 'PERTURBATE_TOP-HAT_THICKNESS'})
    f7 = db.Column('PERTURBATE_SUZUKI_A', ChoiceType([('NO', 'NO'), ('RELATIVE', 'RELATIVE'), ('ABSOLUTE', 'ABSOLUTE')]), info = {'label': 'PERTURBATE_SUZUKI_A'})
    f8 = db.Column('PERTURBATE_SUZUKI_L', ChoiceType([('NO', 'NO'), ('RELATIVE', 'RELATIVE'), ('ABSOLUTE', 'ABSOLUTE')]), info = {'label': 'PERTURBATE_SUZUKI_L'})
    f9 = db.Column('PERTURBATE_WIND', ChoiceType([('NO', 'NO'), ('RELATIVE', 'RELATIVE'), ('ABSOLUTE', 'ABSOLUTE')]), info = {'label': 'PERTURBATE_WIND'})
    f10 = db.Column('PERTURBATE_DATA_INSERTION_CLOUD_HEIGHT', ChoiceType([('NO', 'NO'), ('RELATIVE', 'RELATIVE'), ('ABSOLUTE', 'ABSOLUTE')]), info = {'label': 'PERTURBATE_DATA_INSERTION_CLOUD_HEIGHT'})
    f11 = db.Column('PERTURBATE_DATA_INSERTION_CLOUD_THICKNESS', ChoiceType([('NO', 'NO'), ('RELATIVE', 'RELATIVE'), ('ABSOLUTE', 'ABSOLUTE')]), info = {'label': 'PERTURBATE_DATA_INSERTION_CLOUD_THICKNESS'})
    f12 = db.Column('PERTURBATE_FI_MEAN', ChoiceType([('NO', 'NO'), ('RELATIVE', 'RELATIVE'), ('ABSOLUTE', 'ABSOLUTE')]), info = {'label': 'PERTURBATE_FI_MEAN'})
    f13 = db.Column('PERTURBATE_DIAMETER_AGGREGATES_(MIC)', ChoiceType([('NO', 'NO'), ('RELATIVE', 'RELATIVE'), ('ABSOLUTE', 'ABSOLUTE')]), info = {'label': 'PERTURBATE_DIAMETER_AGGREGATES_(MIC)'})
    f14 = db.Column('PERTURBATE_DENSITY_AGGREGATES', ChoiceType([('NO', 'NO'), ('RELATIVE', 'RELATIVE'), ('ABSOLUTE', 'ABSOLUTE')]), info = {'label': 'PERTURBATE_DENSITY_AGGREGATES'})

    __mapper_args__ = {
        'polymorphic_identity': 'ENSEMBLE'
    }

class ENSEMBLE_POST (ConfigurationModel):
    __tablename__ = "ENSEMBLE_POST"

    id = db.Column(db.Integer, 
                   db.ForeignKey('block.id'), 
                   primary_key=True)
    
    f1 = db.Column('POSTPROCESS_MEMBERS', db.Boolean, info = {'label': 'POSTPROCESS_MEMBERS'})
    f2 = db.Column('POSTPROCESS_MEAN', db.Boolean, info = {'label': 'POSTPROCESS_MEAN'})
    f3 = db.Column('POSTPROCESS_LOGMEAN', db.Boolean, info = {'label': 'POSTPROCESS_LOGMEAN'})
    f4 = db.Column('POSTPROCESS_MEDIAN', db.Boolean, info = {'label': 'POSTPROCESS_MEDIAN'})
    f5 = db.Column('POSTPROCESS_STANDARD_DEV', db.Boolean, info = {'label': 'POSTPROCESS_STANDARD_DEV'})
    f6 = db.Column('POSTPROCESS_PROBABILITY', db.Boolean, info = {'label': 'POSTPROCESS_PROBABILITY'})
    f7 = db.Column('POSTPROCESS_PERCENTILES', db.Boolean, info = {'label': 'POSTPROCESS_PERCENTILES'})

    __mapper_args__ = {
        'polymorphic_identity': 'ENSEMBLE_POST'
    }

class MODEL_PHYSICS (ConfigurationModel):
    __tablename__ = "MODEL_PHYSICS"

    id = db.Column(db.Integer, 
                   db.ForeignKey('block.id'), 
                   primary_key=True)
    
    f1 = db.Column('LIMITER', ChoiceType([('MINMOD', 'MINMOD'), ('SUPERBEE', 'SUPERBEE'), ('OSPRE', 'OSPRE')]), info = {'label': 'LIMITER'})
    f2 = db.Column('TIME_MARCHING', ChoiceType([('EULER', 'EULER'), ('RUNGE-KUTTA', 'RUNGE-KUTTA')]), info = {'label': 'TIME_MARCHING'})
    f3 = db.Column('CFL_CRITERION', ChoiceType([('ONE_DIMENSIONAL', 'ONE_DIMENSIONAL'), ('ALL_DIMENSIONS', 'ALL_DIMENSIONS')]), info = {'label': 'CFL_CRITERION'})
    f4 = db.Column('CFL_SAFETY_FACTOR', db.Float, info = {'label': 'CFL_SAFETY_FACTOR'}, default = 0.9)
    f5 = db.Column('TERMINAL_VELOCITY_MODEL', ChoiceType([('ARASTOOPOUR', 'ARASTOOPOUR'), ('GANSER', 'GANSER'), ('WILSON', 'WILSON'), ('DELLINO', 'DELLINO'), ('PFEIFFER', 'PFEIFFER'), ('DIOGUARDI2017', 'DIOGUARDI2017'), ('DIOGUARDI2018', 'DIOGUARDI2018')]), info = {'label': 'TERMINAL_VELOCITY_MODEL'})
    f6 = db.Column('HORIZONTAL_TURBULENCE_MODEL', ChoiceType([('CONSTANT float', 'CONSTANT float'), ('CMAQ', 'CMAQ'), ('RAMS', 'RAMS')]), info = {'label': 'HORIZONTAL_TURBULENCE_MODEL'})
    f7 = db.Column('VERTICAL_TURBULENCE_MODEL', ChoiceType([('CONSTANT float', 'CONSTANT float'), ('SIMILARITY', 'SIMILARITY')]), info = {'label': 'VERTICAL_TURBULENCE_MODEL'})
    f8 = db.Column('RAMS_CS', db.Float, info = {'label': 'RAMS_CS'}, default = 0.2275)
    f9 = db.Column('WET_DEPOSITION', db.Boolean, info = {'label': 'WET_DEPOSITION'})
    f10 = db.Column('DRY_DEPOSITION', db.Boolean, info = {'label': 'DRY_DEPOSITION'})
    f11 = db.Column('GRAVITY_CURRENT', db.Boolean, info = {'label': 'GRAVITY_CURRENT'})

    __mapper_args__ = {
        'polymorphic_identity': 'MODEL_PHYSICS'
    }

class MODEL_OUTPUT (ConfigurationModel):
    __tablename__ = "MODEL_OUTPUT"

    id = db.Column(db.Integer, 
                   db.ForeignKey('block.id'), 
                   primary_key=True)
    
    f1 = db.Column('PARALLEL_IO', db.Boolean, info = {'label': 'PARALLEL_IO'})
    f2 = db.Column('LOG_FILE_LEVEL', ChoiceType([('NONE', 'NONE'), ('NORMAL', 'NORMAL'), ('FULL', 'FULL')]), info = {'label': 'LOG_FILE_LEVEL'})
    f3 = db.Column('RESTART_TIME_INTERVAL_(HOURS)', ChoiceType([('float', 'float'), ('NONE', 'NONE'), ('END_ONLY', 'END_ONLY')]), info = {'label': 'RESTART_TIME_INTERVAL_(HOURS)'})
    f4 = db.Column('OUTPUT_JSON_FILES', db.Boolean, info = {'label': 'OUTPUT_JSON_FILES'})
    f5 = db.Column('OUTPUT_INTERMEDIATE_FILES', db.Boolean, info = {'label': 'OUTPUT_INTERMEDIATE_FILES'})
    f6 = db.Column('OUTPUT_TIME_START_(HOURS)', ChoiceType([('float', 'float'), ('RUN_START', 'RUN_START')]), info = {'label': 'OUTPUT_TIME_START_(HOURS)'})
    f7 = db.Column('OUTPUT_TIME_INTERVAL_(HOURS)', db.Float, info = {'label': 'OUTPUT_TIME_INTERVAL_(HOURS)'}, default = 1.0)
    f8 = db.Column('OUTPUT_3D_CONCENTRATION', db.Boolean, info = {'label': 'OUTPUT_3D_CONCENTRATION'})
    f9 = db.Column('OUTPUT_3D_CONCENTRATION_BINS', db.Boolean, info = {'label': 'OUTPUT_3D_CONCENTRATION_BINS'})
    f10 = db.Column('OUTPUT_SURFACE_CONCENTRATION', db.Boolean, info = {'label': 'OUTPUT_SURFACE_CONCENTRATION'})
    f11 = db.Column('OUTPUT_COLUMN_LOAD', db.Boolean, info = {'label': 'OUTPUT_COLUMN_LOAD'})
    f12 = db.Column('OUTPUT_CLOUD_TOP', db.Boolean, info = {'label': 'OUTPUT_CLOUD_TOP'})
    f13 = db.Column('OUTPUT_GROUND_LOAD', db.Boolean, info = {'label': 'OUTPUT_GROUND_LOAD'})
    f14 = db.Column('OUTPUT_GROUND_LOAD_BINS', db.Boolean, info = {'label': 'OUTPUT_GROUND_LOAD_BINS'})
    f15 = db.Column('OUTPUT_WET_DEPOSITION', db.Boolean, info = {'label': 'OUTPUT_WET_DEPOSITION'})
    f16 = db.Column('TRACK_POINTS', db.Boolean, info = {'label': 'TRACK_POINTS'})
    f17 = db.Column('TRACK_POINTS_FILE', db.String, info = {'label': 'TRACK_POINTS_FILE'}, default = "my_file.pts")
    f18 = db.Column('OUTPUT_CONCENTRATION_AT_XCUTS', db.Boolean, info = {'label': 'OUTPUT_CONCENTRATION_AT_XCUTS'})
    f19 = db.Column('OUTPUT_CONCENTRATION_AT_YCUTS', db.Boolean, info = {'label': 'OUTPUT_CONCENTRATION_AT_YCUTS'})
    f20 = db.Column('OUTPUT_CONCENTRATION_AT_ZCUTS', db.Boolean, info = {'label': 'OUTPUT_CONCENTRATION_AT_ZCUTS'})
    f21 = db.Column('OUTPUT_CONCENTRATION_AT_FL', db.Boolean, info = {'label': 'OUTPUT_CONCENTRATION_AT_FL'})
    f22 = db.Column('X-VALUES', db.String, info = {'label': 'X-VALUES'}, default = "15")
    f23 = db.Column('Y-VALUES', db.String, info = {'label': 'Y-VALUES'}, default = "37.5")
    f24 = db.Column('Z-VALUES', db.String, info = {'label': 'Z-VALUES'}, default = "[5000, 10000, 15000]")
    f25 = db.Column('FL-VALUES', db.String, info = {'label': 'FL-VALUES'}, default = "[50, 100, 150, 200, 250, 300, 350, 400]")

    __mapper_args__ = {
        'polymorphic_identity': 'MODEL_OUTPUT'
    }

class MODEL_VALIDATION (ConfigurationModel):
    __tablename__ = "MODEL_VALIDATION"

    id = db.Column(db.Integer, 
                   db.ForeignKey('block.id'), 
                   primary_key=True)
    
    f1 = db.Column('OBSERVATIONS_TYPE', ChoiceType([('SATELLITE_DETECTION', 'SATELLITE_DETECTION'), ('SATELLITE_RETRIEVAL', 'SATELLITE_RETRIEVAL'), ('DEPOSIT_CONTOURS', 'DEPOSIT_CONTOURS'), ('DEPOSIT_POINTS', 'DEPOSIT_POINTS')]), info = {'label': 'OBSERVATIONS_TYPE'})
    f2 = db.Column('OBSERVATIONS_FILE', db.String, info = {'label': 'OBSERVATIONS_FILE'}, default = "Example-8.0.sat.nc")
    f3 = db.Column('OBSERVATIONS_DICTIONARY_FILE', db.String, info = {'label': 'OBSERVATIONS_DICTIONARY_FILE'}, default = "Sat.tbl")
    f4 = db.Column('RESULTS_FILE', db.String, info = {'label': 'RESULTS_FILE'}, default = "Example.ens.nc")

    __mapper_args__ = {
        'polymorphic_identity': 'MODEL_VALIDATION'
    }
