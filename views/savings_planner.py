import streamlit as st
import plotly.graph_objects as go
from utils.calculations import (
    calculate_total_expenses,
    calculate_savings,
    calculate_savings_rate,
    calculate_financial_health_score
)

def render_savings_planner(income, expenses):
    st.markdown("### 🎯 Savings Planner & Simulator")
    
    if income <= 0:
        st.warning("Please set a monthly income in the sidebar to use the Savings Planner.")
        return

    # 1. Target Savings Selection
    st.subheader("1. Set Your Monthly Savings Goal")
    
    target_option = st.radio(
        "Choose a target savings rate:",
        ["20% (Recommended Baseline)", "30% (Wealth Builder)", "50% (FIRE Goal)", "Custom Goal"],
        horizontal=True
    )
    
    if target_option == "20% (Recommended Baseline)":
        target_pct = 20.0
    elif target_option == "30% (Wealth Builder)":
        target_pct = 30.0
    elif target_option == "50% (FIRE Goal)":
        target_pct = 50.0
    else:
        target_pct = st.slider("Custom Savings Goal (%)", min_value=0.0, max_value=90.0, value=25.0, step=1.0)
        
    target_amt = income * (target_pct / 100)
    
    # Calculate current values
    current_total_expenses = sum(expenses.values())
    current_savings = income - current_total_expenses
    current_savings_rate = (current_savings / income * 100) if income > 0 else 0
    
    st.markdown(
        f"To hit a **{target_pct:.0f}%** savings rate, you need to save **₹{target_amt:,.2f}** per month."
    )
    
    # Progress towards savings goal
    st.subheader("Goal Progress")
    
    # Check if savings are negative
    display_rate = max(0.0, current_savings_rate)
    progress_percentage = min(1.0, display_rate / target_pct) if target_pct > 0 else 1.0
    
    col_pct, col_bar = st.columns([1, 4])
    with col_pct:
        st.write(f"**Current Savings Rate:** {current_savings_rate:.1f}%")
    with col_bar:
        st.progress(progress_percentage)
        
    if current_savings_rate >= target_pct:
        st.success(f"🎉 Awesome! You are exceeding your target savings goal by {(current_savings_rate - target_pct):.1f}%!")
    else:
        gap_amt = target_amt - current_savings
        st.info(f"💡 You need to reduce expenses or increase income by **₹{gap_amt:,.2f}** to meet your target.")
        
    st.markdown("---")

    # 2. What-If Simulator
    st.subheader("2. What-If Budget Simulator 🎛️")
    st.markdown("Adjust the sliders below to simulate cutting expenses and see the impact on your savings rate instantly:")

    sim_rent = st.slider("Simulated Rent/Hostel (₹)", min_value=0.0, max_value=float(max(rent := expenses.get("Rent/Hostel", 0.0), 1.0)*1.5), value=float(rent), step=10.0)
    sim_food = st.slider("Simulated Food (₹)", min_value=0.0, max_value=float(max(food := expenses.get("Food", 0.0), 1.0)*2.0), value=float(food), step=10.0)
    sim_transport = st.slider("Simulated Transport (₹)", min_value=0.0, max_value=float(max(transport := expenses.get("Transport", 0.0), 1.0)*2.0), value=float(transport), step=10.0)
    sim_entertainment = st.slider("Simulated Entertainment (₹)", min_value=0.0, max_value=float(max(entertainment := expenses.get("Entertainment", 0.0), 1.0)*2.5), value=float(entertainment), step=10.0)
    sim_other = st.slider("Simulated Other (₹)", min_value=0.0, max_value=float(max(other := expenses.get("Other", 0.0), 1.0)*2.5), value=float(other), step=10.0)

    # Re-calculate based on simulation
    sim_total_expenses = calculate_total_expenses(sim_rent, sim_food, sim_transport, sim_entertainment, sim_other)
    sim_savings = calculate_savings(income, sim_total_expenses)
    sim_savings_rate = calculate_savings_rate(income, sim_savings)
    sim_health_score, sim_health_status = calculate_financial_health_score(income, sim_rent, sim_entertainment, sim_other, sim_savings_rate)

    st.markdown("#### 📊 Simulation Results")
    
    col_sim1, col_sim2, col_sim3 = st.columns(3)
    
    with col_sim1:
        st.metric(
            label="Simulated Total Expenses",
            value=f"₹{sim_total_expenses:,.2f}",
            delta=f"₹{sim_total_expenses - current_total_expenses:,.2f}",
            delta_color="inverse"
        )
    with col_sim2:
        st.metric(
            label="Simulated Savings Rate",
            value=f"{sim_savings_rate:.1f}%",
            delta=f"{sim_savings_rate - current_savings_rate:.1f}%"
        )
    with col_sim3:
        st.metric(
            label="Simulated Health Score",
            value=f"{sim_health_score} / 100",
            delta=int(sim_health_score - health_score)
        )

    # Call-to-action message
    savings_diff = sim_savings - current_savings
    if savings_diff > 0:
        st.markdown(
            f"""
            <div style="
                background-color: rgba(0, 230, 118, 0.08);
                border: 1px solid rgba(0, 230, 118, 0.2);
                padding: 1rem;
                border-radius: 8px;
                margin-top: 1rem;
            ">
                🚀 By implementing these budget changes, you will save an extra <strong>₹{savings_diff:,.2f}</strong> per month!
            </div>
            """,
            unsafe_allow_html=True
        )
