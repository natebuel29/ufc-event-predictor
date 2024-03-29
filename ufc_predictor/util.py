from . import db, ml_models
import random
import pandas as pd
import numpy as np
import pendulum
import logging
from ufc_predictor.models.neural_net_model import *

fdf_labels = ['rf', 'bf', 'winner', 'rwins', 'bwins', 'rloses', 'bloses', 'rslpm', 'bslpm', 'rstrac', 'bstrac', 'rsapm', 'bsapm', 'rstrd', 'bstrd', 'rtdav',
              'btdav', 'rtdac', 'btdac', 'rtdd', 'btdd', 'rsubav', 'bsubav']
future_df_labels = ['date', 'event_name', 'rf', 'bf', 'rwins', 'bwins', 'rloses', 'bloses', 'rslpm', 'bslpm', 'rstrac', 'bstrac', 'rsapm', 'bsapm', 'rstrd', 'bstrd', 'rtdav',
                    'btdav', 'rtdac', 'btdac', 'rtdd', 'btdd', 'rsubav', 'bsubav']
stat_indexes = [3, 4, 12, 13, 14, 15, 16, 17, 18, 19]


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


def construct_future_fight_dataframe(df, fighter_stats):
    X = pd.DataFrame(columns=future_df_labels)
    for row in df.itertuples():
        temp_ar = []
        date = row[3]
        rf = row[1]
        bf = row[2]
        event_name = row[6]
        temp_ar.append(date)
        temp_ar.append(event_name)
        temp_ar.append(rf)
        temp_ar.append(bf)

        rf_stats = fighter_stats[rf]
        bf_stats = fighter_stats[bf]
        for index in stat_indexes:
            rstat = rf_stats[index]
            bstat = bf_stats[index]
            temp_ar.append(rstat)
            temp_ar.append(bstat)
        X = pd.concat(
            [pd.DataFrame([temp_ar], columns=future_df_labels), X], ignore_index=True)
    return X


def fit_ml_models():
    logging.info("Refitting the ML models")
    fights_df = db.get_past_matchups()
    X, y = genererate_inputs_n_labels(fights_df)
    ml_models.log_reg_clf.fit(X, y)
    X = add_bias(X)
    ml_models.svm_clf.fit(X, y)
    y = y.reshape(y.shape[0], 1)
    ml_models.nn_clf.add(Layer_Dense(X.shape[1], 128, weight_regularizer_l2=1e-4,
                                     bias_regularizer_l2=1e-4))
    ml_models.nn_clf.add(Activation_ReLU())
    ml_models.nn_clf.add(Layer_Dense(128, 128, weight_regularizer_l2=1e-4,
                                     bias_regularizer_l2=1e-4))
    ml_models.nn_clf.add(Activation_ReLU())
    ml_models.nn_clf.add(Layer_Dense(128, 1))
    ml_models.nn_clf.add(Activation_Sigmoid())

    ml_models.nn_clf.set(loss=Loss_BinaryCrossentropy(),
                         optimizer=Optimizer_Adam(decay=1e-9), accuracy=Accuracy_Categorical(binary=True))
    ml_models.nn_clf.finalize()
    ml_models.nn_clf.train(X, y, epochs=60, print_every=50)


def genererate_inputs_n_labels(fights_df):
    # Get data for model
    X = fights_df.loc[:, 4:].astype(float).to_numpy()
    X = ml_models.standard_scalar.fit_transform(X)
    y = fights_df.loc[:, 3].astype(float).to_numpy()

    return X, y


def saturday_date():
    if pendulum.now().weekday() == 6:
        saturday_date = pendulum.now().previous(pendulum.SATURDAY).format('YYYY-MM-DD')
    elif pendulum.now().weekday() != 5:
        saturday_date = pendulum.now().next(pendulum.SATURDAY).format('YYYY-MM-DD')
    else:
        saturday_date = pendulum.now().format('YYYY-MM-DD')

    return saturday_date


def event_data(future_df):
    future_X = future_df.loc[:, 6:].astype(float).to_numpy()
    future_X = ml_models.standard_scalar.transform(future_X)
    r_fighters = future_df.loc[:, 4].values.tolist()
    b_fighters = future_df.loc[:, 5].values.tolist()
    event_name = future_df.loc[1, 3]

    return future_X, r_fighters, b_fighters, event_name


def add_bias(X):
    rows, columns = X.shape
    X = np.concatenate([np.ones((rows, 1)),
                        X], axis=1)
    return X
