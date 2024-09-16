from collections import OrderedDict
from datetime import date

class CustomDate(date):
    def __repr__(self):
        # Use self.year, self.month, and self.day to format the repr
        return f"date({self.year},{self.month},{self.day})"
    
class OrderedMeta(type):
    @classmethod
    def __prepare__(cls, name, bases):
        return OrderedDict()

    def __new__(cls, name, bases, class_dict):
        clsobj = super().__new__(cls, name, bases, dict(class_dict))
        clsobj._attr_order = list(class_dict.keys())
        return clsobj

class BaseClass(object, metaclass=OrderedMeta):
    def __init__(self, fields=None):
        self._fields = OrderedDict()
        self._vars   = OrderedDict()

        # get class variables
        for key in self.__class__._attr_order:
            if not key.startswith('__'): 
                field = getattr(self.__class__, key)
                if hasattr(field, "_field"):
                    self._fields[key] = field

        if hasattr(fields, 'items'):
            for name, field in fields.items():
                self._fields[name] = field

        seen = set()
        for key,item in self._fields.items():
            v = (item.variable,item.block)
            if v not in seen:
                seen.add(v)
                self._vars[v] = []
            self._vars[v].append(key)

    def __iter__(self):
        """Iterate form fields in creation order."""
        return iter(self._fields.values())

    def __contains__(self, name):
        """ Returns `True` if the named field is a member of this form. """
        return (name in self._fields)

    def __getitem__(self, name):
        """ Dict-style access to this form's fields."""
        return self._fields[name]

    def __setitem__(self, name, value):
        """ Bind a field to this form. """
        self._fields[name] = value

    def __delitem__(self, name):
        """ Remove a field from this form. """
        del self._fields[name]

    @property
    def fields(self):
        return self._fields

    @property
    def vars(self):
        return self._vars

class Field:
    _field = True

    def __init__(self,variable=None,label=None,block=None,default=None):
        self.variable = variable
        self.label    = label
        self.block    = block
        self.default  = default
        self.value    = default
        self._mtype   = None

    def _fmt(self):
        if self.value is not None:
            return self.value
        else: 
            return "no data"

    def __str__(self):
        out = self._fmt()
        if self.label:
            return f'{self.label} {out}'
        else:
            return f'{out}'

class FieldString(Field):
    @property
    def mtype(self):
        return 'str'

class FieldFloat(Field):
    @property
    def mtype(self):
        return 'float'

class FieldInteger(Field):
    @property
    def mtype(self):
        return 'int'

class FieldDate(Field):
    @property
    def mtype(self):
        return 'date'

class FieldBoolean(Field):
    @property
    def mtype(self):
        return 'bool'

    def _fmt(self):
        if self.value is None:
            return ""
        elif self.value:
            return "ON"
        else: 
            return "OFF"

class FieldChoice(Field):

    def __init__(self,variable=None,label=None,block=None,default=None,options=None):
        super().__init__(variable,label,block,default)
        self.options = options

    @property
    def mtype(self):
        items = [(item,item) for item in self.options]
        return f'str'

class Section(BaseClass):

    def _fmt_var(self,index):
        (variable,_) = index
        strings = [str(self[field]) for field in self.vars[index]]
        value = " ".join(strings)
        return f"{variable} = {value}"

    def __str__(self):
        nl = "\n"
        b1 = " "
        b3 = b1*3
        b6 = b1*6

        blocks_str = OrderedDict()
        for index in self.vars:
            (_,block) = index
            if not block in blocks_str:
                blocks_str[block] = ""
            blocks_str[block] += self._fmt_var(index)+nl

        for block,block_str in blocks_str.items():
            if block is None:
                output = nl.join([b3+item for item in block_str.splitlines()])
            else:
                output += nl*2 + b3 + block + nl
                output += nl.join([b6+item for item in block_str.splitlines()])
        return output

    def update_from_obj(self,obj):
        for key, field in self.fields.items():
            if hasattr(obj, key):
                value = getattr(obj,key)
                self[key].value = value

class SectionTime(Section):
    description = "This block defines variables related to date and time. It is used by FALL3D, SetDbs, and SetSrc tasks"

    f1 = FieldDate(variable="DATE", default = CustomDate(2008,4,29))
    f2 = FieldFloat(variable="RUN_START_(HOURS_AFTER_00)", default = 0)
    f3 = FieldFloat(variable="RUN_END_(HOURS_AFTER_00)", default = 24)
    f4 = FieldChoice(variable="INITIAL_CONDITION", default = 'NONE', options = ['NONE','INSERTION','RESTART'])
    f5 = FieldString(variable="RESTART_FILE", default = 'Example-8.0.rst.nc')
    f6 = FieldString(variable="RESTART_ENSEMBLE_BASEPATH", default = './')

    def _fmt_var(self,index):
        if index ==('DATE',None):
            return self.f1.value.strftime("YEAR = %Y \nMONTH = %m\nDAY = %d")
        else:
            return super()._fmt_var(index)

class SectionMeteo(Section):
    description = "This block defines variables related to the input meteorological dataset. It is read by the SetDbs task"

    f1 = FieldChoice(variable="METEO_DATA_FORMAT", default = 'WRF', options = ["WRF", "GFS", "ERA5", "ERA5ML", "IFS", "CARRA"])
    f2 = FieldString(variable="METEO_DATA_DICTIONARY_FILE", default = 'WRF.tbl')
    f3 = FieldString(variable="METEO_DATA_FILE", default = 'Example-8.0.wrf.nc')
    f4 = FieldString(variable="METEO_ENSEMBLE_BASEPATH", default = '')
    f5 = FieldString(variable="METEO_LEVELS_FILE", default = '../Other/Meteo/Tables/L137_ECMWF.levels')
    f6 = FieldFloat(variable="DBS_BEGIN_METEO_DATA_(HOURS_AFTER_00)", default = 0)
    f7 = FieldFloat(variable="DBS_END_METEO_DATA_(HOURS_AFTER_00)", default = 24)
    f8 = FieldFloat(variable="METEO_COUPLING_INTERVAL_(MIN)", default = 60)
    f9 = FieldInteger(variable="MEMORY_CHUNK_SIZE", default = 5)
   
class SectionGrid(Section):
    description = "This block defines the grid variables needed by the SetDbs and FALL3D tasks"

    f1  = FieldChoice (variable="HORIZONTAL_MAPPING", default='SPHERICAL', options = ['CARTESIAN','SPHERICAL'])
    f2  = FieldChoice (variable="VERTICAL_MAPPING", default='SIGMA_LINEAR_DECAY', options = ["SIGMA_NO_DECAY","SIGMA_LINEAR_DECAY","SIGMA_EXPONENTIAL_DECAY"])
    f3  = FieldFloat  (variable="LONMIN", default = 14.0)
    f4  = FieldFloat  (variable="LONMAX", default = 16.0)
    f5  = FieldFloat  (variable="LATMIN", default = 36.5)
    f6  = FieldFloat  (variable="LATMAX", default = 38.5)
    f7  = FieldInteger(variable="NX", default = 50)
    f8  = FieldBoolean(variable="NX", default = False, label='RESOLUTION')
    f9  = FieldFloat  (variable="NX", default = 0.1)
    f10 = FieldInteger(variable="NY", default = 50)
    f11 = FieldBoolean(variable="NY", default = False, label='RESOLUTION')
    f12 = FieldFloat  (variable="NY", default = 0.1)
    f13 = FieldInteger(variable="NZ", default = 10)
    f14 = FieldFloat  (variable="ZMAX_(M)", default = 10000)
    f15 = FieldString (variable="SIGMA_VALUES", default = "") 

    def _fmt_var(self,index):
        if index == ('NX',None):
            if self.f8.value:
                value = f"RESOLUTION {self['f9']}"
            else:
                value = str(self['f7'])
            return f"NX = {value}"
        elif index == ('NY',None):
            if self.f11.value:
                value = f"RESOLUTION {self['f12']}"
            else:
                value = str(self['f10'])
            return f"NY = {value}"
        else:
            return super()._fmt_var(index)

class SectionSpecies(Section):
    description = "This block is used by FALL3D, SetTgsd, and SetSrc tasks and defines which species are modeled"
    
    f1  = FieldBoolean(variable="TEPHRA", default = True)
    f2  = FieldBoolean(variable="DUST", default = False)
    f3  = FieldBoolean(variable="H2O", default = False)
    f4  = FieldFloat  (variable="H2O", default = 2, label='MASS_FRACTION_(%)')
    f5  = FieldBoolean(variable="SO2", default = True)
    f6  = FieldFloat  (variable="SO2", default = 1, label='MASS_FRACTION_(%)')
    f7  = FieldBoolean(variable="CS134", default = False)
    f8  = FieldFloat  (variable="CS134", default = 0, label='MASS_FRACTION_(%)')
    f9  = FieldBoolean(variable="CS137", default = False)
    f10 = FieldFloat  (variable="CS137", default = 0, label='MASS_FRACTION_(%)')
    f11 = FieldBoolean(variable="I131", default = False)
    f12 = FieldFloat  (variable="I131", default = 0, label='MASS_FRACTION_(%)')
    f13 = FieldBoolean(variable="SR90", default = False)
    f14 = FieldFloat  (variable="SR90", default = 0, label='MASS_FRACTION_(%)')
    f15 = FieldBoolean(variable="Y90", default = False)
    f16 = FieldFloat  (variable="Y90", default = 0, label='MASS_FRACTION_(%)')

class SectionTGSD(Section):
    description = "These blocks define the TGSD for each species and are used by the SetTgsd task to generate some basic distributions"

    f1  = FieldInteger(variable="NUMBER_OF_BINS", default = 6)
    f2  = FieldString(variable="FI_RANGE", default = "-2 8")
    f3  = FieldString(variable="DENSITY_RANGE", default = "1200 2300")
    f4  = FieldString(variable="SPHERICITY_RANGE", default = "0.9 0.9")
    f5  = FieldChoice(variable="DISTRIBUTION", default = 'GAUSSIAN', options = ["GAUSSIAN","BIGAUSSIAN","WEIBULL","BIWEIBULL","CUSTOM","ESTIMATE"])
    f6  = FieldFloat(variable="FI_MEAN", block="IF_GAUSSIAN", default = 2.5)
    f7  = FieldFloat(variable="FI_DISP", block="IF_GAUSSIAN", default = 1.5)
    f8  = FieldString(variable="FI_MEAN", block="IF_BIGAUSSIAN", default = "0.25 0.75")
    f9  = FieldString(variable="FI_DISP", block="IF_BIGAUSSIAN", default = "1.44 1.46")
    f10 = FieldFloat(variable="MIXING_FACTOR", block="IF_BIGAUSSIAN", default = 0.5)

class SectionAggregation(Section):
    description = "This block is used by task SetSrc and controls particle aggregation and cut-off (for categories particles and radionuclides only)"

    f1 = FieldChoice(variable="PARTICLE_CUT_OFF", default = 'NONE', options = ["NONE","FI_LOWER_THAN","FI_LARGER_THAN","D_(MIC)_LARGER_THAN","D_(MIC)_LOWER_THAN"])
    f2 = FieldFloat(variable="PARTICLE_CUT_OFF", default = 1.)
    f3 = FieldChoice(variable="AGGREGATION_MODEL", default = 'PERCENTAGE', options = ['NONE','CORNELL','COSTA','PERCENTAGE'])
    f4 = FieldInteger(variable="NUMBER_OF_AGGREGATE_BINS", default = 2)
    f5 = FieldString(variable="DIAMETER_AGGREGATES_(MIC)", default = "300. 200.")
    f6 = FieldString(variable="DENSITY_AGGREGATES_(KGM3)", default = "350. 250.")
    f7 = FieldString(variable="PERCENTAGE_(%)", default = "20. 10.")
    f8 = FieldFloat(variable="VSET_FACTOR", default = "0.5")
    f9 = FieldFloat(variable="FRACTAL_EXPONENT", default = "2.99")

    def _fmt_var(self,index):
        if index ==('PARTICLE_CUT_OFF',None) and self.f1.value == 'NONE':
            return "PARTICLE_CUT_OFF = NONE"
        else:
            return super()._fmt_var(index)

class SectionSource(Section):
    description = "This block defines the variables needed by the SetSrc task to generate the source term for the emission phases"

    f1  = FieldChoice(variable="SOURCE_TYPE", default = 'TOP-HAT', options = ['POINT','SUZUKI','TOP-HAT','PLUME'])
    f2  = FieldString(variable="SOURCE_START_(HOURS_AFTER_00)", default = "0  12")
    f3  = FieldString(variable="SOURCE_END_(HOURS_AFTER_00)",   default = "10 24")
    f4  = FieldFloat(variable="LON_VENT", default = 15.0)
    f5  = FieldFloat(variable="LAT_VENT", default = 37.75)
    f6  = FieldFloat(variable="VENT_HEIGHT_(M)", default = 3000.)
    f7  = FieldFloat(variable="HEIGHT_ABOVE_VENT_(M)", default = 6000.)
    f8  = FieldChoice(variable="MASS_FLOW_RATE_(KGS)", default = 'ESTIMATE-MASTIN', options = ['value','ESTIMATE-MASTIN','ESTIMATE-WOODHOUSE','ESTIMATE-DEGRUYTER'])
    f9  = FieldFloat(variable="MASS_FLOW_RATE_(KGS)", default = 1E7)
    f10 = FieldFloat(variable="ALFA_PLUME", default = 0.1)
    f11 = FieldFloat(variable="BETA_PLUME", default = 0.5)
    f12 = FieldFloat(variable="EXIT_TEMPERATURE_(K)", default = 1200.)
    f13 = FieldFloat(variable="EXIT_WATER_FRACTION_(%)", default = 0.)
    f14 = FieldString(variable="A", block="IF_SUZUKI_SOURCE", default = "4. 5.")
    f15 = FieldString(variable="L", block="IF_SUZUKI_SOURCE", default = "5.")
    f16 = FieldFloat(variable="THICKNESS_(M)", block="IF_TOP-HAT_SOURCE", default = 2000.)

    def _fmt_var(self,index):
        if 'f8' in self.vars[index]:
            if self['f8'].value == 'value':
                return f"MASS_FLOW_RATE_(KGS) = {self['f9']}"
            else:
                return f"MASS_FLOW_RATE_(KGS) = {self['f8']}"
        else:
            return super()._fmt_var(index)

class SectionPhysics(Section):
    description = "This block defines the specific variables related to physics in the FALL3D model"

    f1  = FieldChoice(variable="LIMITER", default = 'SUPERBEE', options = ['MINMOD','SUPERBEE','OSPRE'])
    f2  = FieldChoice(variable="TIME_MARCHING", default = 'RUNGE-KUTTA', options = ['EULER','RUNGE-KUTTA'])
    f3  = FieldChoice(variable="CFL_CRITERION", default = 'ALL_DIMENSIONS', options = ['ONE_DIMENSIONAL','ALL_DIMENSIONS'])
    f4  = FieldFloat(variable="CFL_SAFETY_FACTOR", default = 0.9)
    f5  = FieldChoice(variable="TERMINAL_VELOCITY_MODEL", default = 'GANSER', options = ['ARASTOOPOUR','GANSER','WILSON','DELLINO','PFEIFFER','DIOGUARDI2017','DIOGUARDI2018'])
    f6  = FieldChoice(variable="HORIZONTAL_TURBULENCE_MODEL", default = 'CMAQ', options = ['CONSTANT', 'CMAQ', 'RAMS'])
    f7  = FieldFloat(variable="HORIZONTAL_TURBULENCE_MODEL", default = 1000)
    f8  = FieldChoice(variable="VERTICAL_TURBULENCE_MODEL", default = 'SIMILARITY', options = ['CONSTANT', 'SIMILARITY'])
    f9  = FieldFloat(variable="VERTICAL_TURBULENCE_MODEL", default = 150)
    f10 = FieldFloat(variable="RAMS_CS", default = 0.2275)
    f11 = FieldBoolean(variable="WET_DEPOSITION", default = False)
    f12 = FieldBoolean(variable="DRY_DEPOSITION", default = False)
    f13 = FieldBoolean(variable="GRAVITY_CURRENT", default = False)
    #
    f15 = FieldFloat(variable="C_FLOW_RATE", block="IF_GRAVITY_CURRENT", default = 870)
    f16 = FieldFloat(variable="LAMBDA_GRAV", block="IF_GRAVITY_CURRENT", default = 0.2)
    f17 = FieldFloat(variable="K_ENTRAIN", block="IF_GRAVITY_CURRENT", default = 0.1)
    f18 = FieldFloat(variable="BRUNT_VAISALA", block="IF_GRAVITY_CURRENT", default = 0.02)
    f19 = FieldFloat(variable="GC_START_(HOURS_AFTER_00)", block="IF_GRAVITY_CURRENT", default = 0)
    f20 = FieldFloat(variable="GC_END_(HOURS_AFTER_00)", block="IF_GRAVITY_CURRENT", default = 3)

    def _fmt_var(self,index):
        (var,_) = index
        k = self.vars[index][0]
        if self[k].mtype == "db.Boolean":
            if self[k].value:
                value = "YES"
            else:
                value = "NO"
            return f"{var} = {value}"
        elif k in ['f6','f8'] and self[k].value != 'CONSTANT':
            return f"{var} = {self[k]}"
        else:
            return super()._fmt_var(index)

class SectionOutput(Section):
    description = "This block is read by task FALL3D and defines specific variables related to output strategy"

    f1  = FieldBoolean(variable="PARALLEL_IO", default = False)
    f2  = FieldChoice(variable="LOG_FILE_LEVEL", default = 'FULL', options = ['NONE','NORMAL','FULL'])
    f3  = FieldChoice(variable="RESTART_TIME_INTERVAL_(HOURS)", default = 'END_ONLY', options = ['value','NONE','END_ONLY'])
    f4  = FieldFloat(variable="RESTART_TIME_INTERVAL_(HOURS)", default = 12)
    f5  = FieldBoolean(variable="OUTPUT_JSON_FILES", default = False)
    f6  = FieldBoolean(variable="OUTPUT_INTERMEDIATE_FILES", default = False)
    f7  = FieldChoice(variable="OUTPUT_TIME_START_(HOURS)", default = 'RUN_START', options = ['value','RUN_START'])
    f8  = FieldFloat(variable="OUTPUT_TIME_START_(HOURS)", default = 0)
    f9  = FieldFloat(variable="OUTPUT_TIME_INTERVAL_(HOURS)", default = 1)
    f10  = FieldBoolean(variable="OUTPUT_3D_CONCENTRATION", default = False)
    f11 = FieldBoolean(variable="OUTPUT_3D_CONCENTRATION_BINS", default = False)
    f12 = FieldBoolean(variable="OUTPUT_SURFACE_CONCENTRATION", default = False)
    f13 = FieldBoolean(variable="OUTPUT_COLUMN_LOAD", default = True)
    f14 = FieldBoolean(variable="OUTPUT_CLOUD_TOP", default = True)
    f15 = FieldBoolean(variable="OUTPUT_GROUND_LOAD", default = True)
    f16 = FieldBoolean(variable="OUTPUT_GROUND_LOAD_BINS", default = False)
    f17 = FieldBoolean(variable="OUTPUT_WET_DEPOSITION", default = False)
    f18 = FieldBoolean(variable="TRACK_POINTS", default = False)
    f19 = FieldString(variable="TRACK_POINTS_FILE", default = "my_file.pts")
    f20 = FieldBoolean(variable="OUTPUT_CONCENTRATION_AT_XCUTS", default = False)
    f21 = FieldString(variable="X-VALUES", default = "15")
    f22 = FieldBoolean(variable="OUTPUT_CONCENTRATION_AT_YCUTS", default = False)
    f23 = FieldString(variable="Y-VALUES", default = "37.5")
    f24 = FieldBoolean(variable="OUTPUT_CONCENTRATION_AT_ZCUTS", default = False)
    f25 = FieldString(variable="Z-VALUES", default = "5000")
    f26 = FieldBoolean(variable="OUTPUT_CONCENTRATION_AT_FL", default = True)
    f27 = FieldString(variable="FL-VALUES", default = "50 100 150 200 250 300 350 400")

    def _fmt_var(self,index):
        (var,_) = index
        k = self.vars[index][0]
        if self[k].mtype == "db.Boolean":
            if self[k].value:
                value = "YES"
            else:
                value = "NO"
            return f"{var} = {value}"
        elif 'f3' in self.vars[index]:
            if self['f3'].value == 'value':
                value = self['f4'].value
            else:
                value = self['f3']
            return f"{var} = {value}"
        elif 'f7' in self.vars[index]:
            if self['f7'].value == 'value':
                value = self['f8'].value
            else:
                value = self['f7']
            return f"{var} = {value}"
        else:
            return super()._fmt_var(index)

def get_sections():
    config = {
            'TIME_UTC':             SectionTime(),
            'METEO_DATA':           SectionMeteo(),
            'GRID':                 SectionGrid(),
            'SPECIES':              SectionSpecies(),
            'TEPHRA_TGSD':          SectionTGSD(),
            'PARTICLE_AGGREGATION': SectionAggregation(),
            'SOURCE':               SectionSource(),
            'MODEL_PHYSICS':        SectionPhysics(),
            'MODEL_OUTPUT':         SectionOutput(),
            }
    return config

if __name__ == "__main__":
    from jinja2 import Template, Environment, FileSystemLoader

    # Define the custom filter
    def repr_filter(value):
        return repr(value)

    # Create an environment and add the custom filter
    Loader = FileSystemLoader(searchpath="./")
    env = Environment(loader=Loader)
    env.filters['repr'] = repr_filter
    template = env.get_template('class.jinja')

    config = get_sections()

    sections = {(k,type(obj).__name__): obj for k,obj in config.items()}

    with open("models.py", "w") as f:
        out = template.render(sections=sections)
        f.write(out)

#    for label,section in config.items():
#        print("*** ",label," ***")
#        print(section)
