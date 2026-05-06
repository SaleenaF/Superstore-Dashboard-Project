import kagglehub
import pandas as pd
import os

# ==============================
# STEP 1: Download Dataset
# ==============================
path = kagglehub.dataset_download("himanshuuike/superstore-sales-dataset")
print("Dataset path:", path)

# Find CSV file inside folder
files = os.listdir(path)
print("Files:", files)

# Load dataset (adjust filename if needed)
file_path = os.path.join(path, files[0])
df = pd.read_csv(file_path)

# Preview
print(df.head())
print(df.info())

# ==============================
# STEP 2: Data Cleaning
# ==============================

# Convert date column
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Handle missing values
print(df.isnull().sum())
df = df.dropna()  # or fillna() if needed

# Remove duplicates
df = df.drop_duplicates()

# ==============================
# STEP 3: Feature Engineering
# ==============================

df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month

# Optional: Profit Margin
df['Profit Margin'] = df['Profit'] / df['Sales']

# ==============================
# STEP 4: Basic EDA
# ==============================

# Total Sales
total_sales = df['Sales'].sum()
print("Total Sales:", total_sales)

# Sales by Category
sales_by_category = df.groupby('Category')['Sales'].sum()
print(sales_by_category)

# Profit by Region
profit_by_region = df.groupby('Region')['Profit'].sum()
print(profit_by_region)

# Monthly Sales Trend
monthly_sales = df.groupby(['Year', 'Month'])['Sales'].sum().reset_index()
print(monthly_sales.head())

# ==============================
# STEP 5: Save Clean Data (optional)
# ==============================

df.to_csv("cleaned_superstore_data.csv", index=False)