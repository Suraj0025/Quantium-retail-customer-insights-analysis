import pandas as pd
import numpy as np
import scipy
print (scipy.__version__)
from scipy.stats import pearsonr, ttest_ind
import matplotlib.pyplot as plt

file_path = r'C:\Users\Suraj\Downloads\QVI_data.csv'
data = pd.read_csv(file_path)

# Inspect the DATE column
print(data['DATE'].head())
print(data['DATE'].dtype)

# Convert DATE to datetime format
data['DATE'] = pd.to_datetime(data['DATE'], errors='coerce')

# Check for invalid dates
if data['DATE'].isna().sum() > 0:
    print("Invalid dates found. Removing them...")
    data = data.dropna(subset=['DATE'])

# Extract month and year for aggregation
data['MONTH'] = data['DATE'].dt.to_period('M')

metrics = data.groupby(["STORE_NBR", "MONTH"]).agg(total_sales=("TXN_ID", "count"), total_customers=("LYLTY_CARD_NBR", "nunique"), total_transactions=("TXN_ID", "nunique")).reset_index()

metrics["transactions_per_customer"] = metrics["total_transactions"] / metrics["total_customers"]

def find_control_store(trial_store, metrics):
   trial_metrics = metrics[metrics["STORE_NBR"] == trial_store].set_index("MONTH")
   other_stores = metrics[metrics["STORE_NBR"] != trial_store].groupby("STORE_NBR")

   correlations = {}
   for store, group in other_stores:
      control_metrics = group.set_index("MONTH")
      common_months = trial_metrics.index.intersection(control_metrics.index)
      if len(common_months) > 0:
         corr, _ = pearsonr(trial_metrics.loc[common_months, "total_sales"], control_metrics.loc[common_months, "total_sales"])
         correlations[store] = corr
   return max(correlations, key=correlations.get)

trial_stores = [77, 86, 88]
control_stores = {trial_store: find_control_store(trial_store, metrics) for trial_store in trial_stores}
print("Control Stores Selected:", control_stores)

results = []

for trial_store, control_store in control_stores.items():
   trial_data = metrics[metrics["STORE_NBR"] == trial_store]
   control_data = metrics[metrics["STORE_NBR"] == control_store]

   trial_period = trial_data["MONTH"].unique()[-3:]
   trial_sales = trial_data[trial_data["MONTH"].isin(trial_period)]["total_sales"]
   control_sales = control_data[control_data["MONTH"].isin(trial_period)]["total_sales"]

t_stat, p_val = ttest_ind(trial_sales, control_sales)

results.append({"Trial_Store": trial_store, "Control Store": control_store, "T-statistic": t_stat, "P-value": p_val})
results_df = pd.DataFrame(results)
print("\nTrial vs Control Store Comparison Result:")
print(results_df)

for trial_store, control_store in control_stores.items():
   trial_data = metrics[metrics["STORE_NBR"] == trial_store]
   control_data = metrics[metrics["STORE_NBR"] == control_store]

   plt.figure(figsize=(10,6))
   plt.plot(trial_data["MONTHS"], trial_data["total_sales"], label=f"Trial Stores {trial_store}", marker="o")
   plt.plot(control_data["MONTHS"], control_data["total_sales"], label=f"Control Store {control_store}", marker="o")
   plt.title(f"Sales Comparison: Trial Store {trial_store} vs Control Store {control_store}")
   plt.xlabel("Month")
   plt.ylabel("Total Sales")
   plt.legend()
   plt.grid()
   plt.show()





   