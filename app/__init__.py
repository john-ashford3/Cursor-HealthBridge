import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from config import Config
from flask_bcrypt import Bcrypt

# Initialize Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
csrf = CSRFProtect()
bcrypt = Bcrypt()

# Configure login manager
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
login_manager.session_protection = 'strong'

@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User  # Import here to avoid circular import
    return User.query.get(int(user_id))

def create_app(config_class=Config):
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_class)
    config_class.init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    bcrypt.init_app(app)
    
    # Import and register blueprints
    from app.main import main
    from app.auth import auth
    from app.physician import physician
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(physician)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Configure logging
    if not app.debug and not app.testing:
        # Ensure log directory exists
        if not os.path.exists('logs'):
            os.mkdir('logs')
            
        # Create file handler
        file_handler = RotatingFileHandler(
            'logs/healthbridge.log', 
            maxBytes=10240, 
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        
        # Configure application logger
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('HealthBridge startup')
        
    # Request handlers
    @app.after_request
    def after_request(response):
        # Security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # CORS headers
        response.headers['Access-Control-Allow-Origin'] = app.config.get('FRONTEND_URL', '*')
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        
        return response

    @app.template_filter('get_user_email')
    def get_user_email(user_id):
        from app.models.user import User  # Import here to avoid circular import
        user = User.query.get(int(user_id))
        return user.email if user else 'Unknown User'

    return app 