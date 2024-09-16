{% macro render_str(section) %}
{%if section == 'TIME_UTC' %}
    def _fmt_var(self,index):
        if index ==('DATE',None):
            return getattr(self,'f1').strftime("YEAR = %Y\nMONTH = %m\nDAY = %d")
        return super()._fmt_var(index)
{%elif section == 'GRID' %}
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
{%elif section == 'PARTICLE_AGGREGATION' %}
    def _fmt_var(self,index):
        if index == ('PARTICLE_CUT_OFF',None) and self.f1 == 'NONE':
            return "PARTICLE_CUT_OFF = NONE"
        return super()._fmt_var(index)
{%elif section == 'SOURCE' %}
    def _fmt_var(self,index):
        if 'f8' in self.vars[index]:
            if self.f8 == 'value':
                return f"MASS_FLOW_RATE_(KGS) = {self.f9}"
            else:
                return f"MASS_FLOW_RATE_(KGS) = {self.f8}"
        return super()._fmt_var(index)
{%elif section == 'MODEL_PHYSICS' %}
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
{%elif section == 'MODEL_OUTPUT' %}
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
{% endif %}
{% endmacro %}
