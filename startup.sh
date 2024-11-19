#!/bin/bash
cd /home/site/wwwroot

# Create and activate virtual environment
python -m venv antenv
source antenv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Start Gunicorn
gunicorn --bind=0.0.0.0:8000 application:app
