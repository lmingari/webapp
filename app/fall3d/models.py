from flask import session
from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, reconstructor, relationship
from app.extensions import db
from typing import Optional, List
from datetime import date

class Profiles(db.Model):
    id: Mapped[int]    = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(unique=True, 
                                       nullable=False, 
                                       info={'label': 'Label'})
    description: Mapped[Optional[str]] = mapped_column(db.Text, 
                                       info={'label': 'Description'})

    sections: Mapped[List['Sections']] = relationship(back_populates='profile', cascade='all, delete')

    def __str__(self):
        return self.label

    def __repr__(self):
        return '<Profile {}>'.format(self.label)

class SectionBase(db.Model):
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_on_load()

    @reconstructor
    def init_on_load(self):
        self._vars = {}
        seen = set()
        for col in self.__table__.columns:
            variable = col.info.get('variable',None)
            block    = col.info.get('block',None)
            index    = (variable,block)
            if variable is None: continue
            if index not in seen:
                seen.add(index)
                self._vars[index] = []
            self._vars[index].append(col.name)

            label = col.info.get('label',None)
            if label is None: col.info['label'] = "None"

            options = col.info.get('options',None)
            if not options is None:
                col.info['choices'] = [(o,o) for o in options]

    def _fmt_col(self,label,value):
        if not value is None:
            if isinstance(value,bool):
                if value:
                    value_fmt = "ON"
                else:
                    value_fmt = "OFF"
            else:
                value_fmt = f"{value}"

        if label == "None": label = None

        if label is None and value is None:
            return None
        elif label is None:
            return f"{value_fmt}"
        elif value is None:
            return f"{label}"
        else:
            return f"{label} {value_fmt}"

    def _fmt_var(self,index):
        (variable,block) = index
        strings=[]
        for scol in self._vars[index]:
            lcol = self.__table__.columns[scol].info.get('label',None)
            vcol = getattr(self,scol,None)
            strings.append(self._fmt_col(lcol,vcol))
        value = " ".join([s for s in strings if not s is None])
        return f"{variable} = {value}"

    def __str__(self):
        output = []
        seen = {None}
        for index in self._vars:
            (var,block) = index
            tab = " "*3
            if block not in seen:
                seen.add(block)
                output += ["",tab+block]
            if not block is None: tab = " "*6
            for line in self._fmt_var(index).splitlines():
                output.append(tab+line)
        return "\n".join(output)

    @property
    def vars(self):
        return self._vars

class Sections(SectionBase):
    id:      Mapped[int] = mapped_column(primary_key=True)
    label:   Mapped[str] 
    
    p_id:    Mapped[int] = mapped_column(ForeignKey(Profiles.id), index=True)
    profile: Mapped[Profiles] = relationship(back_populates='sections')

    __mapper_args__ = {
        'polymorphic_identity': 'sections',
        'polymorphic_on': 'label'
    }


class SectionTime (Sections):
    __tablename__ = "TIME_UTC"
    __mapper_args__ = {
        'polymorphic_identity': 'TIME_UTC'
    }

    description = "This block defines variables related to date and time. It is used by FALL3D, SetDbs, and SetSrc tasks"

    id: Mapped[int] = mapped_column(ForeignKey(Sections.id),primary_key=True)
    
    f1: Mapped[date] = mapped_column(default = date(2008,4,29), info = {'variable': "DATE",    })
    f2: Mapped[float] = mapped_column(default = 0, info = {'variable': "RUN_START_(HOURS_AFTER_00)",    })
    f3: Mapped[float] = mapped_column(default = 24, info = {'variable': "RUN_END_(HOURS_AFTER_00)",    })
    f4: Mapped[str] = mapped_column(default = 'NONE', info = {'variable': "INITIAL_CONDITION",    'options': ['NONE', 'INSERTION', 'RESTART'] })
    f5: Mapped[str] = mapped_column(default = 'Example-8.0.rst.nc', info = {'variable': "RESTART_FILE",    })
    f6: Mapped[str] = mapped_column(default = './', info = {'variable': "RESTART_ENSEMBLE_BASEPATH",    })
    
    

    def _fmt_var(self,index):
        if index ==('DATE',None):
            return getattr(self,'f1').strftime("YEAR = %Y\nMONTH = %m\nDAY = %d")
        return super()._fmt_var(index)



class SectionMeteo (Sections):
    __tablename__ = "METEO_DATA"
    __mapper_args__ = {
        'polymorphic_identity': 'METEO_DATA'
    }

    description = "This block defines variables related to the input meteorological dataset. It is read by the SetDbs task"

    id: Mapped[int] = mapped_column(ForeignKey(Sections.id),primary_key=True)
    
    f1: Mapped[str] = mapped_column(default = 'WRF', info = {'variable': "METEO_DATA_FORMAT",    'options': ['WRF', 'GFS', 'ERA5', 'ERA5ML', 'IFS', 'CARRA'] })
    f2: Mapped[str] = mapped_column(default = 'WRF.tbl', info = {'variable': "METEO_DATA_DICTIONARY_FILE",    })
    f3: Mapped[str] = mapped_column(default = 'Example-8.0.wrf.nc', info = {'variable': "METEO_DATA_FILE",    })
    f4: Mapped[str] = mapped_column(default = '', info = {'variable': "METEO_ENSEMBLE_BASEPATH",    })
    f5: Mapped[str] = mapped_column(default = '../Other/Meteo/Tables/L137_ECMWF.levels', info = {'variable': "METEO_LEVELS_FILE",    })
    f6: Mapped[float] = mapped_column(default = 0, info = {'variable': "DBS_BEGIN_METEO_DATA_(HOURS_AFTER_00)",    })
    f7: Mapped[float] = mapped_column(default = 24, info = {'variable': "DBS_END_METEO_DATA_(HOURS_AFTER_00)",    })
    f8: Mapped[float] = mapped_column(default = 60, info = {'variable': "METEO_COUPLING_INTERVAL_(MIN)",    })
    f9: Mapped[int] = mapped_column(default = 5, info = {'variable': "MEMORY_CHUNK_SIZE",    })
    
    



class SectionGrid (Sections):
    __tablename__ = "GRID"
    __mapper_args__ = {
        'polymorphic_identity': 'GRID'
    }

    description = "This block defines the grid variables needed by the SetDbs and FALL3D tasks"

    id: Mapped[int] = mapped_column(ForeignKey(Sections.id),primary_key=True)
    
    f1: Mapped[str] = mapped_column(default = 'SPHERICAL', info = {'variable': "HORIZONTAL_MAPPING",    'options': ['CARTESIAN', 'SPHERICAL'] })
    f2: Mapped[str] = mapped_column(default = 'SIGMA_LINEAR_DECAY', info = {'variable': "VERTICAL_MAPPING",    'options': ['SIGMA_NO_DECAY', 'SIGMA_LINEAR_DECAY', 'SIGMA_EXPONENTIAL_DECAY'] })
    f3: Mapped[float] = mapped_column(default = 14.0, info = {'variable': "LONMIN",    })
    f4: Mapped[float] = mapped_column(default = 16.0, info = {'variable': "LONMAX",    })
    f5: Mapped[float] = mapped_column(default = 36.5, info = {'variable': "LATMIN",    })
    f6: Mapped[float] = mapped_column(default = 38.5, info = {'variable': "LATMAX",    })
    f7: Mapped[int] = mapped_column(default = 50, info = {'variable': "NX",    })
    f8: Mapped[bool] = mapped_column(default = False, info = {'variable': "NX",  'label': "RESOLUTION"    })
    f9: Mapped[float] = mapped_column(default = 0.1, info = {'variable': "NX",    })
    f10: Mapped[int] = mapped_column(default = 50, info = {'variable': "NY",    })
    f11: Mapped[bool] = mapped_column(default = False, info = {'variable': "NY",  'label': "RESOLUTION"    })
    f12: Mapped[float] = mapped_column(default = 0.1, info = {'variable': "NY",    })
    f13: Mapped[int] = mapped_column(default = 10, info = {'variable': "NZ",    })
    f14: Mapped[float] = mapped_column(default = 10000, info = {'variable': "ZMAX_(M)",    })
    f15: Mapped[str] = mapped_column(default = '', info = {'variable': "SIGMA_VALUES",    })
    
    

    def _fmt_var(self,index):
        if index == ('NX',None):
            if self.f8:
                value = f"RESOLUTION {self.f9}"
            else:
                value = f"{self.f7}"
            return f"NX = {value}"
        elif index == ('NY',None):
            if self.f11:
                value = f"RESOLUTION {self.f12}"
            else:
                value = f"{self.f10}"
            return f"NY = {value}"
        return super()._fmt_var(index)



class SectionSpecies (Sections):
    __tablename__ = "SPECIES"
    __mapper_args__ = {
        'polymorphic_identity': 'SPECIES'
    }

    description = "This block is used by FALL3D, SetTgsd, and SetSrc tasks and defines which species are modeled"

    id: Mapped[int] = mapped_column(ForeignKey(Sections.id),primary_key=True)
    
    f1: Mapped[bool] = mapped_column(default = True, info = {'variable': "TEPHRA",    })
    f2: Mapped[bool] = mapped_column(default = False, info = {'variable': "DUST",    })
    f3: Mapped[bool] = mapped_column(default = False, info = {'variable': "H2O",    })
    f4: Mapped[float] = mapped_column(default = 2, info = {'variable': "H2O",  'label': "MASS_FRACTION_(%)"    })
    f5: Mapped[bool] = mapped_column(default = True, info = {'variable': "SO2",    })
    f6: Mapped[float] = mapped_column(default = 1, info = {'variable': "SO2",  'label': "MASS_FRACTION_(%)"    })
    f7: Mapped[bool] = mapped_column(default = False, info = {'variable': "CS134",    })
    f8: Mapped[float] = mapped_column(default = 0, info = {'variable': "CS134",  'label': "MASS_FRACTION_(%)"    })
    f9: Mapped[bool] = mapped_column(default = False, info = {'variable': "CS137",    })
    f10: Mapped[float] = mapped_column(default = 0, info = {'variable': "CS137",  'label': "MASS_FRACTION_(%)"    })
    f11: Mapped[bool] = mapped_column(default = False, info = {'variable': "I131",    })
    f12: Mapped[float] = mapped_column(default = 0, info = {'variable': "I131",  'label': "MASS_FRACTION_(%)"    })
    f13: Mapped[bool] = mapped_column(default = False, info = {'variable': "SR90",    })
    f14: Mapped[float] = mapped_column(default = 0, info = {'variable': "SR90",  'label': "MASS_FRACTION_(%)"    })
    f15: Mapped[bool] = mapped_column(default = False, info = {'variable': "Y90",    })
    f16: Mapped[float] = mapped_column(default = 0, info = {'variable': "Y90",  'label': "MASS_FRACTION_(%)"    })
    
    



class SectionTGSD (Sections):
    __tablename__ = "TEPHRA_TGSD"
    __mapper_args__ = {
        'polymorphic_identity': 'TEPHRA_TGSD'
    }

    description = "These blocks define the TGSD for each species and are used by the SetTgsd task to generate some basic distributions"

    id: Mapped[int] = mapped_column(ForeignKey(Sections.id),primary_key=True)
    
    f1: Mapped[int] = mapped_column(default = 6, info = {'variable': "NUMBER_OF_BINS",    })
    f2: Mapped[str] = mapped_column(default = '-2 8', info = {'variable': "FI_RANGE",    })
    f3: Mapped[str] = mapped_column(default = '1200 2300', info = {'variable': "DENSITY_RANGE",    })
    f4: Mapped[str] = mapped_column(default = '0.9 0.9', info = {'variable': "SPHERICITY_RANGE",    })
    f5: Mapped[str] = mapped_column(default = 'GAUSSIAN', info = {'variable': "DISTRIBUTION",    'options': ['GAUSSIAN', 'BIGAUSSIAN', 'WEIBULL', 'BIWEIBULL', 'CUSTOM', 'ESTIMATE'] })
    f6: Mapped[float] = mapped_column(default = 2.5, info = {'variable': "FI_MEAN",   'block': "IF_GAUSSIAN",   })
    f7: Mapped[float] = mapped_column(default = 1.5, info = {'variable': "FI_DISP",   'block': "IF_GAUSSIAN",   })
    f8: Mapped[str] = mapped_column(default = '0.25 0.75', info = {'variable': "FI_MEAN",   'block': "IF_BIGAUSSIAN",   })
    f9: Mapped[str] = mapped_column(default = '1.44 1.46', info = {'variable': "FI_DISP",   'block': "IF_BIGAUSSIAN",   })
    f10: Mapped[float] = mapped_column(default = 0.5, info = {'variable': "MIXING_FACTOR",   'block': "IF_BIGAUSSIAN",   })
    
    



class SectionAggregation (Sections):
    __tablename__ = "PARTICLE_AGGREGATION"
    __mapper_args__ = {
        'polymorphic_identity': 'PARTICLE_AGGREGATION'
    }

    description = "This block is used by task SetSrc and controls particle aggregation and cut-off (for categories particles and radionuclides only)"

    id: Mapped[int] = mapped_column(ForeignKey(Sections.id),primary_key=True)
    
    f1: Mapped[str] = mapped_column(default = 'NONE', info = {'variable': "PARTICLE_CUT_OFF",    'options': ['NONE', 'FI_LOWER_THAN', 'FI_LARGER_THAN', 'D_(MIC)_LARGER_THAN', 'D_(MIC)_LOWER_THAN'] })
    f2: Mapped[float] = mapped_column(default = 1.0, info = {'variable': "PARTICLE_CUT_OFF",    })
    f3: Mapped[str] = mapped_column(default = 'PERCENTAGE', info = {'variable': "AGGREGATION_MODEL",    'options': ['NONE', 'CORNELL', 'COSTA', 'PERCENTAGE'] })
    f4: Mapped[int] = mapped_column(default = 2, info = {'variable': "NUMBER_OF_AGGREGATE_BINS",    })
    f5: Mapped[str] = mapped_column(default = '300. 200.', info = {'variable': "DIAMETER_AGGREGATES_(MIC)",    })
    f6: Mapped[str] = mapped_column(default = '350. 250.', info = {'variable': "DENSITY_AGGREGATES_(KGM3)",    })
    f7: Mapped[str] = mapped_column(default = '20. 10.', info = {'variable': "PERCENTAGE_(%)",    })
    f8: Mapped[float] = mapped_column(default = '0.5', info = {'variable': "VSET_FACTOR",    })
    f9: Mapped[float] = mapped_column(default = '2.99', info = {'variable': "FRACTAL_EXPONENT",    })
    
    

    def _fmt_var(self,index):
        if index == ('PARTICLE_CUT_OFF',None) and self.f1 == 'NONE':
            return "PARTICLE_CUT_OFF = NONE"
        return super()._fmt_var(index)



class SectionSource (Sections):
    __tablename__ = "SOURCE"
    __mapper_args__ = {
        'polymorphic_identity': 'SOURCE'
    }

    description = "This block defines the variables needed by the SetSrc task to generate the source term for the emission phases"

    id: Mapped[int] = mapped_column(ForeignKey(Sections.id),primary_key=True)
    
    f1: Mapped[str] = mapped_column(default = 'TOP-HAT', info = {'variable': "SOURCE_TYPE",    'options': ['POINT', 'SUZUKI', 'TOP-HAT', 'PLUME'] })
    f2: Mapped[str] = mapped_column(default = '0  12', info = {'variable': "SOURCE_START_(HOURS_AFTER_00)",    })
    f3: Mapped[str] = mapped_column(default = '10 24', info = {'variable': "SOURCE_END_(HOURS_AFTER_00)",    })
    f4: Mapped[float] = mapped_column(default = 15.0, info = {'variable': "LON_VENT",    })
    f5: Mapped[float] = mapped_column(default = 37.75, info = {'variable': "LAT_VENT",    })
    f6: Mapped[float] = mapped_column(default = 3000.0, info = {'variable': "VENT_HEIGHT_(M)",    })
    f7: Mapped[float] = mapped_column(default = 6000.0, info = {'variable': "HEIGHT_ABOVE_VENT_(M)",    })
    f8: Mapped[str] = mapped_column(default = 'ESTIMATE-MASTIN', info = {'variable': "MASS_FLOW_RATE_(KGS)",    'options': ['value', 'ESTIMATE-MASTIN', 'ESTIMATE-WOODHOUSE', 'ESTIMATE-DEGRUYTER'] })
    f9: Mapped[float] = mapped_column(default = 10000000.0, info = {'variable': "MASS_FLOW_RATE_(KGS)",    })
    f10: Mapped[float] = mapped_column(default = 0.1, info = {'variable': "ALFA_PLUME",    })
    f11: Mapped[float] = mapped_column(default = 0.5, info = {'variable': "BETA_PLUME",    })
    f12: Mapped[float] = mapped_column(default = 1200.0, info = {'variable': "EXIT_TEMPERATURE_(K)",    })
    f13: Mapped[float] = mapped_column(default = 0.0, info = {'variable': "EXIT_WATER_FRACTION_(%)",    })
    f14: Mapped[str] = mapped_column(default = '4. 5.', info = {'variable': "A",   'block': "IF_SUZUKI_SOURCE",   })
    f15: Mapped[str] = mapped_column(default = '5.', info = {'variable': "L",   'block': "IF_SUZUKI_SOURCE",   })
    f16: Mapped[float] = mapped_column(default = 2000.0, info = {'variable': "THICKNESS_(M)",   'block': "IF_TOP-HAT_SOURCE",   })
    
    

    def _fmt_var(self,index):
        if 'f8' in self.vars[index]:
            if self.f8 == 'value':
                return f"MASS_FLOW_RATE_(KGS) = {self.f9}"
            else:
                return f"MASS_FLOW_RATE_(KGS) = {self.f8}"
        return super()._fmt_var(index)



class SectionPhysics (Sections):
    __tablename__ = "MODEL_PHYSICS"
    __mapper_args__ = {
        'polymorphic_identity': 'MODEL_PHYSICS'
    }

    description = "This block defines the specific variables related to physics in the FALL3D model"

    id: Mapped[int] = mapped_column(ForeignKey(Sections.id),primary_key=True)
    
    f1: Mapped[str] = mapped_column(default = 'SUPERBEE', info = {'variable': "LIMITER",    'options': ['MINMOD', 'SUPERBEE', 'OSPRE'] })
    f2: Mapped[str] = mapped_column(default = 'RUNGE-KUTTA', info = {'variable': "TIME_MARCHING",    'options': ['EULER', 'RUNGE-KUTTA'] })
    f3: Mapped[str] = mapped_column(default = 'ALL_DIMENSIONS', info = {'variable': "CFL_CRITERION",    'options': ['ONE_DIMENSIONAL', 'ALL_DIMENSIONS'] })
    f4: Mapped[float] = mapped_column(default = 0.9, info = {'variable': "CFL_SAFETY_FACTOR",    })
    f5: Mapped[str] = mapped_column(default = 'GANSER', info = {'variable': "TERMINAL_VELOCITY_MODEL",    'options': ['ARASTOOPOUR', 'GANSER', 'WILSON', 'DELLINO', 'PFEIFFER', 'DIOGUARDI2017', 'DIOGUARDI2018'] })
    f6: Mapped[str] = mapped_column(default = 'CMAQ', info = {'variable': "HORIZONTAL_TURBULENCE_MODEL",    'options': ['CONSTANT', 'CMAQ', 'RAMS'] })
    f7: Mapped[float] = mapped_column(default = 1000, info = {'variable': "HORIZONTAL_TURBULENCE_MODEL",    })
    f8: Mapped[str] = mapped_column(default = 'SIMILARITY', info = {'variable': "VERTICAL_TURBULENCE_MODEL",    'options': ['CONSTANT', 'SIMILARITY'] })
    f9: Mapped[float] = mapped_column(default = 150, info = {'variable': "VERTICAL_TURBULENCE_MODEL",    })
    f10: Mapped[float] = mapped_column(default = 0.2275, info = {'variable': "RAMS_CS",    })
    f11: Mapped[bool] = mapped_column(default = False, info = {'variable': "WET_DEPOSITION",    })
    f12: Mapped[bool] = mapped_column(default = False, info = {'variable': "DRY_DEPOSITION",    })
    f13: Mapped[bool] = mapped_column(default = False, info = {'variable': "GRAVITY_CURRENT",    })
    f15: Mapped[float] = mapped_column(default = 870, info = {'variable': "C_FLOW_RATE",   'block': "IF_GRAVITY_CURRENT",   })
    f16: Mapped[float] = mapped_column(default = 0.2, info = {'variable': "LAMBDA_GRAV",   'block': "IF_GRAVITY_CURRENT",   })
    f17: Mapped[float] = mapped_column(default = 0.1, info = {'variable': "K_ENTRAIN",   'block': "IF_GRAVITY_CURRENT",   })
    f18: Mapped[float] = mapped_column(default = 0.02, info = {'variable': "BRUNT_VAISALA",   'block': "IF_GRAVITY_CURRENT",   })
    f19: Mapped[float] = mapped_column(default = 0, info = {'variable': "GC_START_(HOURS_AFTER_00)",   'block': "IF_GRAVITY_CURRENT",   })
    f20: Mapped[float] = mapped_column(default = 3, info = {'variable': "GC_END_(HOURS_AFTER_00)",   'block': "IF_GRAVITY_CURRENT",   })
    
    

    def _fmt_var(self,index):
        value_fmt = {True: "YES", False: "NO"}
        (var,_) = index
        k = self.vars[index][0]
        value = getattr(self,k,None)
        if isinstance(value,bool):
            return f"{var} = {value_fmt[value]}"
        elif k in ['f6','f8'] and value != 'CONSTANT':
            return f"{var} = {value}"
        return super()._fmt_var(index)



class SectionOutput (Sections):
    __tablename__ = "MODEL_OUTPUT"
    __mapper_args__ = {
        'polymorphic_identity': 'MODEL_OUTPUT'
    }

    description = "This block is read by task FALL3D and defines specific variables related to output strategy"

    id: Mapped[int] = mapped_column(ForeignKey(Sections.id),primary_key=True)
    
    f1: Mapped[bool] = mapped_column(default = False, info = {'variable': "PARALLEL_IO",    })
    f2: Mapped[str] = mapped_column(default = 'FULL', info = {'variable': "LOG_FILE_LEVEL",    'options': ['NONE', 'NORMAL', 'FULL'] })
    f3: Mapped[str] = mapped_column(default = 'END_ONLY', info = {'variable': "RESTART_TIME_INTERVAL_(HOURS)",    'options': ['value', 'NONE', 'END_ONLY'] })
    f4: Mapped[float] = mapped_column(default = 12, info = {'variable': "RESTART_TIME_INTERVAL_(HOURS)",    })
    f5: Mapped[bool] = mapped_column(default = False, info = {'variable': "OUTPUT_JSON_FILES",    })
    f6: Mapped[bool] = mapped_column(default = False, info = {'variable': "OUTPUT_INTERMEDIATE_FILES",    })
    f7: Mapped[str] = mapped_column(default = 'RUN_START', info = {'variable': "OUTPUT_TIME_START_(HOURS)",    'options': ['value', 'RUN_START'] })
    f8: Mapped[float] = mapped_column(default = 0, info = {'variable': "OUTPUT_TIME_START_(HOURS)",    })
    f9: Mapped[float] = mapped_column(default = 1, info = {'variable': "OUTPUT_TIME_INTERVAL_(HOURS)",    })
    f10: Mapped[bool] = mapped_column(default = False, info = {'variable': "OUTPUT_3D_CONCENTRATION",    })
    f11: Mapped[bool] = mapped_column(default = False, info = {'variable': "OUTPUT_3D_CONCENTRATION_BINS",    })
    f12: Mapped[bool] = mapped_column(default = False, info = {'variable': "OUTPUT_SURFACE_CONCENTRATION",    })
    f13: Mapped[bool] = mapped_column(default = True, info = {'variable': "OUTPUT_COLUMN_LOAD",    })
    f14: Mapped[bool] = mapped_column(default = True, info = {'variable': "OUTPUT_CLOUD_TOP",    })
    f15: Mapped[bool] = mapped_column(default = True, info = {'variable': "OUTPUT_GROUND_LOAD",    })
    f16: Mapped[bool] = mapped_column(default = False, info = {'variable': "OUTPUT_GROUND_LOAD_BINS",    })
    f17: Mapped[bool] = mapped_column(default = False, info = {'variable': "OUTPUT_WET_DEPOSITION",    })
    f18: Mapped[bool] = mapped_column(default = False, info = {'variable': "TRACK_POINTS",    })
    f19: Mapped[str] = mapped_column(default = 'my_file.pts', info = {'variable': "TRACK_POINTS_FILE",    })
    f20: Mapped[bool] = mapped_column(default = False, info = {'variable': "OUTPUT_CONCENTRATION_AT_XCUTS",    })
    f21: Mapped[str] = mapped_column(default = '15', info = {'variable': "X-VALUES",    })
    f22: Mapped[bool] = mapped_column(default = False, info = {'variable': "OUTPUT_CONCENTRATION_AT_YCUTS",    })
    f23: Mapped[str] = mapped_column(default = '37.5', info = {'variable': "Y-VALUES",    })
    f24: Mapped[bool] = mapped_column(default = False, info = {'variable': "OUTPUT_CONCENTRATION_AT_ZCUTS",    })
    f25: Mapped[str] = mapped_column(default = '5000', info = {'variable': "Z-VALUES",    })
    f26: Mapped[bool] = mapped_column(default = True, info = {'variable': "OUTPUT_CONCENTRATION_AT_FL",    })
    f27: Mapped[str] = mapped_column(default = '50 100 150 200 250 300 350 400', info = {'variable': "FL-VALUES",    })
    
    

    def _fmt_var(self,index):
        value_fmt = {True: "YES", False: "NO"}
        (var,_) = index
        k = self.vars[index][0]
        value = getattr(self,k,None)
        if isinstance(value,bool):
            return f"{var} = {value_fmt[value]}"
        elif 'f3' in self.vars[index]:
            if value == 'value':
                return f"{var} = {self.f4}"
            return f"{var} = {value}"
        elif 'f7' in self.vars[index]:
            if value == 'value':
                return f"{var} = {self.f8}"
            return f"{var} = {value}"
        return super()._fmt_var(index)




@db.event.listens_for(Profiles, 'load')
def receive_load(target, context):
    print("Loading profile")
    if 'profile' in session: print(session['profile'])

@db.event.listens_for(Profiles, 'init')
def receive_init(target, args, kwargs):
    print('Starting new profile')
    print(kwargs)
    s = [ 
        SectionTime(profile=target),
        SectionMeteo(profile=target),
        SectionGrid(profile=target),
        SectionSpecies(profile=target),
        SectionTGSD(profile=target),
        SectionAggregation(profile=target),
        SectionSource(profile=target),
        SectionPhysics(profile=target),
        SectionOutput(profile=target),]
    db.session.add_all(s)