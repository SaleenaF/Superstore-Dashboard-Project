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
plotly_template = 'plotly_white'
main_color = 'skyblue'

# BAR CHART
# Get categories and values as separate lists
sales_by_category = df.groupby('Category')['Sales'].sum()

categories = sales_by_category.index.tolist()
sales = sales_by_category.values.tolist()

# Plotly Bar Chart with matplotlib-style labels/stats
bar_fig = px.bar(
    x=categories,
    y=sales,
    labels={'x': 'Category', 'y': 'Sales'},
    title='Sales by Category',
    text=sales,
    template=plotly_template
)

# Style bars similar to matplotlib version
bar_fig.update_traces(
    marker_color=main_color,
    marker_line_color='black',
    marker_line_width=1,
    texttemplate='$%{text:.2f}',
    textposition='outside'
)

bar_fig.update_layout(
    width=800,
    height=500
)

bar_fig.write_html("visuals/bar_chart.html")
bar_fig.show()
# ==============================

# HEATMAP
# Create pivot table for heatmap
heatmap_data = df.pivot_table(
    values='Profit',
    index='Region',
    columns='Category',
    aggfunc='sum'
)

# Create heatmap
heatmap_fig = px.imshow(
    heatmap_data,
    text_auto=True,
    color_continuous_scale='Blues',
    title='Profit by Region and Category',
    template=plotly_template
)

heatmap_fig.update_layout(
    width=800,
    height=500
)

heatmap_fig.write_html("visuals/heatmap_profit.html")
heatmap_fig.show()
# ==============================

# LINE CHART 2
# Group sales by month
monthly_sales = df.groupby(
    pd.Grouper(key='Order Date', freq='ME')
)['Sales'].sum().reset_index()

# Create Plotly line chart
line_fig2 = px.line(
    monthly_sales,
    x='Order Date',
    y='Sales',
    markers=True,
    title='Monthly Sales Trend',
    template=plotly_template
)

line_fig2.update_traces(
    line=dict(width=3, color=main_color),
    marker=dict(size=8, color=main_color)
)

line_fig2.update_layout(
    xaxis_title='Date',
    yaxis_title='Sales',
    width=1000,
    height=500
)

line_fig2.write_html("visuals/monthly_sales_trend.html")
line_fig2.show()
# ==============================

# PIE CHART
# Sales Distribution by Category
# Create pie chart
pie_fig = px.pie(
    names=categories,
    values=sales,
    title='Sales Distribution by Category',
    template=plotly_template,
    color_discrete_sequence=[main_color]
)

pie_fig.update_traces(textinfo='percent+label')

pie_fig.write_html("visuals/pie_chart.html")
pie_fig.show()
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
    title='Sales by U.S. State',
    template=plotly_template
)

fig.write_html("visuals/state_sales_map.html")
fig.show()
# ==============================

# BOXPLOT
# For sales
box_fig = px.box(
    df,
    y='Sales',
    title='Sales Values',
    template=plotly_template
)

box_fig.update_traces(
    marker_color=main_color,
    line_color=main_color
)

box_fig.write_html("visuals/boxplot_sales.html")
box_fig.show()

# ==============================
# Step 6: SAVE CLEAN DATA
# ==============================

df.to_csv("data/cleaned_superstore_data.csv", index=False)

print(df.shape)
print("All visualizations saved to visuals folder.")