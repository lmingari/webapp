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
    def __init__(self, fields):
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
        if label is None:
            self.label    = variable
        else:
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
    def __init__(self,label=None,fields=None):
        super().__init__(fields)
        self.label = label

    def _fmt_var(self,variable):
        strings = [item.__str__() for item in self if item.variable==variable]
        value = " ".join(strings)
        return f"{variable} = {value}"

    def __str__(self):
        seen = set()
        output = "++++++ " + self.label
        for item in self:
            v = item.variable
            if v not in seen: 
                seen.add(v)
                output += '\n'
                output += self._fmt_var(v)
        return output

class SectionTime(Section):
#    f1a = FieldInteger(variable="YEAR", default = 2008)
#    f1b = FieldInteger(variable="MONTH", default = 4)
#    f1c = FieldInteger(variable="DAY", default = 29)
    f1 = FieldDate(variable="DATE", default = date(2008,4,29))
    f2 = FieldFloat(variable="RUN_START_(HOURS_AFTER_00)", default = 0)
    f3 = FieldFloat(variable="RUN_END_(HOURS_AFTER_00)", default = 10)
    f4 = FieldChoice(variable="INITIAL_CONDITION", default = 'NONE', options = ['NONE','INSERTION','RESTART'])
    f5 = FieldString(variable="RESTART_FILE", default = 'Example-8.0.rst.nc')

class SectionGrid(Section):
    f1  = FieldChoice (variable="HORIZONTAL_MAPPING", default='SPHERICAL', options = ['CARTESIAN','SPHERICAL'])
    f2  = FieldChoice (variable="VERTICAL_MAPPING", default='SIGMA_LINEAR_DECAY', options = ["SIGMA_NO_DECAY","SIGMA_LINEAR_DECAY","SIGMA_EXPONENTIAL_DECAY"])
    f3  = FieldFloat  (variable="LONMIN", default = 14.0)
    f4  = FieldFloat  (variable="LONMAX", default = 16.0)
    f5  = FieldFloat  (variable="LATMIN", default = 36.5)
    f6  = FieldFloat  (variable="LATMAX", default = 38.5)
    f7  = FieldInteger(variable="NX", default = 50)
    f8  = FieldFloat  (variable="NX", default = 0.1)
    f9  = FieldBoolean(variable="NX", default = True, label='RESOLUTION')
    f10 = FieldInteger(variable="NY", default = 50)
    f11 = FieldFloat  (variable="NY", default = 0.1)
    f12 = FieldBoolean(variable="NY", default = True, label='RESOLUTION')
    f13 = FieldInteger(variable="NZ", default = 10)
    f14 = FieldFloat  (variable="ZMAX_(M)", default = 10000)

    def _fmt_var(self,variable):
        if variable =='NX':
            if self.f7.value:
                value = self.f8.__str__()
            else:
                value = self.f9.__str__()
            return f"{variable} = {value}"
        elif variable == 'NY':
            if self.f10.value:
                value = self.f11.__str__()
            else:
                value = self.f12.__str__()
            return f"{variable} = {value}"
        else:
            return super()._fmt_var(variable)

class SectionSpecies(Section):
    f1  = FieldBoolean(variable="TEPHRA", default = True)
    f2  = FieldBoolean(variable="DUST", default = False)
    f3  = FieldBoolean(variable="H2O", default = False)
    f4  = FieldFloat  (variable="H2O", default = 2, label='MASS_FRACTION_(%)')
    f5  = FieldBoolean(variable="SO2", default = True)
    f6  = FieldFloat  (variable="SO2", default = 1, label='MASS_FRACTION_(%)')

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

    config = [
            SectionTime(label='TIME_UTC'),
            SectionGrid(label='GRID'),
            SectionSpecies(label='SPECIES'),
            ]

    with open("models.py", "w") as f:
        out = template.render(sections=config)
        f.write(out)

    for section in config:
        print(section.label)
        for k,field in section.data.items():
            print(k)
