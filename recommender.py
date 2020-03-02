import pandas as pd
import numpy as np

from scipy.sparse.linalg import svds
from scipy.optimize import minimize

NUM_RATINGS = 10000     # len(df)
NUM_CONTEXTUAL_FACTORS = 2
MAX_NUM_CONTEXTUAL_CONDITIONS = 4
LAMBDA = 0.2

# Much slower with dtype={"rating": bool}
df = pd.read_csv("datasets/data.csv", dtype={"weekend": int})
df = df[:NUM_RATINGS]

NUM_ITEMS = len(df["track_id"].unique())
NUM_USERS = len(df["user_id"].unique())

print("|D| = {}. The number of tracks.".format(NUM_ITEMS))
print("|U| = {}. The number of users.".format(NUM_USERS))

# Pivot so that we have one row per user and one column per track.
R = df.pivot_table(index="user_id", columns="track_id", values='rating').fillna(0)

# Normalise by users' means and convert to NumPy array. Differs from source code; see comment section.
mean = np.array(R.mean(axis=1))
demeaned = R.sub(mean, axis=0).fillna(0).values

# Perform SVD
d = min(demeaned.shape[0] - 1, 25)
V, SIGMA, Q = svds(demeaned, k=d)

Q = Q.T

# Randomly initialise context weights
B = np.random.rand(MAX_NUM_CONTEXTUAL_CONDITIONS, NUM_CONTEXTUAL_FACTORS)

def cost(B):

    B = B.reshape(MAX_NUM_CONTEXTUAL_CONDITIONS, NUM_CONTEXTUAL_FACTORS)

    cost_sum = 0

    for row in R.itertuples():

        index = row[0]
        u = row[1]  # user_id
        i = row[2]  # track_id
        c = [int(x) for x in row[-NUM_CONTEXTUAL_FACTORS - 1:-1]]  # context
        r = row[-1]  # rating

        v_u = V[index]
        q_i = Q[index]

        context = sum([B[c[k], k] for k in range(2)])
        term = (r - np.dot(v_u, q_i) - context) ** 2

        regularisation = LAMBDA * (np.dot(v_u, v_u) + np.dot(q_i, q_i) + np.sum(B ** 2))

        cost_sum += term + regularisation

    print("{:.4f}".format(cost_sum))

    return cost_sum


result = minimize(cost, B, method="BFGS")

B = result.x.reshape(MAX_NUM_CONTEXTUAL_CONDITIONS, NUM_CONTEXTUAL_FACTORS)

# Need to extract result

print(B)