from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import logging
import traceback

db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """Initialize database"""
    if not os.path.exists('system.db'):
        open('system.db', 'w').close()
    
    with app.app_context():
        db.create_all()

def create_app(test_config=None):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Default configuration
    default_config = {
        'SECRET_KEY': os.urandom(24),
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///system.db',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_POOL_RECYCLE': 3600
    }
    
    # Update with test config if provided
    if test_config is None:
        test_config = {}
    
    # Merge configurations
    config = {**default_config, **test_config}
    
    # Special handling for testing environment
    if test_config.get('TESTING', False):
        config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    app.config.from_mapping(config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize database
    init_db(app)
    
    # Initialize routes
    from .routes import init_routes
    init_routes(app)
    
    # Configure logging
    logging.basicConfig(
        filename='system.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    # Error handling middleware
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Handle all exceptions
        logger.error(f"Unhandled exception: {str(e)}\n{traceback.format_exc()}")
        response = {
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "code": 500
        }
        return jsonify(response), 500
    
    @app.after_request
    def after_request(response):
        logger.info(f"{request.method} {request.path} {response.status_code}")
        return response
    
    return app
