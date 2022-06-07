import random
import pandas as pd
import numpy as np

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
