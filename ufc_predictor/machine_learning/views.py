from cmath import e
from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, url_for, app
)

from ufc_predictor import ml_models, util, db
import traceback
machine_learning_views = Blueprint('machine_learning', __name__)


@machine_learning_views.route('/')
def logistic_regression():
    try:
        saturday_date = util.saturday_date()
        future_df = db.get_future_machups(saturday_date)
        future_X, r_fighters, b_fighters, event_name = util.event_data(
            future_df)
        future_X = future_X[:, ml_models.log_reg_clf.fit_support]
        future_X = util.add_bias(future_X)
        app.logging.info(
            f"Fetching predictions for UFC event on {saturday_date}")
        results = ml_models.log_reg_clf.predict(future_X)

    except TypeError:
        app.logging.error(
            f"No UFC event on {saturday_date} - redirecting user to invalid_date url")
        traceback.print_exc()
        return redirect(url_for("invalid_event.invalid_date", date=saturday_date))

    results_rf_bf = zip(results, r_fighters, b_fighters)

    app.logging.info(
        f"Successfully predicted UFC event on {saturday_date} - rendering machine_learning template with log reg parameters")

    return render_template('machine_learning/machine_learning_template.html', results_rf_bf=results_rf_bf, event_name=event_name, event_date=saturday_date, algorithm="Logistic Regression", class_name="log_reg")


@machine_learning_views.route('/svm')
def support_vector_machine():
    try:
        saturday_date = util.saturday_date()
        future_df = db.get_future_machups(saturday_date)
        future_X, r_fighters, b_fighters, event_name = util.event_data(
            future_df)
        future_X = util.add_bias(future_X)
        results = ml_models.svm_clf.predict(future_X)
        app.logging.info(
            f"Fetching predictions for UFC event on {saturday_date}")

    except TypeError:
        app.logging.error(
            f"No UFC event on {saturday_date} - redirecting user to invalid_date url")
        traceback.print_exc()
        return redirect(url_for("invalid_event.invalid_date", date=saturday_date))

    results_rf_bf = zip(results, r_fighters, b_fighters)

    app.logging.info(
        f"Successfully predicted UFC event on {saturday_date} - rendering machine_learning template with svm parameters")

    return render_template('machine_learning/machine_learning_template.html', results_rf_bf=results_rf_bf, event_name=event_name, event_date=saturday_date, algorithm="Support Vector Machines", class_name="svm")


@machine_learning_views.route('/neuralnetworks')
def neural_networks():
    try:
        saturday_date = util.saturday_date()
        future_df = db.get_future_machups(saturday_date)
        future_X, r_fighters, b_fighters, event_name = util.event_data(
            future_df)
        future_X = util.add_bias(future_X)
        results = ml_models.nn_clf.predict(future_X)
        results = 1*(results[:, 0] > 0.5)
        app.logging.info(
            f"Fetching predictions for UFC event on {saturday_date}")

    except TypeError:
        app.logging.error(
            f"No UFC event on {saturday_date} - redirecting user to invalid_date url")
        traceback.print_exc()
        return redirect(url_for("invalid_event.invalid_date", date=saturday_date))

    results_rf_bf = zip(results, r_fighters, b_fighters)

    app.logging.info(
        f"Successfully predicted UFC event on {saturday_date} - rendering machine_learning template with svm parameters")

    return render_template('machine_learning/machine_learning_template.html', results_rf_bf=results_rf_bf, event_name=event_name, event_date=saturday_date, algorithm="Neural Networks", class_name="neural_networks")
