from dataclasses import dataclass
import pandas as pd
df=pd.read_csv('data.csv')
print(df.columns)
x = df['data'].tolist()
print(x[1])
print(type(x))