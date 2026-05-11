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

# Find CSV file inside folder
files = os.listdir(path)
print("Files:", files)

# Load dataset (adjust filename if needed)
file_path = os.path.join(path, files[0])
df = pd.read_csv(file_path)

# Save ORIGINAL unclean dataset
os.makedirs("data", exist_ok=True)
df.to_csv("data/unclean_superstore_data.csv", index=False)

# Preview
print(df.head())
print(df.info())

# ==============================
# STEP 2: Data Cleaning
# ==============================

# Convert date column
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

# Handle missing values
print(df.isnull().sum())
# Remove duplicates
df = df.drop_duplicates()
df = df.dropna()
# Print the dimensions of the dataframe
df.shape

# ==============================
# STEP 3: Feature Engineering
# ==============================

df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month

# Optional: Profit Margin
df['Profit Margin'] = df['Profit'] / df['Sales'].replace(0, 1)

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
# Step 5: VISUALIZATIONS
# ==============================

# BAR CHART
# Get categories and values as separate lists
categories = sales_by_category.index.tolist()
sales = sales_by_category.values.tolist()

# Create bar chart
plt.figure(figsize=(8, 5))
plt.bar(categories, sales, color='skyblue', edgecolor='black')
# Labels and title
plt.xlabel('Category')
plt.ylabel('Sales')
plt.title('Sales by Category')
# Show values on top of bars
for i, v in enumerate(sales):
    plt.text(i, v + 200, f'${v}', ha='center', fontweight='bold')

plt.tight_layout()
plt.show()
# ==============================

# LINE CHART 1
# Get region and profit as separate lists
region = profit_by_region.index.tolist()
profit = profit_by_region.values.tolist()

plt.figure(figsize=(10, 6))
# Labels and title
plt.xlabel('Region')
plt.ylabel('Profit')
plt.title('Profit by Category')

# Show values on top of bars
for i, v in enumerate(profit):
    plt.text(i, v + 200, f'${v}', ha='center', fontweight='bold')
# Create the line plot
plt.plot(region, profit, marker='o', linewidth=2, markersize=8, color='blue')
plt.show()
# ==============================

# LINE CHART 2
# Group sales by month
monthly_sales = df.groupby(
    pd.Grouper(key='Order Date', freq='ME')
)['Sales'].sum().reset_index()

# Create figure
plt.figure(figsize=(12, 6))

# Plot line chart
plt.plot(
    monthly_sales['Order Date'],
    monthly_sales['Sales'],
    marker='o',
    linewidth=2,
    markersize=6
)

# Labels and title
plt.title('Monthly Sales Trend')
plt.xlabel('Date')
plt.ylabel('Sales')

plt.xticks(rotation=45) # Rotate dates for readability
plt.grid(True)
plt.tight_layout() # Adjust layout
plt.show()
# ==============================

# PIE CHART
# Sales Distribution by Category
# Create pie chart
plt.figure(figsize=(8, 8))
plt.pie(sales, labels=categories, autopct='%1.1f%%')
plt.title('Sales Distribution by Category')
plt.axis('equal') # Keeps it circular
plt.show()
# ==============================

#print(df.columns.tolist())

# SALES BY STATE MAP
# Group sales by state/province
state_sales = df.groupby('State/Province')['Sales'].sum().reset_index()

# Create choropleth map
fig = px.choropleth(
    state_sales,
    locations='State/Province',
    locationmode='USA-states',
    color='Sales',
    scope='usa',
    color_continuous_scale='Blues',
    title='Sales by U.S. State'
)
fig.show()
# ==============================

# ==============================
# Save Clean Data
# ==============================

df.to_csv("data/cleaned_superstore_data.csv", index=False)
print(df.shape)