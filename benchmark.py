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