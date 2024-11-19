import os
from app import create_app

# Get environment from system or default to development
env = os.environ.get('FLASK_ENV', 'development')
app = create_app()

if __name__ == '__main__':
    if env == 'production':
        # Production settings
        app.run(
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000)),
            debug=False
        )
    else:
        # Development settings
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=True
        )