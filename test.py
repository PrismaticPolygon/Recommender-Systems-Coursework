import pandas as pd
import numpy as np

from scipy.optimize import minimize
from functools import partial

NUM_RATINGS = 10000     # len(df)
NUM_CONTEXTUAL_FACTORS = 2
MAX_NUM_CONTEXTUAL_CONDITIONS = 4
LAMBDA = 0.2

# Much slower with dtype={"rating": bool}
df = pd.read_csv("datasets/data.csv", dtype={"weekend": int})
# df = df.sample(NUM_RATINGS)
df = df[:NUM_RATINGS]
# df = df.reset_index(drop=True)

NUM_ITEMS = len(df["track_id"].unique())
NUM_USERS = len(df["user_id"].unique())

print("|D| = {}. The number of tracks.".format(NUM_ITEMS))
print("|U| = {}. The number of users.".format(NUM_USERS))

# Pivot so that we have one row per user and one column per track.
R = df.pivot_table(index="user_id", columns="track_id", values='rating').fillna(0)

# Initialise parameters randomly
d = np.random.randint(10, 50, (1, ))

B = np.random.rand(MAX_NUM_CONTEXTUAL_CONDITIONS, NUM_CONTEXTUAL_FACTORS)
V = np.random.rand(NUM_USERS, d[0])
Q = np.random.rand(NUM_ITEMS, d[0])


def cost(x, R):

    d = int(x[0])

    i = 1

    B = x[i: (i + (MAX_NUM_CONTEXTUAL_CONDITIONS * NUM_CONTEXTUAL_FACTORS))]\
        .reshape(MAX_NUM_CONTEXTUAL_CONDITIONS, NUM_CONTEXTUAL_FACTORS)

    i += MAX_NUM_CONTEXTUAL_CONDITIONS * NUM_CONTEXTUAL_FACTORS

    V = x[i: i + (NUM_USERS * d)].reshape(NUM_USERS, d)

    i += NUM_USERS * d

    Q = x[i: i + (NUM_ITEMS * d)].reshape(NUM_ITEMS, d)

    cost_sum = 0

    for row in R.itertuples():

        index = row[0]
        u = row[1]  # user_id
        i = row[2]  # track_id
        c = [int(x) for x in row[-NUM_CONTEXTUAL_FACTORS - 1:-1]]  # context
        r = row[-1]  # rating

        v_u = V[index]
        q_i = Q[index]

        term = (r - np.dot(v_u, q_i) - sum([B[c[k], k] for k in range(2)])) ** 2

        regularisation = LAMBDA * (np.dot(v_u, v_u) + np.dot(q_i, q_i) + np.sum(B ** 2))

        cost_sum += term + regularisation

    print(cost_sum)

    return cost_sum

# Too slow. Remember how fast SVD is?
# Very slow. We have a lot of parameters.


x = np.concatenate((d, B, V, Q), axis=None)
fun = partial(cost, R=R)

result = minimize(fun, x, method="BFGS")    # Everyone seems to use this.

print(result)