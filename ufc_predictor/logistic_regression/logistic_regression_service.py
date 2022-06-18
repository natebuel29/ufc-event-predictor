from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
from sklearn.feature_selection import RFE
from ufc_predictor import db
from ufc_predictor.util import standardize


def predict(date):
    conn = db.mysql.connect()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM future_matchups WHERE date_='{date}'")

    future_df = pd.DataFrame(cursor.fetchall()).loc[:, 2:]

    cursor.execute(f"SELECT * FROM past_matchups")
    fights_df = pd.DataFrame(cursor.fetchall()).loc[:, 1:]

    # grab event name
    event_name = future_df.loc[1, 2]

    future_X = future_df.loc[:, 5:].astype(float).to_numpy()
    future_X = standardize(future_X)

    # Get data for model
    X = fights_df.loc[:, 4:].astype(float).to_numpy()
    X_norm = standardize(X)
    y = fights_df.loc[:, 3].astype(float).to_numpy()

    clf = LogisticRegression(random_state=2)

    # Use Recursive Feature Elimation for feature selection
    rfe = RFE(clf)
    fit = rfe.fit(X_norm, y)

    # filter to only the significant variables
    X_norm = X_norm[:, fit.support_]
    future_X = future_X[:, fit.support_]

    rows, columns = X_norm.shape

    # add one column
    X_norm = np.concatenate([np.ones((rows, 1)),
                             X_norm], axis=1)
    future_X = np.concatenate([np.ones((future_X.shape[0], 1)),
                               future_X], axis=1)

    # fit model
    clf.fit(X_norm, y)

    # predict
    clf_predictions = clf.predict(future_X).tolist()

    r_fighters = future_df.loc[:, 3].values.tolist()
    b_fighters = future_df.loc[:, 4].values.tolist()

    return clf_predictions, r_fighters, b_fighters, event_name
