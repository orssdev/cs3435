import pandas as pd
df = pd.read_csv('joined.csv')
print(df.iloc[:, :5].head(n=20))