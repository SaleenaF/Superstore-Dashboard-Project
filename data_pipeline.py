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
os.makedirs("visuals", exist_ok=True)

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

# Basic Statistics
print(df['Sales'].describe())
print(df['Profit'].describe())

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

# Universal Plotly Style
col1 = 'plotly_white'
col2 = 'skyblue'

# BAR CHART
# Get categories and values as separate lists
sales_by_category = df.groupby('Category')['Sales'].sum()

categories = sales_by_category.index.tolist()
sales = sales_by_category.values.tolist()

barChart = px.bar(
    x=categories, y=sales,
    labels={'x': 'Category', 'y': 'Sales'},
    title='Sales by Category',
    text=sales,
    template=col1,
    color_discrete_sequence=[col2]
)

barChart.update_traces(textposition='outside') # Make info sit on top of bars
barChart.write_html("visuals/bar_chart.html")
barChart.show()
# ==============================

# HEATMAP
# Create pivot table for heatmap
heat = df.pivot_table(values='Profit', index='Region', columns='Category', aggfunc='sum')

heatMap = px.imshow(
    heat,
    text_auto=True,
    color_continuous_scale='Blues',
    title='Profit by Region and Category',
    template=col1
)

heatMap.write_html("visuals/heatmap.html")
heatMap.show()
# ==============================

# LINE CHART
monthly_sales = df.groupby(pd.Grouper(key='Order Date', freq='ME'))['Sales'].sum().reset_index()

lineChart = px.line(
    monthly_sales,
    x='Order Date',
    y='Sales',
    markers=True,
    title='Monthly Sales Trend',
    template=col1,
    color_discrete_sequence=[col2]
)

lineChart.write_html("visuals/line_chart.html")
lineChart.show()
# ==============================

# PIE CHART
pieChart = px.pie(
    names=categories,
    values=sales,
    title='Sales Distribution by Category',
    template=col1,
    color_discrete_sequence=[col2]
)

pieChart.write_html("visuals/pie_chart.html")
pieChart.show()
# ==============================

# SALES BY STATE MAP
state_sales = df.groupby('State/Province')['Sales'].sum().reset_index()

fig = px.choropleth(
    state_sales,
    locations='State/Province',
    locationmode='USA-states',
    color='Sales',
    scope='usa',
    color_continuous_scale='Blues',
    title='Sales by U.S. State',
    template=col1
)

fig.write_html("visuals/choropleth_map.html")
fig.show()
# ==============================

# BOXPLOT
boxPlot = px.box(
    df,
    y='Sales',
    title='Sales Values',
    template=col1,
    color_discrete_sequence=[col2]
)

boxPlot.write_html("visuals/boxplot.html")
boxPlot.show()
# ==============================

# ==============================
# Step 6: SAVE CLEAN DATA
# ==============================

df.to_csv("data/cleaned_superstore_data.csv", index=False)

print(df.shape)
print("All visualizations saved to visuals folder.")