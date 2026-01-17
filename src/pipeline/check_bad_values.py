import pandas as pd

df = pd.read_csv("data/raw/clinical_trials_10000.csv", dtype=str)
bad = (df == "nan").sum().sum()
print("Count of literal 'nan' strings:", bad)
