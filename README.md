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
```
If you don’t have Git installed, download it from the [Git](https://git-scm.com) website.  
Installing Git will also install **Git Bash**, which we will use in VS Code.

---

### 2. Open the project in VS Code

1. Open VS Code  
2. Click **File → Open Folder**  
3. Select the **Superstore-Dashboard-Project** folder you just cloned  

---

### 3. Open the terminal (Git Bash)

1. Press **Ctrl + ~** (tilde key)  
2. Click the **dropdown arrow** in the terminal  
3. Select **Git Bash** (instead of PowerShell or Command Prompt)  

If you don’t have Python installed, download it from the [Python](https://www.python.org/downloads/) website.  
Make sure to check **"Add Python to PATH"** during installation.

---

### 4. Navigate to the project folder (if needed)

```bash
cd Superstore-Dashboard-Project
```

---

### 5. Install required libraries

```bash
pip install -r requirements.txt
```
If you get errors, try upgrading pip:

```bash
python -m pip install --upgrade pip
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

### ⚡ Git Quick Guide (READ THIS FIRST)

### 🔁 Daily Workflow

```bash
# 1. Always start here
git pull origin main

# 2. Create your own branch (recommended)
git checkout -b feature-yourname

# 3. After coding
git add .
git commit -m "what you did"
git push origin feature-yourname
```

👉 Then:

1. Go to the GitHub repo  
2. Click **Compare & Pull Request**  
3. Click **Create Pull Request**  
4. Click **Merge**

---

### ⚡ Fast Option (Small Fixes Only)

```bash
git pull origin main
git add .
git commit -m "small fix"
git push origin main
```

👉 Only use this for very small, safe changes (like typos)

---

### ⚖️ When Can You Merge?

You can merge if:

* Your code runs **without errors**
* It doesn’t break someone else’s work
* The project still runs after your change

💡 Simple rule:  
> If someone pulls your code and their project still works, you're good

---

### 🚫 When NOT to Merge

* Your code is unfinished  
* You changed large/shared files and aren’t sure  
* You think it *might* break something  

---

### 🧠 Project Rule (IMPORTANT)

> Big feature → use a branch + PR  
> Small safe fix → you *can* push to main (but branches are safer)

---

### 🔥 Golden Rule

```bash
git pull origin main
```

Always do this before starting work.

---

### 🧠 Memory Trick

> Pull → Branch → Work → Add → Commit → Push → PR → Merge

---

### ❓ If something breaks

Run:

```bash
git pull origin main
```

If you're stuck, ask the group before pushing.

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
* Always use branches when possible  
* Keep commits clear and meaningful  

---

## 📌 How to Run (after setup)

```bash
python data_pipeline.py
```

(Dashboard will be added later)
