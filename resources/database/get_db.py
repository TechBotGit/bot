import pandas as pd

file = "database.xlsx"

load = pd.ExcelFile(file)

print(load.sheet_names)

df1 = load.parse('Sheet1')
print(df1.head())
