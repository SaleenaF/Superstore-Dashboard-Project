# 📊 Superstore Sales Dashboard Project

## 📌 Project Overview

This project focuses on transforming raw retail sales data into meaningful business insights through data analysis and an interactive dashboard.

We perform:

* Data cleaning and preparation (data wrangling)  
* Exploratory Data Analysis (EDA)  
* Interactive dashboard development using Plotly Dash  

The goal is to simulate a real-world data analyst workflow and support data-driven decision-making.

---

## 📂 Dataset

Dataset used: **Superstore Sales Dataset (Kaggle)**

It includes:

* Sales, Profit, Category, Region  
* Order Dates (time-based analysis)  
* Customer and product-level data  

---

## ⚙️ Setup Instructions (IMPORTANT)

Follow these steps before running the project:

### 1. Clone the repository

```bash
git clone https://github.com/SaleenaF/Superstore-Dashboard-Project.git
cd Superstore-Dashboard-Project
```

### 2. Install required libraries

```bash
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
Superstore-Dashboard-Project/
│
├── data/                  # Dataset files
├── data_pipeline.py       # Data cleaning + analysis
├── dashboard.py           # Interactive dashboard (to be built)
├── requirements.txt       # Required libraries
└── README.md              # Project documentation
```

---

## 👥 Team Workflow (VERY IMPORTANT)

### 🔹 Before starting work:

Always pull the latest changes:

```bash
git pull origin main
```

### 🔹 Create your own branch:

```bash
git checkout -b feature-yourname
```

Example:

```bash
git checkout -b feature-dashboard
```

### 🔹 After making changes:

```bash
git add .
git commit -m "Describe your changes"
git push origin feature-yourname
```

### 🔹 Submit a Pull Request (PR)

* Go to GitHub  
* Click **Compare & Pull Request**  
* Request review before merging  

---

## 📊 Project Tasks

### ✔️ Data Cleaning

* Handle missing values  
* Fix data types  
* Remove duplicates  
* Create new features (Year, Month, etc.)  

### ✔️ EDA

* Sales by Category  
* Profit by Region  
* Monthly trends  
* Data visualizations (bar, line, pie, box)  

### ✔️ Dashboard (Final Step)

* Interactive filters (Year, Category)  
* Multiple charts:  
  * Bar chart  
  * Line chart  
  * Pie chart  
  * Box plot  
* Clean layout with clear titles  

---

## 🚀 Goal

By completing this project, we aim to:

* Practice real-world data analysis workflows  
* Build a professional dashboard project for portfolios  
* Learn collaborative development using GitHub  

---

## 💡 Notes

* Do NOT overwrite others’ work  
* Always use branches  
* Keep commits clear and meaningful  

---

## 📌 How to Run (after setup)

```bash
python data_pipeline.py
```

(Dashboard will be added later)