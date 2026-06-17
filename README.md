# FinBud – AI Personal Finance Coach 💰🤖

## Overview

FinBud is an AI-powered personal finance management platform designed to help users track expenses, analyze spending habits, improve savings, and receive personalized financial recommendations using Google Gemini AI.

Built with Python, Streamlit, Plotly, and Gemini AI, FinBud provides an interactive dashboard that transforms financial data into actionable insights.

---

## Features

### 📊 Financial Dashboard

* Monthly Income Tracking
* Expense Monitoring
* Net Savings Calculation
* Savings Rate Analysis
* Financial Health Score

### 📈 Expense Analysis

* Interactive Expense Breakdown
* Category-wise Spending Insights
* Expense Distribution Charts
* Spending Pattern Visualization

### 🎯 Savings Planner

* Savings Goal Tracking
* What-If Budget Simulator
* Financial Scenario Planning
* Goal Achievement Recommendations

### 🤖 AI Financial Coach

Powered by Google Gemini AI.

Generate:

* Spending Analysis
* Savings Recommendations
* Financial Health Assessment
* Budget Optimization Suggestions

### 🎨 Modern FinTech UI

* Dark FinTech Theme
* Interactive Charts
* Responsive Layout
* Modern Dashboard Cards

---

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI

* Google Gemini API

### Data Visualization

* Plotly
* Pandas

### Version Control

* Git
* GitHub

---

## Project Structure

```text
FinBudAI/
│
├── .streamlit/
│
├── utils/
│   ├── calculations.py
│   └── gemini_service.py
│
├── views/
│   ├── dashboard.py
│   ├── expense_analysis.py
│   ├── savings_planner.py
│   └── ai_coach.py
│
├── assets/
│   ├── dashboard.png
│   ├── expense-analysis.png
│   ├── savings-planner.png
│   └── ai-coach.png
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Screenshots

### Dashboard

![Dashboard](assets/dashboard.png)

### Expense Analysis

![Expense Analysis](assets/expense-analysis.png)

### Savings Planner

![Savings Planner](assets/savings-planner.png)

### AI Financial Coach

![AI Coach](assets/ai-coach.png)

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd FinBudAI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create:

```text
.streamlit/secrets.toml
```

Add:

```toml
GEMINI_API_KEY = "YOUR_API_KEY"
```

Run:

```bash
streamlit run app.py
```

---

## Resume Description

Developed an AI-powered personal finance platform using Python, Streamlit, Plotly, and Google Gemini API. Implemented expense tracking, savings analysis, financial health scoring, interactive financial dashboards, and personalized AI-generated financial recommendations through a modular multi-page architecture.

---

## Future Enhancements

* User Authentication
* Cloud Database Integration
* PDF Financial Reports
* Investment Recommendations
* Expense History Tracking
* Mobile Application Version

---

### FinBud

**Smart Money. Smarter Decisions.**
