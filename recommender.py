import pandas as pd

df = pd.read_csv("datasets/data.csv", index_col="twitter-id")

print(df.head())