import pandas as pd
import numpy as np

from scipy.sparse.linalg import svds

# http://www.quuxlabs.com/blog/2010/09/matrix-factorization-a-simple-tutorial-and-implementation-in-python/

# Much slower with dtype={"rating": bool}
df = pd.read_csv("datasets/data.csv")

df = df.drop(["twitter-id", "artist-id", "country"], axis=1)

df = df.set_index("user-id")

print(df.head())

index = [x for x in range(136867)]

df = df.reindex(index, axis="index")

# I'm close to losing my damn mind here.
# Let's chill. I only have to do this once, after all, in pre-process.

#
print(df.head())
#
# print(df.index.value_counts())

# 136867 unique users.
# There's no good way to normalise them. reset_index? drop_index? re_index>

# print(df.head())

# df = df[:10000]
# df = df.reset_index()
#
# print(df.columns)
#
# print("|D| = {}. The number of tracks.".format(len(df["track-id"].unique())))
# print("|U| = {}. The number of users.".format(len(df["user-id"].unique())))
#
# # Pivot so that we have one row per user and one column per track.
# R = df.pivot_table(index="user-id", columns="track-id", values='rating').fillna(0)
#
# # Normalise by users' means and convert to NumPy array. Differs from source code; see comment section.
# mean = np.array(R.mean(axis=1))
# demeaned = R.sub(mean, axis=0).fillna(0).values
#
# # Perform singular value decomposition (SVD).
# d = min(demeaned.shape[0] - 1, 25)
# V, SIGMA, Q = svds(demeaned, k=d)
#
# Q = np.transpose(Q)
# SIGMA = np.diag(SIGMA)
#
# print("\nV = |U| x d = {} x {}. Each row is the strength of association between a USER and features.".format(*V.shape))
# print("Q = |D| x d = {} x {}. Each row is the strength of association between an ITEM and features.".format(*Q.shape))
#
# # # Calculate predictions and put into a dataframe
# # predictions = np.dot(np.dot(V, SIGMA), Q) + mean.reshape(-1, 1)
# # predictions = pd.DataFrame(predictions, columns=R.columns)
# # predictions.index.names = ["user-id"]
#
# # Create contextual factors matrix of shape (R, K, k), where R is the number of ratings, K is the maximum number
# # of contextual conditions for a single contextual factor, and k is the number of contextual factors.
# c = df[["weekend", "season"]]
#
# c.at[0, "season"] = 3
# c.at[5000, "season"] = 1
# c.at[9999, "season"] = 2
#
# # c = c.pivot_table(index=[c.index, "season"], values=["season", "weekend"])
#
# c = np.random.rand(10000, 4, 2)
#
# print(c.shape)
#
# # |B| = K x k (max no. contextual conditions x no. contextual factors)
# B = np.random.rand(4, 2)
# #
# # # a = B * np.transpose(contexts)
# # #
# # # Wrong shape. If I tranposed one, mind you...
# # # print(a.shape)
# #
# #
# # print(R.shape)
# # I suppose that one, or the other, should be transpose for my scalar value.
#
# x = c[0]    # (4, 2)
# # q = x @ B   # Matrix multiplication Elementwise sum?
#
# print(np.sum(np.multiply(B, x)))

# Okay.
# There's no-one that one should be 74 million. God knows where they got that from.
# Make it the index and then reset it?




# That seems to work.


# Doesn't error out. It must be the weights. Right? And

# print(q.shape)


# And the specific row is indexed by the r_UI. Okay.
#
# r_uic = df.iloc[0].values
#
# # So now we're back to our indexing problem.
# # I need to map those IDs from the present range to 0 to however many there are.
#
# # How is there a 0? Ah. That's the index.
#
#
# print(r_uic)
#
# print(R.shape)
#
# y = R - np.dot(V, Q) - np.sum(B, axis=1)
#
# print(np.dot(V, Q).shape)   # 5339, 6033. Shouldn't it be 10,000?
#
# # That needs to be times the contextual factors.
#
# print(y.shape)  # (5339, 6033).

# Curious, as we have 10000 ratings...


# Disregard i_bar and b_u. The former is the average of item ratings in R, which is 1. I don't know what b_u is. Perhaps... the user's mean. Also 1.
# for _, user in df.iterrows():
#
#     u = user["user-id"]
#
#     # track_ids similarly need re-indexing.
#     # Which isn't that easy to do.
#     # Must be a dataframe itself.
#     # Perhaps matrix IS the way forwards.
#
#     for x in df.loc[df["user-id"] == u]:
#
#         print(x)

    # r = row["rating"]
    # i = row["track-id"]
    # c1 = row["country"]
    # c2 = row["weekend"]
    # c3 = row["season"]

    # print("\n{} = ({}, {}, {}, {}, {})".format(r, u, i, c1, c2, c3))



    # break

# Excellent.