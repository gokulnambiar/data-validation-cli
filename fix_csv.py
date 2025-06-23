import pandas as pd

df = pd.read_csv("titanic_valid.csv")

# Fill nulls in 'Age' column with median values from the column
df['Age'] = df['Age'].fillna(df['Age'].median())


df.to_csv("titanic_fixed.csv", index=False)