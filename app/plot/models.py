from app.extensions import db

class PlotModel(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    variable    = db.Column(db.String,  info = {'choices': [('','No available variables')]})
    time        = db.Column(db.Integer, info = {'choices': [(0,'No available times')]})
    minval      = db.Column(db.Float, default=0)
    maxval      = db.Column(db.Float, default=10)
    step        = db.Column(db.Float, default=1)
    logscale    = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Profile "{self.variable}">'


