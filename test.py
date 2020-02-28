import pandas as pd
import numpy as np

from scipy.sparse.linalg import svds

# http://www.quuxlabs.com/blog/2010/09/matrix-factorization-a-simple-tutorial-and-implementation-in-python/

# Much slower with dtype={"rating": bool}
df = pd.read_csv("datasets/data.csv")
df = df[:10000]

print("|D| = {}. The number of tracks.".format(len(df["track_id"].unique())))
print("|U| = {}. The number of users.".format(len(df["user_id"].unique())))

# Pivot so that we have one row per user and one column per track.
R = df.pivot_table(index="user_id", columns="track_id", values='rating').fillna(0)

# # Normalise by users' means and convert to NumPy array. Differs from source code; see comment section.
mean = np.array(R.mean(axis=1))
demeaned = R.sub(mean, axis=0).fillna(0).values

# Perform singular value decomposition (SVD).
d = min(demeaned.shape[0] - 1, 25)
V, SIGMA, Q = svds(demeaned, k=d)

SIGMA = np.diag(SIGMA)

print("\nV = |U| x d = {} x {}. Each row is the strength of association between a USER and features.".format(*V.shape))
print("Q = |D| x d = {} x {}. Each row is the strength of association between an ITEM and features.".format(*Q.shape))

# Calculate predictions and put into a dataframe
predictions = np.dot(np.dot(V, SIGMA), Q) + mean.reshape(-1, 1)
predictions = pd.DataFrame(predictions, columns=R.columns)
predictions.index.names = ["user-id"]

np.random.seed(1)

# |B| = K x k (max no. contextual conditions x no. contextual factors)
B = np.random.rand(4, 2)

# |c| = max no. contextual conditions x no contextual factors (in CAMF-C)
c = np.array([[0, 1], [0, 0], [1, 0], [0, 0]])


for index, r_uic in df.iterrows():

    r = r_uic["rating"]
    u = r_uic["user_id"]
    i = r_uic["track_id"]

    c = [r_uic["season"], int(r_uic["weekend"])]

    print(c)

    v_u = V[index]
    q_i = Q[:, index]   # It's unclear whether Q ought to be transposed; get the column

    y = (r - np.dot(v_u, q_i) - sum([B[c[k], k] for k in range(2)])) ** 2

    regularisation = np.dot(v_u, v_u) + np.dot(q_i, q_i) + np.sum(B ** 2)

    # And the user's baseline.
    # Do I know this? How is it calculated?

    # Er

    # Nice. Now we just need that regularisation term

    print(y)

    break