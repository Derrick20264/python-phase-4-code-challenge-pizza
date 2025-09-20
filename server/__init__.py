from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create a single SQLAlchemy instance
db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Config
    if test_config:
        app.config.update(test_config)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Init SQLAlchemy
    db.init_app(app)

    # Import models so they register with SQLAlchemy
    from .models import Pizza, Restaurant

    # Create tables
    with app.app_context():
        db.create_all()
    
    # Import routes
    from .routes import bp
    app.register_blueprint(bp)

    return app
