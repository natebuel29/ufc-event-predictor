from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, url_for,
)
import numpy as np
import pendulum

from . import logistic_regression_service

logistic_regresion_views = Blueprint('logistic_regression', __name__)


@logistic_regresion_views.route('/')
def logistic_regression():
    saturday_date = ""
    print(pendulum.now().weekday())
    if pendulum.now().weekday() != 5:
        saturday_date = pendulum.now().next(pendulum.SATURDAY).format('YYYY-MM-DD')
    elif pendulum.now().weekday() == 6 or pendulum.now().weekday() == 0:
        saturday_date = pendulum.now().previous(pendulum.SATURDAY).format('YYYY-MM-DD')
    else:
        saturday_date = pendulum.now().format('YYYY-MM-DD')

    results, r_fighters, b_fighters, event_name = logistic_regression_service.predict(
        saturday_date)
    results_rf_bf = zip(results, r_fighters, b_fighters)

    return render_template('logistic_regression/logistic_regression.html', results_rf_bf=results_rf_bf, event_name=event_name, event_date=saturday_date)
