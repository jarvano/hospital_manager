from flask import Blueprint

bp = Blueprint('pharmacy', __name__)

from app.pharmacy import routes