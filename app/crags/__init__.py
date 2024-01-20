from flask import Blueprint
bp = Blueprint('crags', __name__)
from app.auth import routes