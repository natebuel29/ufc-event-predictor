from sklearn.linear_model import LogisticRegression
import random
import pandas as pd
import numpy as np
import csv
from sklearn.feature_selection import RFE

fdf_labels = ['rf', 'bf', 'winner', 'rwins', 'bwins', 'rloses', 'bloses', 'rslpm', 'bslpm', 'rstrac', 'bstrac', 'rsapm', 'bsapm', 'rstrd', 'bstrd', 'rtdav',
              'btdav', 'rtdac', 'btdac', 'rtdd', 'btdd', 'rsubav', 'bsubav']
stat_indexes = [4, 5, 13, 14, 15, 16, 17, 18, 19, 20]


# temporarily load csv and modify data each request - this a terrible solution and will need to be resolved later on, but we are just testing things.

def construct_fight_dataframe(df, fighter_stats, shouldRandomize):
    """ 
    Constructs the fight dataframe from using the fights df and fighter stats dict
    Arguments:
        df: the fighter df that is read from fighters.csv
        shouldRandomize: boolean flag to randomize the red/blue corner to balance the classes
    Returns:
        The fight dataframe which includes the fighters,their stats, and the winner
    """
    X = pd.DataFrame(columns=fdf_labels)
    for row in df.itertuples():
        temp_ar = []
        rwin = row[3]
        chance = random.uniform(0, 1)
        if chance > 0.65 and shouldRandomize:
            rf = row[2]
            bf = row[1]
            rwin = row[4]
            bwin = row[3]
        else:
            rf = row[1]
            bf = row[2]
            rwin = row[3]
            bwin = row[4]

        if rwin != bwin:
            temp_ar.append(rf)
            temp_ar.append(bf)

            winner = 1 if rwin == 1 else 0
            temp_ar.append(winner)

            rf_stats = fighter_stats[rf]
            bf_stats = fighter_stats[bf]

            for index in stat_indexes:
                rstat = rf_stats[index]
                bstat = bf_stats[index]
                temp_ar.append(rstat)
                temp_ar.append(bstat)

            X = pd.concat(
                [pd.DataFrame([temp_ar], columns=fdf_labels), X], ignore_index=True)

    return X


def standardize(X):
    X_norm = X.copy()
    mu = np.mean(X_norm, axis=0)
    sigma = np.std(X_norm, axis=0)
    X_norm = (X_norm - mu)/sigma
    return X_norm


def logistic_regression_predict(date):
    fighter_stats = {}

    with open('C:\\Users\\nateb\\Documents\\Repos\\python\\ufc-event-predictor\\ufc_predictor\\logistic_regression\\temp_data\\fighters.csv', mode='r') as inp:
        reader = csv.reader(inp)
        fighter_stats = {rows[0]: rows[0:] for rows in reader}

    fights_df = pd.read_csv(
        'C:\\Users\\nateb\\Documents\\Repos\\python\\ufc-event-predictor\\ufc_predictor\\logistic_regression\\temp_data\\fights.csv')

    future_df = pd.read_csv(
        'C:\\Users\\nateb\\Documents\\Repos\\python\\ufc-event-predictor\\ufc_predictor\\logistic_regression\\temp_data\\future_fights.csv')

    # grab event name
    event_name = future_df.loc[future_df["date"] ==
                               date].reset_index().loc[0, "event_name"]
    future_df = construct_fight_dataframe(
        future_df.loc[future_df["date"] == date], fighter_stats, False)

    fights_df = construct_fight_dataframe(fights_df, fighter_stats, False)

    future_X = future_df.loc[:, "rwins":].astype(float).to_numpy()
    future_X = standardize(future_X)

    # Get data for model
    X = fights_df.loc[:, "rwins":].astype(float).to_numpy()
    X_norm = standardize(X)
    y = fights_df.loc[:, "winner"].astype(float).to_numpy()

    clf = LogisticRegression(random_state=2)

    # Use Recursive Feature Elimation for feature selection
    rfe = RFE(clf)
    fit = rfe.fit(X_norm, y)
    # filter to only the best variables
    X_norm = X_norm[:, fit.support_]
    rows, columns = X_norm.shape
    X_norm = np.concatenate([np.ones((rows, 1)),
                             X_norm], axis=1)
    future_X = future_X[:, fit.support_]
    future_X = np.concatenate([np.ones((future_X.shape[0], 1)),
                               future_X], axis=1)

    # fit model
    clf.fit(X_norm, y)
    clf_predictions = clf.predict(future_X).tolist()

    r_fighters = future_df.loc[:, "rf"].values.tolist()
    b_fighters = future_df.loc[:, "bf"].values.tolist()

    return clf_predictions, r_fighters, b_fighters, event_name
