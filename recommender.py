import pandas as pd
import numpy as np

from scipy.sparse.linalg import svds

NUM_RATINGS = 10000     # len(df)
NUM_CONTEXTUAL_FACTORS = 2
MAX_NUM_CONTEXTUAL_CONDITIONS = 4
LAMBDA = 0.2

# Much slower with dtype={"rating": bool}
df = pd.read_csv("datasets/data.csv", dtype={"weekend": int})
df = df.sample(NUM_RATINGS)
df = df.reset_index(drop=True)

NUM_ITEMS = len(df["track_id"].unique())
NUM_USERS = len(df["user_id"].unique())

print("|D| = {}. The number of tracks.".format(NUM_ITEMS))
print("|U| = {}. The number of users.".format(NUM_USERS))


# Pivot so that we have one row per user and one column per track.
R = df.pivot_table(index="user_id", columns="track_id", values='rating').fillna(0)

# Normalise by users' means and convert to NumPy array. Differs from source code; see comment section.
mean = np.array(R.mean(axis=1))
demeaned = R.sub(mean, axis=0).fillna(0).values

print(demeaned.shape)   # (7026, 6188). No. users x no. tracks. 

# That can be our initial guess for k.
# Then we keep going, round and round.
# This is going to be pretty fuckin' expensive.
# That's fine, of course.
# This will take decades to train, mind you.
# I don't have to unwrap V or Q, just recalculate k.

# Perform singular value decomposition (SVD).
d = min(demeaned.shape[0] - 1, 25)
V, SIGMA, Q = svds(demeaned, k=d)

SIGMA = np.diag(SIGMA)

print("\nV = |U| x d = {} x {}. Each row is the strength of association between a USER and features.".format(*V.shape))
print("Q = |D| x d = {} x {}. Each row is the strength of association between an ITEM and features.".format(*Q.shape))

# Calculate predictions and put into a dataframe
predictions = np.dot(np.dot(V, SIGMA), Q) + mean.reshape(-1, 1)
predictions = pd.DataFrame(predictions, columns=R.columns)
predictions.index.names = ["user_id"]

# Initialise B randomly
B = np.random.rand(MAX_NUM_CONTEXTUAL_CONDITIONS, NUM_CONTEXTUAL_FACTORS)

# This will assume a certain format. It might actually be nicer to have them in separate tables

Q = Q.T

# So we want to minimise this function. x must be a 1-D array, which we can then unravel.
# Itself a complex operation, mind you!

# We are going to need these shapes.
# Hol' up. We're optimising V and Q also.
# Which means we'll have to include it ALL.
# Unfortunate.
# So it's just B?
# Or do I?
# In theory, yes. So long as my function is fast... I think.

# x = np.concatenate((V, Q, B), axis=None)  # Flattens matrices before concatenation
#
# def cost_II(x, R):
#
#     V = x[]



# Is R fixed? Yes.

def cost(R, V, Q, B):

    cost_sum = 0

    for row in R.itertuples():

        index = row[0]
        u = row[1]  # user_id
        i = row[2]  # track_id
        c = row[-NUM_CONTEXTUAL_FACTORS - 1:-1]  # context
        r = row[-1]  # rating

        v_u = V[index]
        q_i = Q[index]

        term = (r - np.dot(v_u, q_i) - sum([B[c[k], k] for k in range(2)])) ** 2

        regularisation = LAMBDA * (np.dot(v_u, v_u) + np.dot(q_i, q_i) + np.sum(B ** 2))

        cost_sum += term + regularisation

    return cost_sum


# SGD is sensitive to feature scaling
# Converges after approx 10 ^ 6 training examples.

print(V.shape)  # (7877, 25)

q = V.shape

x = V.flatten() # (198700, )

# We also want to optimise k, though. We do that separately I believe.

print(x.shape)

z = x.reshape(q)

print(z.shape)

# Easy as taking candy off a baby.
# Okay.

params = np.concatenate((V, Q, B), axis=None)  # Flattens matrices before concatenation

# Excellent. 350,000 parameters. Very trainable.
# Huh. I need my custom loss function.

print(params.shape)

# print(V.flatten().shape)

# Parameters are in V, Q, b, and B.
