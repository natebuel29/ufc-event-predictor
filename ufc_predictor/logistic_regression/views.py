from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, url_for,
)
import numpy as np

from . import logistic_regression_service

logistic_regresion_views = Blueprint('logistic_regression', __name__)


@logistic_regresion_views.route('/logistic-regression')
def logistic_regression():
    results = logistic_regression_service.logistic_regression_predict(
        "May 21, 2022")
    return np.array2string(results)
