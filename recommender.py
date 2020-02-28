import pandas as pd
import numpy as np

from scipy.sparse.linalg import svds

# http://www.quuxlabs.com/blog/2010/09/matrix-factorization-a-simple-tutorial-and-implementation-in-python/

# Much slower with dtype={"rating": bool}
df = pd.read_csv("datasets/data.csv")

df = df.drop(["twitter-id", "artist-id"], axis=1)

df = df[:10000]
df = df.reset_index()

print("|D| = {}. The number of tracks.".format(len(df["track-id"].unique())))
print("|U| = {}. The number of users.".format(len(df["user-id"].unique())))

# Pivot so that we have one row per user and one column per track.
R = df.pivot_table(index="user-id", columns="track-id", values='rating').fillna(0)

# Normalise by users' means and convert to NumPy array. Differs from source code; see comment section.
mean = np.array(R.mean(axis=1))
demeaned = R.sub(mean, axis=0).fillna(0).values

# Perform singular value decomposition (SVD).
d = min(demeaned.shape[0] - 1, 25)
V, SIGMA, Q = svds(demeaned, k=d)
SIGMA = np.diag(SIGMA)

print("V = |U| x d = {} x {}. Each row is the strength of association between a USER and features.".format(*V.shape))
print("Q = d x |D| = {} x {}. Each row is the strength of association between an ITEM and features.".format(*Q.shape))

# Calculate predictions and put into a dataframe
predictions = np.dot(np.dot(V, SIGMA), Q) + mean.reshape(-1, 1)
predictions = pd.DataFrame(predictions, columns=R.columns)
predictions.index.names = ["user-id"]

print(predictions)
