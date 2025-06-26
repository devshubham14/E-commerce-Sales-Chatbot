from flask import Blueprint

chatbot_bp = Blueprint('chatbot', __name__)

from .routes import *  # Import routes to register them with the blueprint