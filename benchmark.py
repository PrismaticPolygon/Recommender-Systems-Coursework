import os

import pandas as pd
import numpy as np

from recommender import C

B = np.load(os.path.join("weights", "B.npy"))

# Sum up contexts for all ratings
contexts = np.sum(B * C, axis=(1, 2))

# Just ratings and predictions
P = pd.read_csv(os.path.join("weights", "P.csv"))

# With context
df = pd.read_csv(os.path.join("weights", "df.csv"))

# Calculate MAE
mae = np.mean(df.apply(lambda row: abs(row["rating"] - row["prediction"]), axis=1))

print("MAE: {}".format(mae))

# Calculate MAE with contextual weights
mae_b = np.mean(df.apply(lambda row: abs(row["rating"] - row["prediction"] - contexts[row.name]), axis=1))

print("MAE_B: {}".format(mae_b))
print("Improvement: {:.2f}%".format(100 * (mae_b - mae) / mae))
print("")

TP = np.sum((P["rating"] == 1.0) & (P["prediction"] > 0.5))
FP = np.sum((P["rating"] == 0.0) & (P["prediction"] > 0.5))
TN = np.sum((P["rating"] == 0.0) & (P["prediction"] < 0.5))
FN = np.sum((P["rating"] == 1.0) & (P["prediction"] < 0.5))

print("Number of true positives: {}".format(TP))
print("Number of false positives: {}".format(FP))
print("Number of true negatives: {}".format(TN))
print("Number of false negatives: {}".format(FN))
print("")

accuracy = TP / (TP + FP)
recall = TP / (TP + TN)

print("Accuracy: {}".format(accuracy))
print("Recall: {}".format(recall))


