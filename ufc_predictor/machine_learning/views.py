from cmath import e
from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, url_for, app
)
import numpy as np
import pendulum
from ufc_predictor import util
from ufc_predictor import db
import traceback
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from ufc_predictor.machine_learning.ml_model_service import ML_Model_Service
machine_learning_views = Blueprint('machine_learning', __name__)


@machine_learning_views.route('/')
def logistic_regression():
    try:
        saturday_date = util.saturday_date()
        future_df = db.get_future_machups(saturday_date)
        fights_df = db.get_past_matchups()
        r_fighters, b_fighters, event_name = util.event_data(future_df)
        X, y, future_X = util.genererate_inputs_n_labels(future_df, fights_df)
        clf = LogisticRegression(random_state=2)

        # Use Recursive Feature Elimation for feature selection
        rfe = RFE(clf)
        fit = rfe.fit(X, y)

        # filter to only the significant variables
        X = X[:, fit.support_]
        future_X = future_X[:, fit.support_]

        # add bias
        X = util.add_bias(X)
        future_X = util.add_bias(future_X)

        app.logging.info(
            f"Fetching predictions for UFC event on {saturday_date}")
        service = ML_Model_Service(clf=clf)
        results = service.predict(X, y, future_X)

    except TypeError:
        app.logging.error(
            f"No UFC event on {saturday_date} - redirecting user to invalid_date url")
        traceback.print_exc()
        return redirect(url_for("invalid_event.invalid_date", date=saturday_date))

    results_rf_bf = zip(results, r_fighters, b_fighters)

    app.logging.info(
        f"Successfully predicted UFC event on {saturday_date} - rendering logistic_regression template")

    return render_template('logistic_regression/logistic_regression.html', results_rf_bf=results_rf_bf, event_name=event_name, event_date=saturday_date)

# temp support vector machines


@machine_learning_views.route('/support-vector-machines')
def support_vector_machine():
    try:
        saturday_date = util.saturday_date()
        future_df = db.get_future_machups(saturday_date)
        fights_df = db.get_past_matchups()
        r_fighters, b_fighters, event_name = util.event_data(future_df)
        X, y, future_X = util.genererate_inputs_n_labels(future_df, fights_df)

        # parameters of kernel=rbf, c=5, and gamma=0.01 are the best performing parameters according to GridSearch
        clf = svm.SVC(kernel="rbf", C=5, gamma=0.01)

        # add bias
        X = util.add_bias(X)
        future_X = util.add_bias(future_X)

        app.logging.info(
            f"Fetching predictions for UFC event on {saturday_date}")
        service = ML_Model_Service(clf=clf)
        results = service.predict(X, y, future_X)

    except TypeError:
        app.logging.error(
            f"No UFC event on {saturday_date} - redirecting user to invalid_date url")
        traceback.print_exc()
        return redirect(url_for("invalid_event.invalid_date", date=saturday_date))

    results_rf_bf = zip(results, r_fighters, b_fighters)

    app.logging.info(
        f"Successfully predicted UFC event on {saturday_date} - rendering logistic_regression template")

    return render_template('logistic_regression/logistic_regression.html', results_rf_bf=results_rf_bf, event_name=event_name, event_date=saturday_date)
