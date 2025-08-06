from flask import Blueprint

bp = Blueprint('laboratory', __name__)

from app.laboratory import routes