# 📊 Superstore Sales Dashboard Project

## 📌 Project Overview

This project focuses on transforming raw retail sales data into meaningful business insights through data analysis and an interactive dashboard.

We perform:

* Data cleaning and preparation (data wrangling)  
* Exploratory Data Analysis (EDA)  
* Interactive dashboard development using Plotly Dash  

---

## 📂 Dataset

Dataset used: **Superstore Sales Dataset (Kaggle)**

Includes:

* Sales, Profit, Category, Region  
* Order Dates  
* Customer & product data  

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/SaleenaF/Superstore-Dashboard-Project.git
cd Superstore-Dashboard-Project
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
Superstore-Dashboard-Project/
├── data/
├── data_pipeline.py
├── dashboard.py
├── requirements.txt
└── README.md
```

---

## 👥 Team Workflow

## ⚡ Git Quick Guide

### 🔁 Main Workflow (USE THIS)

```bash
git pull origin main
git checkout -b feature-yourname

# after coding
git add .
git commit -m "what you did"
git push origin feature-yourname
```

👉 Then create a **Pull Request** on GitHub and merge

---

### ⚡ Quick Fix (ONLY small changes)

```bash
git pull origin main
git add .
git commit -m "small fix"
git push origin main
```

---

### ⚖️ When to Merge

✅ Merge if:
* Code runs without errors  
* Project still works after your change  

❌ Don’t merge if:
* Work is unfinished  
* You changed major/shared code  

---

### 🧠 Rule

> Big change → branch + PR  
> Small fix → push to main  

---

### 🔥 Golden Rule

```bash
git pull origin main
```

---

### 🧠 Shortcut to Remember

> Pull → Branch → Work → Push → Merge

---

## 📊 Project Tasks

### ✔️ Data Cleaning
* Missing values, types, duplicates  
* Create features (Year, Month)

### ✔️ EDA
* Sales by Category  
* Profit by Region  
* Monthly trends  

### ✔️ Dashboard
* Filters (Year, Category)  
* Charts: bar, line, pie, box  

---

## 🚀 Goal

* Practice real-world data workflows  
* Build a portfolio project  
* Learn Git collaboration  

---

## 📌 Run Project

```bash
python data_pipeline.py
```