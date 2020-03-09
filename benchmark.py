import os

import pandas as pd
import numpy as np

from recommender import C

B = np.load(os.path.join("weights", "B.npy"))

print("Loaded context matrix B {}".format(B.shape))

# Sum up contexts for all ratings
contexts = np.sum(B * C, axis=(1, 2))

df = pd.read_csv("weights/df.csv")

mae = np.mean(df.apply(lambda row: row["rating"] - row["prediction"], axis=1))

print("MAE: {}".format(mae))

mae_b = np.mean(df.apply(lambda row: row["rating"] - row["prediction"] - contexts[row.name], axis=1))

print("MAE with context: {}".format(mae_b))

print("Improvement: {:.2f}%".format(100 * (mae_b - mae) / mae))

# Let's call it a difference of... 50%. I suspect we can afford to be harsh.
# But we will have to join up P appropriately. And we did! We don't have context for our predictions, hence the duplicates. 

# We need to compute precision and recall.
# Precision is true positives / all positives.
# This is prediction territory. So we need the P.
