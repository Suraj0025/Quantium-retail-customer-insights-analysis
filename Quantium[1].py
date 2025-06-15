import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file_path = r'C:\Users\Suraj\Downloads\QVI_transaction_data.xlsx'
data = pd.read_excel(file_path)

import openpyxl
print("openpyxl installed successfully!")

import pandas as pd
file_path = r'C:\Users\Suraj\Downloads\QVI_transaction_data.xlsx'
data = pd.read_excel(file_path)
print(data.head())
print(data.tail())
print(data.describe())
print(data.info())
print(data.dropna())

data["DATE"] = pd.to_datetime(data["DATE"], origin="1900-01-01", unit="D")
print(data.head())
print(data.isnull().sum())

data.dropna(inplace=True)

data["BRAND"] = data["PROD_NAME"].str.split().str[0]
data["PACK_SIZE"] = data["PROD_NAME"].str.extract(r"(d+g)")

data["AVG_SALES_PER_UNIT"] = data["TOT_SALES"] / data["PROD_QTY"]

brand_analysis = data.groupby("BRAND").agg({"TOT_SALES": "sum", "PROD_QTY": "sum"}).reset_index()
print("\nBrand Analysis=")
print(brand_analysis)

plt.figure(figsize=(12, 6))
sns.barplot(x="BRAND", y="TOT_SALES", data=brand_analysis)
plt.title("Total Sales by Brand")
plt.xlabel("BRAND")
plt.ylabel("Total_Sales")
plt.show()

store_analysis = data.groupby("STORE_NBR").agg({"TOT_SALES": "sum", "PROD_QTY": "sum"}).reset_index()
print("\nStore Analysis=")
print(store_analysis)

plt.figure(figsize=(12, 6))
sns.barplot(x="STORE_NBR", y="TOT_SALES", data=store_analysis)
plt.title("Total Sales by Store")
plt.xlabel("Store Number")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.show()

output_file_path = r'C:\Users\Suraj\Downloads\QVI_transaction_data_cleaned.xlsx'
data.to_excel(output_file_path, index=False)

print(f"\nData cleaned and saved to {output_file_path}")



