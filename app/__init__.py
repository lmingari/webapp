from flask import Flask
from config import Config
from app.extensions import db

from app.main import bp as main_bp
from app.profiles import bp as profiles_bp
from app.configuration import bp as configuration_bp
from app.run import bp as run_bp
from app.plot import bp as plot_bp
from app.cli import bp as cli_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here
    app.register_blueprint(main_bp)
    app.register_blueprint(profiles_bp, url_prefix='/profiles')
    app.register_blueprint(configuration_bp, url_prefix='/configuration')
    app.register_blueprint(run_bp, url_prefix='/run')
    app.register_blueprint(plot_bp, url_prefix='/plot')
    app.register_blueprint(cli_bp)

    return app
