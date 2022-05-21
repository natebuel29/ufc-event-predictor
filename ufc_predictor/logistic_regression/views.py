from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, url_for,
)
import numpy as np

from . import logistic_regression_service

logistic_regresion_views = Blueprint('logistic_regression', __name__)


@logistic_regresion_views.route('/logistic-regression')
def logistic_regression():
    results, r_fighters, b_fighters = logistic_regression_service.logistic_regression_predict(
        "May 21, 2022")
    print(results)
    results_rf_bf = zip(results, r_fighters, b_fighters)
    print(results_rf_bf)
    return render_template('logistic_regression/logistic_regression.html', results_rf_bf=results_rf_bf)
