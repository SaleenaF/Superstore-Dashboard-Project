import kagglehub
import os
import numpy as np  # useful for many scientific computing in Python
import pandas as pd # primary data structure library
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots
import calendar
from datetime import datetime
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# ==============================
# STEP 1: Download Dataset
# ==============================
path = kagglehub.dataset_download("himanshuuike/superstore-sales-dataset")
print("Dataset path:", path)

files = os.listdir(path)
print("Files:", files)

file_path = os.path.join(path, files[0])
df = pd.read_csv(file_path)

os.makedirs("data", exist_ok=True)
os.makedirs("visuals", exist_ok=True)

df.to_csv("data/unclean_superstore_data.csv", index=False)

print(df.head())
print(df.info())

# ==============================
# STEP 2: Data Cleaning
# ==============================

df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

print(df.isnull().sum())

df = df.drop_duplicates()
df = df.dropna()

df.shape

# ==============================
# STEP 3: Feature Engineering
# ==============================

df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month

df['Profit Margin'] = df['Profit'] / df['Sales'].replace(0, 1)

# ==============================
# STEP 4: EDA
# ==============================

total_sales = df['Sales'].sum()
print("Total Sales:", total_sales)

print(df['Sales'].describe())
print(df['Profit'].describe())

sales_by_category = df.groupby('Category')['Sales'].sum()
print(sales_by_category)

profit_by_region = df.groupby('Region')['Profit'].sum()
print(profit_by_region)

monthly_sales = df.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
print(monthly_sales.head())

# ==============================
# STEP 5: SAVE CLEANED DATA
# ==============================

df.to_csv("data/cleaned_superstore_data.csv", index=False)

print(df.shape)
print("Cleaned dataset saved.")