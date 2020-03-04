import pandas as pd
import numpy as np

from scipy.sparse.linalg import svds
from scipy.optimize import minimize

NUM_USERS = 10
CONTEXTUAL_FACTORS = ["country", "season", "weekend"]
LAMBDA = 0.2                                            # Learning rate

df = pd.read_csv("datasets/data.csv")

# Select users with IDs from 0 to NUM_USERS
df = df.loc[df['user_id'].isin([x for x in range(NUM_USERS)])]

# Drop unused contextual factors
df = df.drop(["city", "month"], axis=1)

# Convert country to category. Should probably one-hot encode.
df["country"] = df["country"].astype("category").cat.codes

NUM_RATINGS = len(df)
NUM_ITEMS = len(df["track_id"].unique())
MAX_NUM_CONTEXTUAL_CONDITIONS = max([len(df[context].unique()) for context in CONTEXTUAL_FACTORS])

print("\nNumber of items |D| = {}".format(NUM_ITEMS))
print("Number of users |U| = {}".format(NUM_USERS))
print("Number of ratings |R| = {}".format(NUM_RATINGS))
print("")

# Pivot so that we have one row per user and one column per track.
R = df.pivot_table(index="user_id", columns="track_id", values='rating').fillna(0)

# Normalise by users' means and convert to NumPy array. Differs from source code; see comment section.
mean = np.array(R.mean(axis=1))
demeaned = R.sub(mean, axis=0).fillna(0).values

# Perform SVD
d = min(demeaned.shape[0] - 1, 25)

print("Number of latent dimensions d = {}".format(d))

V, SIGMA, Q = svds(demeaned, k=d)

# Convert to a diagonal for matrix multiplication
SIGMA = np.diag(SIGMA)

print("User matrix V = |U| x d = {} x {}".format(*V.shape))
print("Item matrix Q = d x |D| = {} x {}".format(*Q.shape))

# Randomly initialise context weights
B = np.random.rand(len(CONTEXTUAL_FACTORS), MAX_NUM_CONTEXTUAL_CONDITIONS)

print("Context matrix B = no. factors x no. conditions = {} x {}".format(*B.shape))
print("")

# Compute predicted ratings
P = np.dot(np.dot(V, SIGMA), Q) + mean.reshape(-1, 1)

# Convert back to DataFrame and reformat so that each row is a tuple (user_id, item_id, prediction)
P = pd.DataFrame(P)
P.index.name = "user_id"
P = P.reset_index()
P = pd.melt(P, id_vars=["user_id"], var_name="track_id", value_name="prediction")

# Merge onto original DataFrame.
df = df.merge(P, on=["user_id", "track_id"])

# Create context matrix
C = np.zeros((NUM_RATINGS, len(CONTEXTUAL_FACTORS), MAX_NUM_CONTEXTUAL_CONDITIONS), dtype=np.uint8)

for i, row in df.iterrows():

    for j, context in enumerate(CONTEXTUAL_FACTORS):

        C[i, j, row[context]] = 1

# np.sum(V * V, axis=(1, 0)) is the sum (axis=0) of the row-wise (axis=1) dot product of V
# https://stackoverflow.com/questions/15616742/vectorized-way-of-calculating-row-wise-dot-product-two-matrices-with-scipy
regularisation = np.sum(V * V, axis=(1, 0)) ** 2 + np.sum(Q * Q, axis=(1, 0)) ** 2

print("Optimising context weights...")


def cost(B):

    B = B.reshape(len(CONTEXTUAL_FACTORS), MAX_NUM_CONTEXTUAL_CONDITIONS)

    contexts = np.sum(B * C, axis=(1, 2))
    ratings = df["rating"].values
    predictions = df["prediction"].values

    cost_sum = (ratings - predictions - contexts) ** 2 + LAMBDA * (regularisation + np.sum(B ** 2))

    return np.sum(cost_sum)


result = minimize(cost, B, method="BFGS")

B = result.x.reshape(len(CONTEXTUAL_FACTORS), MAX_NUM_CONTEXTUAL_CONDITIONS)

print(B)
