from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, url_for, app
)
import numpy as np
import pendulum
from . import logistic_regression_service

logistic_regresion_views = Blueprint('logistic_regression', __name__)


@logistic_regresion_views.route('/')
def logistic_regression():
    saturday_date = ""
    if pendulum.now().weekday() == 6:
        saturday_date = pendulum.now().previous(pendulum.SATURDAY).format('YYYY-MM-DD')
    elif pendulum.now().weekday() != 5:
        saturday_date = pendulum.now().next(pendulum.SATURDAY).format('YYYY-MM-DD')
    else:
        saturday_date = pendulum.now().format('YYYY-MM-DD')
    try:
        app.logging.info(
            f"Fetching predictions for UFC event on {saturday_date}")
        results, r_fighters, b_fighters, event_name = logistic_regression_service.predict(
            saturday_date)
    except TypeError:
        app.logging.error(
            f"No UFC event on {saturday_date} - redirecting user to invalid_date url")
        return redirect(url_for("invalid_event.invalid_date", date=saturday_date))

    results_rf_bf = zip(results, r_fighters, b_fighters)

    return render_template('logistic_regression/logistic_regression.html', results_rf_bf=results_rf_bf, event_name=event_name, event_date=saturday_date)
