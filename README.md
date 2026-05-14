# 📊 Superstore Sales Dashboard Project

## 📌 Project Overview

This project focuses on transforming raw retail sales data into meaningful business insights through data analysis and an interactive dashboard.

We perform:
* Data cleaning and preparation (data wrangling)
* Exploratory Data Analysis (EDA)
* Interactive dashboard development using Plotly Dash + HTML export

The goal is to simulate a real-world data analyst workflow and support data-driven decision-making.

---

## 🌐 Live Dashboard

You can view the dashboard here (GitHub Pages):

👉 https://saleenaf.github.io/Superstore-Dashboard-Project/

The dashboard includes:
* Sales analysis by category
* Profit heatmap
* Time-based trend analysis
* Geographic sales distribution

> ⚠️ Note:
> The GitHub Pages version is a static HTML export of the dashboard.
> Interactive Dash-specific components such as the Year filter dropdown and KPI cards are only available when running the local Dash application (`dashboard.py`).

---

## 📂 Dataset

Dataset used: Superstore Sales Dataset (Kaggle)

It includes:
* Sales, Profit, Category, Region
* Order Dates (time-based analysis)
* Customer and product-level data

---

## ⚙️ Setup Instructions (IMPORTANT)

Follow these steps before running the project:

### 1. Clone the repository

git clone https://github.com/SaleenaF/Superstore-Dashboard-Project.git

If you don’t have Git installed, download it from https://git-scm.com  
Installing Git will also install Git Bash, which we will use in VS Code.

---

### 2. Open the project in VS Code

1. Open VS Code
2. Click File → Open Folder
3. Select the Superstore-Dashboard-Project folder you just cloned

---

### 3. Open the terminal (Git Bash)

1. Press Ctrl + ~ (tilde key)
2. Click the dropdown arrow in the terminal
3. Select Git Bash (instead of PowerShell or Command Prompt)

If you don’t have Python installed, download it from https://www.python.org/downloads/  
Make sure to check "Add Python to PATH" during installation.

---

### 4. Navigate to the project folder (if needed)

cd Superstore-Dashboard-Project

---

### 5. Install required libraries

pip install -r requirements.txt

If you get errors, try upgrading pip:

python -m pip install --upgrade pip

---

## 📁 Project Structure

Superstore-Dashboard-Project/
│
├── data/                  # Dataset files
├── visuals/               # Generated charts + dashboard HTML
├── docs/                  # GitHub Pages deployment folder
├── data_pipeline.py       # Data cleaning + feature engineering
├── dashboard.py           # Dash app + HTML export
├── requirements.txt       # Required libraries
└── README.md              # Project documentation

---

## 👥 Team Workflow (VERY IMPORTANT)

### ⚡ Git Quick Guide

### 🔁 Daily Workflow

# 1. Always start here
git pull origin main

# 2. Create your own branch (recommended)
git checkout -b feature-yourname

# 3. After coding
git add .
git commit -m "what you did"
git push origin feature-yourname

Then:
1. Go to GitHub repo
2. Click Compare & Pull Request
3. Click Create Pull Request
4. Click Merge

---

### ⚡ Fast Option (Small Fixes Only)

git pull origin main
git add .
git commit -m "small fix"
git push origin main

---

### ⚖️ When Can You Merge?

You can merge if:
* Your code runs without errors
* It doesn’t break someone else’s work
* The project still runs after your change

---

### 🚫 When NOT to Merge

* Your code is unfinished
* You changed large/shared files and aren’t sure
* You think it might break something

---

### 🧠 Project Rule

Big feature → use a branch + PR
Small safe fix → can push to main (but branches are safer)

---

### 🔥 Golden Rule

git pull origin main

Always do this before starting work.

---

### 🧠 Memory Trick

Pull → Branch → Work → Add → Commit → Push → PR → Merge

---

### ❓ If something breaks

git pull origin main

If you're stuck, ask the group before pushing.

---

## 📊 Project Tasks

### ✔️ Data Cleaning
* Handle missing values
* Fix data types
* Remove duplicates
* Create new features (Year, Month, Profit Margin)

---

### ✔️ EDA
* Sales by Category
* Profit by Region
* Monthly trends
* Descriptive statistics
* Visualizations (bar, line, pie, heatmap, box plot)

---

### ✔️ Dashboard (Final Step)

Built using Plotly Dash + HTML export for deployment.

Features:
* Interactive Year filter (including "All Years")
* Bar chart → Sales by Category
* Line chart → Monthly Sales Trend
* Pie chart → Sales Distribution
* Heatmap → Profit by Region and Category
* Choropleth map → Sales by U.S. State
* Box plot → Sales distribution and outliers

The dashboard is available in two formats:
* Dash app (local interactive version)
* Static HTML dashboard (GitHub Pages deployment)

---

## 📈 Key Insights (EDA Findings)

From the analysis:
* Technology and Office Supplies generate strong revenue
* Sales show seasonal monthly trends
* Certain regions outperform others in profit
* Outliers exist in sales distribution indicating high-value transactions

---

## 🚀 Goal

By completing this project, we aim to:
* Practice real-world data analysis workflows
* Build a professional dashboard project for portfolios
* Learn collaborative development using GitHub

---

## 💡 Technologies Used

* Python (Pandas, NumPy)
* Plotly (Express + Graph Objects)
* Dash (Interactive dashboard)
* Git & GitHub
* HTML (for deployment)

---

## 📌 How to Run

python data_pipeline.py

python dashboard.py
