# FinBud - AI Personal Finance Coach 💰

FinBud is a premium, modern, and interactive Streamlit web application designed to help users track their personal finances and assess their overall financial health.

## 🚀 Features

*   **Financial Profile Input**: Set monthly income and detailed expense breakdown (Rent/Hostel, Food, Transport, Entertainment, Other).
*   **Key Financial Metrics**:
    *   Monthly Income
    *   Total Expenses
    *   Net Savings (dynamically color-coded based on positive/negative balances)
    *   Financial Health Score (0 - 100) with a performance-based rating
*   **Interactive Visualizations**:
    *   **Expense Breakdown**: An interactive donut/pie chart showing how your spending is distributed.
    *   **Financial Health Meter**: A gauge indicator highlighting your rating zone (Needs Attention, Fair, Good, Excellent).
*   **Actionable Insights**: Instant, contextual recommendations based on key personal finance benchmarks (e.g., target 20% savings rate, housing cost limits, discretionary spend tracking).

---

## 🛠️ Setup & Installation

### 1. Prerequisites
Make sure you have **Python 3.8+** installed.

### 2. Install Dependencies
Navigate to the project directory and install the required packages:

```bash
pip install -r requirements.txt
```

### 3. Run the App
Launch the Streamlit server:

```bash
streamlit run app.py
```

The app will open automatically in your browser. If it doesn't, navigate to the local URL shown in your console (usually `http://localhost:8501`).

---

## 📂 Project Structure

```text
FinBudAI/
│
├── utils/
│   └── calculations.py  # Core financial algorithms and health scoring
│
├── app.py               # Main UI and dashboard setup
├── requirements.txt     # Python dependencies
└── README.md            # Project overview and setup instructions
```
