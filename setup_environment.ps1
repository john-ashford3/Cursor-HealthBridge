# Create and activate virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Green
python -m venv venv
.\venv\Scripts\Activate

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Green
python -m pip install --upgrade pip

# Install required packages
Write-Host "Installing required packages..." -ForegroundColor Green
pip install flask
pip install flask-sqlalchemy
pip install flask-login
pip install Flask-Dance[sqla]
pip install oauthlib
pip install requests
pip install azure-storage-blob
pip install python-magic-bin  # Windows-compatible version of python-magic
pip install Werkzeug
pip install python-dotenv

# Optional but recommended packages
pip install flask-migrate  # For database migrations
pip install flask-wtf     # For form handling
pip install email-validator  # For email validation

# Save requirements to file
Write-Host "Saving requirements to requirements.txt..." -ForegroundColor Green
pip freeze > requirements.txt

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "To activate the virtual environment in the future, run: .\venv\Scripts\Activate" -ForegroundColor Yellow