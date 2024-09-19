from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column

class PlotModel(db.Model):
    id: Mapped[int]   = mapped_column(primary_key=True)
    f1: Mapped[str]   = mapped_column(unique=True,   info={'label': 'Variable', 'choices': [('','No available variables')]})
    f2: Mapped[int]   = mapped_column(unique=True,   info={'label': 'Time', 'choices': [(0,'No available times')]})
    f3: Mapped[float] = mapped_column(default=0,     info={'label': 'Minimum'})
    f4: Mapped[float] = mapped_column(default=5,     info={'label': 'Maximum'})
    f5: Mapped[float] = mapped_column(default=1,     info={'label': 'Step'})
    f6: Mapped[bool]  = mapped_column(default=False, info={'label': 'Logscale'})
    f7: Mapped[bool]  = mapped_column(default=False, info={'label': 'Automatic scale'})
