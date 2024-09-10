from collections import OrderedDict
from datetime import date

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

        # get class variables
        for key in self.__class__._attr_order:
            if not key.startswith('__'): 
                field = getattr(self.__class__, key)
                if hasattr(field, "_field"):
                    self._fields[key] = field

        if hasattr(fields, 'items'):
            for name, field in fields.items():
                self._fields[name] = field

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
    def data(self):
        return self._fields

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
        return 'db.String'

class FieldFloat(Field):
    @property
    def mtype(self):
        return 'db.Float'

class FieldInteger(Field):
    @property
    def mtype(self):
        return 'db.Integer'

class FieldDate(Field):
    @property
    def mtype(self):
        return 'db.Date'

class FieldBoolean(Field):
    @property
    def mtype(self):
        return 'db.Boolean'

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
        return f'ChoiceType({items})'

class Section(BaseClass):

    def _fmt_var(self,variable):
        strings = [item.__str__() for item in self if item.variable==variable]
        value = " ".join(strings)
        return f"{variable} = {value}"

    def __str__(self):
        output = "\n"
        for v in self.data_var:
            output += self._fmt_var(v)+'\n'
        return output

    @property
    def data_var(self):
        output = {}
        seen = set()
        for key,item in self._fields.items():
            v = item.variable
            if v not in seen:
                seen.add(v)
                output[v] = []
            output[v].append(key)
        return output

class SectionTime(Section):
    description = "This block defines variables related to date and time. It is used by FALL3D, SetDbs, and SetSrc tasks"
#    f1a = FieldInteger(variable="YEAR", default = 2008)
#    f1b = FieldInteger(variable="MONTH", default = 4)
#    f1c = FieldInteger(variable="DAY", default = 29)
    f1 = FieldDate(variable="DATE", default = date(2008,4,29))
    f2 = FieldFloat(variable="RUN_START_(HOURS_AFTER_00)", default = 0)
    f3 = FieldFloat(variable="RUN_END_(HOURS_AFTER_00)", default = 10)
    f4 = FieldChoice(variable="INITIAL_CONDITION", default = 'NONE', options = ['NONE','INSERTION','RESTART'])
    f5 = FieldString(variable="RESTART_FILE", default = 'Example-8.0.rst.nc')
    f6 = FieldString(variable="RESTART_ENSEMBLE_BASEPATH", default = './')

    def _fmt_var(self,variable):
        if variable =='DATE':
            return self.f1.value.strftime("YEAR = %Y \nMONTH = %m\nDAY = %d")
        else:
            return super()._fmt_var(variable)

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
    f15 = FieldFloat  (variable="SIGMA_VALUES", default = 10000) #TODO

    def _fmt_var(self,variable):
        if variable =='NX':
            if self.f8.value:
                value = f"RESOLUTION {self['f9']}"
            else:
                value = str(self['f7'])
            return f"{variable} = {value}"
        elif variable == 'NY':
            if self.f11.value:
                value = f"RESOLUTION {self['f12']}"
            else:
                value = str(self['f10'])
            return f"{variable} = {value}"
        else:
            return super()._fmt_var(variable)

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

def get_sections():
    config = {
            'TIME_UTC':   SectionTime(),
            'METEO_DATA': SectionMeteo(),
            'GRID':       SectionGrid(),
            'SPECIES':    SectionSpecies(),
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

    with open("models.py", "w") as f:
        out = template.render(sections=config)
        f.write(out)

    for label,section in config.items():
        print(section)
#        for k,field in section.data.items():
#            print(k)
