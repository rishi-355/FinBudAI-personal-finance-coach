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
    st.session_state.income = 5000.0
if "rent" not in st.session_state:
    st.session_state.rent = 1500.0
if "food" not in st.session_state:
    st.session_state.food = 500.0
if "transport" not in st.session_state:
    st.session_state.transport = 300.0
if "entertainment" not in st.session_state:
    st.session_state.entertainment = 400.0
if "other" not in st.session_state:
    st.session_state.other = 300.0

# ----------------- STYLING (Modern Dark Theme - CRED / Jupiter Style) -----------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

        /* Global Theme Override */
        html, body, [class*="css"], .stApp {
            font-family: 'Outfit', sans-serif;
            background-color: #0D0F12 !important;
            color: #E2E8F0 !important;
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #12161A !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* Title styling */
        .brand-header {
            font-size: 2.2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #00E5FF 0%, #8A2BE2 50%, #FF007A 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0px;
        }
        
        .brand-subtitle {
            font-size: 0.95rem;
            color: #64748B;
            margin-top: 0px;
            margin-bottom: 1.5rem;
            font-weight: 400;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        /* Nav menu */
        .nav-item {
            padding: 10px 15px;
            border-radius: 8px;
            margin-bottom: 5px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        /* Style Streamlit forms and buttons */
        div.stButton > button {
            background: linear-gradient(135deg, #8A2BE2 0%, #4A0E4E 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s;
        }
        div.stButton > button:hover {
            box-shadow: 0 0 15px rgba(138, 43, 226, 0.5);
            transform: translateY(-1px);
        }
        
        /* Input fields styles */
        div[data-baseweb="input"] {
            background-color: #1A1F26 !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 8px !important;
        }
    </style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR BRANDING & ROUTING -----------------
st.sidebar.markdown('<div class="brand-header">FinBud</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="brand-subtitle">AI Finance Buddy</div>', unsafe_allow_html=True)

st.sidebar.subheader("Navigation")
menu_selection = st.sidebar.radio(
    label="Go to Page:",
    options=[
        "🏛️ Dashboard",
        "📈 Expense Analysis",
        "🎯 Savings Planner",
        "🤖 AI Coach (Preview)"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.subheader("👤 Financial Profile")

# Data Entry Inputs bound directly to session state
income = st.sidebar.number_input("Monthly Income (₹)", min_value=0.0, step=100.0, key="income")

st.sidebar.markdown("**Monthly Expenses:**")
rent = st.sidebar.number_input("Rent / Hostel (₹)", min_value=0.0, step=50.0, key="rent")
food = st.sidebar.number_input("Food (₹)", min_value=0.0, step=25.0, key="food")
transport = st.sidebar.number_input("Transport (₹)", min_value=0.0, step=10.0, key="transport")
entertainment = st.sidebar.number_input("Entertainment (₹)", min_value=0.0, step=25.0, key="entertainment")
other = st.sidebar.number_input("Other (₹)", min_value=0.0, step=20.0, key="other")

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
        expenses=expenses_dict
    )

elif menu_selection == "🤖 AI Coach (Preview)":
    render_ai_coach(
        income=income,
        expenses=expenses_dict,
        total_expenses=total_expenses,
        savings=savings,
        savings_rate=savings_rate,
        health_score=health_score,
        health_status=health_status
    )
