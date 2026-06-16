import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.calculations import (
    calculate_total_expenses,
    calculate_savings,
    calculate_savings_rate,
    calculate_financial_health_score,
)

# Page configuration
st.set_page_config(
    page_title="FinBud - AI Personal Finance Coach",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium UI styling
st.markdown("""
    <style>
        /* General styling */
        .main-header {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            background: linear-gradient(90deg, #12c2e9, #c471ed, #f64f59);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            margin-bottom: 0px;
            padding-bottom: 0px;
        }
        .subtitle {
            font-family: 'Outfit', sans-serif;
            color: #8892b0;
            font-size: 1.25rem;
            margin-top: 0px;
            margin-bottom: 2rem;
            font-weight: 300;
        }
        /* Metric container styling */
        .metric-container {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s ease-in-out;
        }
        .metric-container:hover {
            transform: translateY(-3px);
            border-color: rgba(255, 255, 255, 0.2);
            box-shadow: 0 10px 15px rgba(0,0,0,0.2);
        }
        .metric-label {
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.1rem;
            color: #8892b0;
            margin-bottom: 0.5rem;
        }
        .metric-val {
            font-size: 2rem;
            font-weight: 700;
            color: #ffffff;
        }
        /* Custom alerts / notes styling */
        .insight-card {
            background: linear-gradient(135deg, rgba(31, 38, 135, 0.1) 0%, rgba(255, 255, 255, 0.03) 100%);
            border-left: 5px solid #c471ed;
            border-radius: 0 8px 8px 0;
            padding: 1.25rem;
            margin-top: 1rem;
        }
        /* Light mode fallback adjustments */
        @media (prefers-color-scheme: light) {
            .metric-container {
                background-color: rgba(0, 0, 0, 0.02);
                border: 1px solid rgba(0, 0, 0, 0.08);
            }
            .metric-val {
                color: #212529;
            }
            .metric-container:hover {
                border-color: rgba(0, 0, 0, 0.15);
            }
            .insight-card {
                background: linear-gradient(135deg, rgba(31, 38, 135, 0.03) 0%, rgba(0, 0, 0, 0.01) 100%);
            }
        }
    </style>
""", unsafe_allow_html=True)

# Application Header
st.markdown('<h1 class="main-header">FinBud</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your AI Finance Buddy 🚀</p>', unsafe_allow_html=True)

# ----------------- SIDEBAR: INPUTS -----------------
st.sidebar.header("📊 Financial Profile")
st.sidebar.markdown("Enter your monthly income and expenses below:")

# Income Input
income = st.sidebar.number_input(
    "Monthly Income ($)",
    min_value=0.0,
    value=5000.0,
    step=100.0,
    help="Enter your total monthly take-home income."
)

st.sidebar.subheader("💸 Monthly Expenses")

# Expense Inputs
rent = st.sidebar.number_input(
    "Rent / Hostel ($)",
    min_value=0.0,
    value=1500.0,
    step=50.0,
    help="Rent, mortgage, or hostel fees."
)

food = st.sidebar.number_input(
    "Food ($)",
    min_value=0.0,
    value=500.0,
    step=25.0,
    help="Groceries, dining out, and delivery."
)

transport = st.sidebar.number_input(
    "Transport ($)",
    min_value=0.0,
    value=300.0,
    step=10.0,
    help="Public transit, fuel, vehicle insurance, etc."
)

entertainment = st.sidebar.number_input(
    "Entertainment ($)",
    min_value=0.0,
    value=400.0,
    step=25.0,
    help="Movies, concerts, streaming services, hobbies."
)

other = st.sidebar.number_input(
    "Other ($)",
    min_value=0.0,
    value=300.0,
    step=20.0,
    help="Miscellaneous or unexpected expenses."
)

# ----------------- CALCULATIONS -----------------
total_expenses = calculate_total_expenses(rent, food, transport, entertainment, other)
savings = calculate_savings(income, total_expenses)
savings_rate = calculate_savings_rate(income, savings)
health_score, health_status = calculate_financial_health_score(income, rent, entertainment, other, savings_rate)

# ----------------- MAIN AREA: DASHBOARD -----------------

# 1. METRICS GRID
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-label">Monthly Income</div>
            <div class="metric-val">${income:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-label">Total Expenses</div>
            <div class="metric-val" style="color: #ff6b6b;">${total_expenses:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    # Color savings based on positive/negative
    savings_color = "#2ecc71" if savings >= 0 else "#e74c3c"
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-label">Net Savings</div>
            <div class="metric-val" style="color: {savings_color};">${savings:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    # Color score based on classification
    if health_score >= 80:
        score_color = "#2ecc71"  # Green
    elif health_score >= 60:
        score_color = "#f1c40f"  # Yellow/Gold
    elif health_score >= 40:
        score_color = "#e67e22"  # Orange
    else:
        score_color = "#e74c3c"  # Red
        
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-label">Health Score</div>
            <div class="metric-val" style="color: {score_color};">{health_score} / 100</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# 2. VISUALIZATIONS SECTION
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🍰 Expense Breakdown")
    if total_expenses > 0:
        expense_data = {
            "Category": ["Rent/Hostel", "Food", "Transport", "Entertainment", "Other"],
            "Amount": [rent, food, transport, entertainment, other]
        }
        df = pd.DataFrame(expense_data)
        
        # Filtering categories with 0 values to keep the chart clean
        df_filtered = df[df["Amount"] > 0]
        
        if not df_filtered.empty:
            fig = px.pie(
                df_filtered,
                names="Category",
                values="Amount",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#8892b0")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No expenses entered yet.")
    else:
        st.info("All expenses are $0.00.")

with col_right:
    st.subheader("🩺 Financial Health Meter")
    
    # Financial Health Gauge chart
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=health_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Status: {health_status}", 'font': {'size': 18, 'color': "#8892b0"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#8892b0"},
            'bar': {'color': "#c471ed"},
            'bgcolor': "rgba(255,255,255,0.05)",
            'borderwidth': 2,
            'bordercolor': "rgba(255,255,255,0.1)",
            'steps': [
                {'range': [0, 40], 'color': 'rgba(231, 76, 60, 0.2)'},
                {'range': [40, 60], 'color': 'rgba(230, 126, 34, 0.2)'},
                {'range': [60, 80], 'color': 'rgba(241, 196, 15, 0.2)'},
                {'range': [80, 100], 'color': 'rgba(46, 204, 113, 0.2)'}
            ],
        }
    ))
    
    fig_gauge.update_layout(
        margin=dict(t=40, b=10, l=30, r=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#8892b0", family="Outfit")
    )
    
    st.plotly_chart(fig_gauge, use_container_width=True)

# 3. COACH'S INSIGHTS (Static recommendations preparing for AI integration)
st.markdown("### 💬 Coach's Insights")

insights = []

# Savings Rate Insights
if savings_rate <= 0:
    insights.append(
        "🚨 **Red Alert (Savings Rate: Negative):** You are spending more than your monthly income. "
        "Review your discretionary categories immediately to find savings opportunities."
    )
elif savings_rate < 20.0:
    insights.append(
        f"⚠️ **Target Savings Rate (Current: {savings_rate:.1f}%):** The standard rule of thumb is to save "
        "at least 20% of your income. Consider looking at your Entertainment or Other expenses to scale back."
    )
else:
    insights.append(
        f"🌟 **Excellent Savings Rate (Current: {savings_rate:.1f}%):** You are successfully saving a healthy portion "
        "of your income! Keep this up to supercharge your financial goals."
    )

# Rent Ratio Insights
rent_ratio = (rent / income) * 100 if income > 0 else 0
if rent_ratio > 35.0:
    insights.append(
        f"🏠 **Housing Cost Warning:** Rent represents **{rent_ratio:.1f}%** of your total income. "
        "Standard financial planning advice suggests keeping housing expenses under 30% of income."
    )

# Discretionary Spend Insights
discretionary_spend = entertainment + other
disc_ratio = (discretionary_spend / income) * 100 if income > 0 else 0
if disc_ratio > 30.0:
    insights.append(
        f"🎟️ **Discretionary Spending Warning:** Entertainment and Other expenses consume **{disc_ratio:.1f}%** of your income. "
        "Consider creating a monthly limit for these areas to free up cash flow."
    )

# Health Score Insights
if health_score >= 80:
    insights.append(
        "🏆 **FinBud's Verdict:** Your financial health score is excellent! You have balanced your fixed costs, "
        "discretionary spending, and savings rate remarkably well. Bravo!"
    )
elif health_score >= 60:
    insights.append(
        "👍 **FinBud's Verdict:** Your financial health is in the good zone. With a few minor adjustments, "
        "you can reach the top tier. Look for small adjustments to savings or entertainment."
    )
else:
    insights.append(
        "💡 **FinBud's Verdict:** There are significant areas for improvement. Focus on reducing variable "
        "costs and setting aside even a tiny percentage of savings each month."
    )

# Render insights beautifully
for insight in insights:
    st.markdown(f'<div class="insight-card">{insight}</div>', unsafe_allow_html=True)
