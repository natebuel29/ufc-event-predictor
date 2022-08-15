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
        fights_df = db.get_past_matchups()
        r_fighters, b_fighters, event_name = util.event_data(future_df)
        X, y, future_X = util.genererate_inputs_n_labels(future_df, fights_df)
        log_clf = ml_models.log_reg_clf
        future_X = future_X[:, log_clf.fit_support]
        future_X = util.add_bias(future_X)
        app.logging.info(
            f"Fetching predictions for UFC event on {saturday_date}")
        results = log_clf.predict(future_X)

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
        fights_df = db.get_past_matchups()
        r_fighters, b_fighters, event_name = util.event_data(future_df)
        X, y, future_X = util.genererate_inputs_n_labels(future_df, fights_df)

        # parameters of kernel=rbf, c=5, and gamma=0.01 were the parameters selected by GridSearchCV
        clf = ml_models.svm_clf

        # add bias
        X = util.add_bias(X)
        future_X = util.add_bias(future_X)
        results = clf.predict(future_X)

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
