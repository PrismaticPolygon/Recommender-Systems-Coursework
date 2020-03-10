import pandas as pd
import numpy as np

P = pd.read_csv("weights/P.csv")
B = np.load("weights/B.npy")

predictions = P[P["user_id"] == 0]

context = {"country": 20, "season": 2, "weekend": 1}

def cost(context, B):

    cumsum = 0

    for i, key in enumerate(context):

        cumsum += B[i, context[key]]

    return cumsum

x = cost(context, B)

# Nice. So it doesn't actually change my predictions. It would if it were item-based.
# Instead, we can only make predictions more accurate.

print(x)

#
# print(B.shape)  (3, 24)
#
# # We just need to one-hot encode it, essentially.
#
# # No need, actually.
# # It should be a simple matter of... AH!
#
# for i, row in predictions.iterrows():
#
#     for j, c in enumerate(CONTEXTUAL_FACTORS):
#
#         C[i, j, row[c]] = 1
#
# # contexts = np.sum(B * C, axis=(1, 2))
#
# print(predictions)
# print(len(predictions))
