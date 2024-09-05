from app.extensions import db

class PlotModel(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    variable    = db.Column(db.String, info = {'choices': [('var1','var1'),('var2','var2')]})
    time        = db.Column(db.Integer, info = {'choices': [(1,1),(2,2)]})
    minval      = db.Column(db.Float, default=0)
    maxval      = db.Column(db.Float, default=10)
    step        = db.Column(db.Float, default=1)

    def __repr__(self):
        return f'<Profile "{self.variable}">'


