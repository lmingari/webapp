import json
from jinja2 import Template
with open('class.jinja') as file:
    template = Template(file.read())

with open('namelist.json') as f:
    data = json.load(f)
    out = template.render(blocks=data)

with open("models.py", "w") as f:
    f.write(out)
