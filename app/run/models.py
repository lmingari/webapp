from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column

class RunModel(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    f1: Mapped[int] = mapped_column(default=2, info={'label': 'NX'})
    f2: Mapped[int] = mapped_column(default=1, info={'label': 'NY'})
    f3: Mapped[int] = mapped_column(default=1, info={'label': 'NZ'})
    f4: Mapped[int] = mapped_column(default=1, info={'label': 'NENS'})
