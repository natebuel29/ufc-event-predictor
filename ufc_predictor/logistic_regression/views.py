from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, url_for,
)
import numpy as np
import pendulum

from . import logistic_regression_service

logistic_regresion_views = Blueprint('logistic_regression', __name__)


@logistic_regresion_views.route('/logistic-regression')
def logistic_regression():
    next_saturday = pendulum.now().next(pendulum.SATURDAY).format("LL")
    results, r_fighters, b_fighters, event_name = logistic_regression_service.logistic_regression_predict(
        next_saturday)
    results_rf_bf = zip(results, r_fighters, b_fighters)
    return render_template('logistic_regression/logistic_regression.html', results_rf_bf=results_rf_bf, event_name=event_name)
