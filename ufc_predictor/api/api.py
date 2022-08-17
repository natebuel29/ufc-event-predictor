from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, url_for,
)
from ufc_predictor import util
import asyncio

api_views = Blueprint('api', __name__)


@api_views.route('/api/refit-models')
def refit_models_endpoint():
    util.fit_ml_models()
    return "OK", 200
