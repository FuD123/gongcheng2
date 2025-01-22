import os
from flask import Flask
from flask_cors import CORS
from app import db, routes

def create_app(test_config=None):
    """Create and configure the Flask application"""
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
    
    # Default configuration
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'system.db'),
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'system.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # Load configuration from file if exists
    if test_config is None:
        # Load from instance config
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load test configuration
        app.config.update(test_config)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(routes.bp)
    
    # Initialize routes
    routes.init_routes(app)

    return app

if __name__ == '__main__':
    # Create and run application
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
