import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import calculations
from utils.calculations import (
    calculate_total_expenses,
    calculate_savings,
    calculate_savings_rate,
    calculate_financial_health_score,
)

# Import views
from views.dashboard import render_dashboard
from views.expense_analysis import render_expense_analysis
from views.savings_planner import render_savings_planner
from views.ai_coach import render_ai_coach

# Page configuration
st.set_page_config(
    page_title="FinBud - AI Personal Finance Coach",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State values for inputs if they do not exist
if "income" not in st.session_state:
    st.session_state.income = 50000.0
if "rent" not in st.session_state:
    st.session_state.rent = 15000.0
if "food" not in st.session_state:
    st.session_state.food = 8000.0
if "transport" not in st.session_state:
    st.session_state.transport = 3000.0
if "entertainment" not in st.session_state:
    st.session_state.entertainment = 5000.0
if "other" not in st.session_state:
    st.session_state.other = 4000.0

# ----------------- STYLING (Modern Dark Fintech - CRED / Jupiter Style) -----------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

        /* Global overrides */
        html, body, [class*="css"], .stApp {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            background-color: #080A0F !important;
            color: #F8FAFC !important;
        }

        /* Sidebar container styling */
        [data-testid="stSidebar"] {
            background-color: #0D111A !important;
            border-right: 1px solid rgba(255, 255, 255, 0.03);
            padding: 1.5rem 1rem;
        }

        /* Branding logo in sidebar */
        .sidebar-logo {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 800;
            font-size: 2.2rem;
            background: linear-gradient(135deg, #00E5FF 0%, #8A2BE2 50%, #FF007A 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -1.5px;
            margin-bottom: 0px;
        }
        
        .sidebar-tagline {
            font-size: 0.75rem;
            color: #64748B;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 2.5px;
            margin-top: 0px;
            margin-bottom: 2rem;
        }

        /* Style labels in inputs */
        label {
            font-weight: 500 !important;
            color: #94A3B8 !important;
            font-size: 0.85rem !important;
        }

        /* Input box overrides */
        div[data-baseweb="input"] {
            background-color: #121824 !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 10px !important;
            color: #F8FAFC !important;
            transition: all 0.3s ease;
        }
        div[data-baseweb="input"]:focus-within {
            border-color: #00E5FF !important;
            box-shadow: 0 0 10px rgba(0, 229, 255, 0.15) !important;
        }

        /* Streamlit primary buttons */
        div.stButton > button {
            background: linear-gradient(135deg, #8A2BE2 0%, #00E5FF 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.6rem 1.8rem !important;
            font-weight: 600 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            letter-spacing: 0.5px !important;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
            box-shadow: 0 4px 15px rgba(138, 43, 226, 0.25) !important;
        }
        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(0, 229, 255, 0.4) !important;
        }
        div.stButton > button:active {
            transform: translateY(0px) !important;
        }
            /* ===== SIDEBAR NAVIGATION COLORS ===== */

/* Navigation heading */
[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* Radio button text */
[data-testid="stSidebar"] .stRadio label {
    color: #E2E8F0 !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
}

/* Sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: #E2E8F0;
}

/* Financial Profile heading */
[data-testid="stSidebar"] h2 {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* Input labels */
[data-testid="stSidebar"] label {
    color: #CBD5E1 !important;
}

/* Hover effect */
[data-testid="stSidebar"] .stRadio label:hover {
    color: #00E5FF !important;
}

        /* Hide default Streamlit visual headers */
        #MainMenu, header, footer {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR BRANDING & ROUTING -----------------
st.sidebar.markdown('<div class="sidebar-logo">FinBud</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-tagline">AI Wealth Coach</div>', unsafe_allow_html=True)

st.sidebar.subheader("Navigation")
menu_selection = st.sidebar.radio(
    label="Go to Page:",
    options=[
        "🏛️ Dashboard",
        "📈 Expense Analysis",
        "🎯 Savings Planner",
        "🤖 AI Coach (Gemini)"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.subheader("👤 Financial Profile")

# Data Entry Inputs bound directly to session state
income = st.sidebar.number_input("Monthly Income (₹)", min_value=0.0, step=1000.0, key="income")

st.sidebar.markdown("**Monthly Expenses:**")
rent = st.sidebar.number_input("Rent / Hostel (₹)", min_value=0.0, step=500.0, key="rent")
food = st.sidebar.number_input("Food (₹)", min_value=0.0, step=500.0, key="food")
transport = st.sidebar.number_input("Transport (₹)", min_value=0.0, step=200.0, key="transport")
entertainment = st.sidebar.number_input("Entertainment (₹)", min_value=0.0, step=500.0, key="entertainment")
other = st.sidebar.number_input("Other (₹)", min_value=0.0, step=500.0, key="other")

# ----------------- CENTRAL CALCULATIONS -----------------
expenses_dict = {
    "Rent/Hostel": rent,
    "Food": food,
    "Transport": transport,
    "Entertainment": entertainment,
    "Other": other
}

total_expenses = calculate_total_expenses(rent, food, transport, entertainment, other)
savings = calculate_savings(income, total_expenses)
savings_rate = calculate_savings_rate(income, savings)
health_score, health_status = calculate_financial_health_score(income, rent, entertainment, other, savings_rate)

# ----------------- ROUTING TO ACTIVE VIEW -----------------
if menu_selection == "🏛️ Dashboard":
    render_dashboard(
        income=income,
        expenses=expenses_dict,
        total_expenses=total_expenses,
        savings=savings,
        savings_rate=savings_rate,
        health_score=health_score,
        health_status=health_status
    )

elif menu_selection == "📈 Expense Analysis":
    render_expense_analysis(
        income=income,
        expenses=expenses_dict,
        total_expenses=total_expenses
    )

elif menu_selection == "🎯 Savings Planner":
    render_savings_planner(
        income=income,
        expenses=expenses_dict,
        health_score=health_score
    )

elif menu_selection == "🤖 AI Coach (Gemini)":
    render_ai_coach(
        income=income,
        expenses=expenses_dict,
        total_expenses=total_expenses,
        savings=savings,
        savings_rate=savings_rate,
        health_score=health_score,
        health_status=health_status
    )
