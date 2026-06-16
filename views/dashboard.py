import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def render_dashboard(income, expenses, total_expenses, savings, savings_rate, health_score, health_status):
    # Custom dashboard card component helper
    def render_metric_card(label, val_str, desc, border_color, val_color="#ffffff"):
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, rgba(20, 24, 33, 0.8) 0%, rgba(10, 12, 16, 0.8) 100%);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-top: 3px solid {border_color};
                padding: 1.5rem;
                border-radius: 12px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.3);
                text-align: left;
                margin-bottom: 1rem;
                transition: transform 0.2s ease-in-out;
            ">
                <div style="font-size: 0.8rem; text-transform: uppercase; color: #8892b0; letter-spacing: 1px; font-weight: 600;">{label}</div>
                <div style="font-size: 2rem; font-weight: 700; margin: 0.4rem 0; color: {val_color};">{val_str}</div>
                <div style="font-size: 0.8rem; color: #64ffda;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### 🏛️ Financial Overview")
    
    # 1. Dashboard Cards Row
    col1, col2, col3, col4 = st.columns(4)
    
    # Custom colors for accents
    primary_blue = "#00E5FF"
    neon_red = "#ff6b6b"
    emerald_green = "#00E676"
    electric_purple = "#8A2BE2"
    
    with col1:
        render_metric_card("Monthly Income", f"₹{income:,.2f}", "Total cash inflows", primary_blue)
        
    with col2:
        render_metric_card("Total Expenses", f"₹{total_expenses:,.2f}", f"{(total_expenses/income*100) if income > 0 else 0:.1f}% of income spent", neon_red, val_color="#ff6b6b")
        
    with col3:
        savings_lbl = "Net Savings"
        savings_desc = f"{savings_rate:.1f}% savings rate"
        savings_val_color = emerald_green if savings >= 0 else neon_red
        render_metric_card(savings_lbl, f"₹{savings:,.2f}", savings_desc, emerald_green, val_color=savings_val_color)
        
    with col4:
        health_colors = {
            "Excellent": emerald_green,
            "Good": "#f1c40f",
            "Fair": "#e67e22",
            "Needs Attention": neon_red
        }
        score_color = health_colors.get(health_status, electric_purple)
        render_metric_card("Health Score", f"{health_score} / 100", f"Status: {health_status}", score_color, val_color=score_color)

    st.markdown("---")

    # 2. Main Dashboard grid (Gauge on left, Savings summary on right)
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("#### 🩺 Health Gauge")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=health_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#8892b0"},
                'bar': {'color': electric_purple},
                'bgcolor': "rgba(255,255,255,0.02)",
                'borderwidth': 1,
                'bordercolor': "rgba(255,255,255,0.1)",
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(255, 107, 107, 0.15)'},
                    {'range': [40, 60], 'color': 'rgba(230, 126, 34, 0.15)'},
                    {'range': [60, 80], 'color': 'rgba(241, 196, 15, 0.15)'},
                    {'range': [80, 100], 'color': 'rgba(0, 230, 118, 0.15)'}
                ],
            }
        ))
        fig_gauge.update_layout(
            margin=dict(t=30, b=10, l=30, r=30),
            height=250,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8892b0", family="Outfit")
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_right:
        st.markdown("#### 📝 Monthly Savings Summary")
        
        # Build a neat pandas table for visual display
        summary_items = {
            "Item": ["Income", "Fixed Costs (Rent)", "Living Expenses (Food, Transport)", "Discretionary (Entertainment, Other)", "Net Savings"],
            "Amount (₹)": [
                income,
                expenses.get("Rent/Hostel", 0.0),
                expenses.get("Food", 0.0) + expenses.get("Transport", 0.0),
                expenses.get("Entertainment", 0.0) + expenses.get("Other", 0.0),
                savings
            ]
        }
        df_summary = pd.DataFrame(summary_items)
        # Apply formatting
        df_summary["Amount (₹)"] = df_summary["Amount (₹)"].map(lambda val: f"₹{val:,.2f}")
        
        # Output clean styled table
        st.dataframe(df_summary, hide_index=True, use_container_width=True)

    st.markdown("---")

    # 3. Insights section
    st.markdown("#### 💡 FinBud Coach Insights")
    
    insights = []
    
    if savings_rate <= 0:
        insights.append(
            ("🚨", "CRITICAL", f"Your net savings is negative (₹{savings:,.2f}). You are living beyond your means. Review your expenses in the **Expense Analysis** tab.")
        )
    elif savings_rate < 20.0:
        insights.append(
            ("⚠️", "WARNING", f"Your savings rate is {savings_rate:.1f}%, which is below the recommended fintech golden rule of 20%. Try the **Savings Planner** tab to see where to cut back.")
        )
    else:
        insights.append(
            ("🎉", "SUCCESS", f"Superb savings habits! You saved {savings_rate:.1f}% (₹{savings:,.2f}) this month. Consider investing your excess funds.")
        )

    rent_pct = (expenses.get("Rent/Hostel", 0.0) / income * 100) if income > 0 else 0
    if rent_pct > 35.0:
        insights.append(
            ("🏠", "RENT ALERT", f"Rent consumes {rent_pct:.1f}% of your monthly income (recommended: <30%). This reduces your financial flexibility.")
        )

    disc_total = expenses.get("Entertainment", 0.0) + expenses.get("Other", 0.0)
    disc_pct = (disc_total / income * 100) if income > 0 else 0
    if disc_pct > 25.0:
        insights.append(
            ("🎟️", "BUDGET ALERT", f"Discretionary spending (Entertainment + Other) is at {disc_pct:.1f}% of income. This is an easy area to find immediate savings.")
        )
        
    for emoji, title, text in insights:
        border_col = emerald_green if "SUCCESS" in title or "🎉" in emoji else (neon_red if "🚨" in emoji or "CRITICAL" in title else "#f1c40f")
        st.markdown(
            f"""
            <div style="
                background-color: rgba(255,255,255,0.02);
                border-left: 4px solid {border_col};
                padding: 1rem;
                margin-bottom: 0.8rem;
                border-radius: 0 8px 8px 0;
            ">
                <strong>{emoji} {title}:</strong> {text}
            </div>
            """,
            unsafe_allow_html=True
        )
