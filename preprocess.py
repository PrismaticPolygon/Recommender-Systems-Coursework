import pandas as pd
import numpy as np

from functools import partial

df = pd.read_csv("datasets/raw.csv", index_col="twitter-id")

# Can't drop other IDs without risking duplicates, particularly for track-id
df = df.drop(["country-id"], axis=1)


# Okay. Let's get down to business. We wanted very limited dimensions to start with.
# Whether it's a weekday or weekend.

def cyclical(column, column_range, type):
    """
    A cylical transform, as explained at http://blog.davidkaleko.com/feature-engineering-cyclical-features.html.
    Reputedly better than one-hot encoding the target variable.
    :param column: the target variable.
    :param column_range: the range of values. Explicit as the dataset doesn't contain 12 months.
    :param type: sin or cos. Gets around creating two columns using 'apply', which is very slow.
    :return:
    """

    if type == "sin":

        return np.sin(column * (2. * np.pi / column_range))

    elif type == "cos":

        return np.cos(column * (2. * np.pi / column_range))

    raise ValueError("type must be either 'sin' or 'cos'")


# Weekdays run from 0 to 6
df["weekend"] = df["weekday"] >= 5

# df = df.drop(["weekday"], axis=1)

# Data was collected between 11/11 and 09/11
# df["year"] = df["month"].map(lambda month: 2011 if month > 9 else 2012)


def season(month):

    if month in [11, 12, 1]:

        return 0    # Winter

    elif month in [2, 3, 4]:

        return 1    # Spring

    elif month in [5, 6, 7]:

        return 2    # Summer

    elif month in [8, 9, 10]:

        return 3    # Autumn


df["season"] = df["month"].map(season)
#
# weekday = partial(cyclical, column_range=7)
# month = partial(cyclical, column_range=12)
#
# df["weekday_sin"] = df["weekday"].map(partial(weekday, type="sin"))
# df["weekday_cos"] = df["weekday"].map(partial(weekday, type="cos"))
#
# df["month_sin"] = df["month"].map(partial(month, type="sin"))
# df["month_cos"] = df["month"].map(partial(month, type="cos"))

# Every film has a rating of 1: watched. This is a classification, not regression, problem.
df["rating"] = 1

df = df.drop(["month", "weekday"], axis=1)
df = df.drop(["longitude", "latitude", "city-id", "artist", "track", "city"], axis=1)

print(df.columns)

df.to_csv("datasets/data.csv")


