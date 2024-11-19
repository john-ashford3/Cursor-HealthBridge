from flask import Blueprint

physician = Blueprint('physician', __name__)

from app.physician import routes
