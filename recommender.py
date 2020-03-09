import os
import pandas as pd
import numpy as np

from scipy.sparse.linalg import svds
from scipy.optimize import minimize

NUM_USERS = 100        # 100

CONTEXTUAL_FACTORS = ["country", "season", "weekend"]
LAMBDA = 0.2                                            # Learning rate

df = pd.read_csv(os.path.join("data", "events.csv"), dtype={"rating": np.uint8})

if NUM_USERS is not None:

    # Select users with IDs from 0 to NUM_USERS
    df = df.loc[df['user_id'].isin([x for x in range(NUM_USERS)])]

NUM_USERS = len(df["user_id"].unique())

# Drop unused contextual factors
df = df.drop(["city", "month"], axis=1)

# Convert country to category. Should probably one-hot encode.
df["country"] = df["country"].astype("category").cat.codes

NUM_RATINGS = len(df)
NUM_ITEMS = len(df["track_id"].unique())
MAX_NUM_CONTEXTUAL_CONDITIONS = max([len(df[context].unique()) for context in CONTEXTUAL_FACTORS])

# Create context matrix
C = np.zeros((NUM_RATINGS, len(CONTEXTUAL_FACTORS), MAX_NUM_CONTEXTUAL_CONDITIONS), dtype=np.uint8)

for i, row in df.iterrows():

    for j, context in enumerate(CONTEXTUAL_FACTORS):

        C[i, j, row[context]] = 1

if __name__ == "__main__":

    print("\nNumber of items |D| = {}".format(NUM_ITEMS))
    print("Number of users |U| = {}".format(NUM_USERS))
    print("Number of ratings |R| = {}".format(NUM_RATINGS))
    print("")

    # Pivot so that we have one row per user and one column per track.
    R = df.pivot_table(index="user_id", columns="track_id", values='rating').fillna(0)

    # That will be changed the dtype.
    # After all, they are all ones and zeros...

    # Normalise by users' means and convert to NumPy array. Differs from source code; see comment section.
    mean = np.array(R.mean(axis=1))
    demeaned = R.sub(mean, axis=0).fillna(0).values

    # Perform SVD
    d = min(demeaned.shape[0] - 1, 25)

    print("Number of latent dimensions d = {}".format(d))
    print("")

    # It's P, not R!

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

    print(P)

    # Merge actual ratings onto P. Fill un-rated (i.e. unlistened to) events with 0
    # P = P.merge(df, on=["user_id", "track_id"], how="left").fillna(0)

    # Merge onto original DataFrame.
    df = df.merge(P, on=["user_id", "track_id"])


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

    if not os.path.exists("weights"):

        os.mkdir("weights")

    np.save(os.path.join("weights", "B"), B)
    P.to_csv(os.path.join("weights", "P.csv"), index=False)

    with open(os.path.join("weights", "log.txt"), "w") as log:

        log.write(str(result))
