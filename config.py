import os 

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'secretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RUN_FOLDER = '/home/lmingari/fall3d/flask'
