import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def render_dashboard(income, expenses, total_expenses, savings, savings_rate, health_score, health_status):
    # Colors matching design guidelines
    primary_blue = "#00E5FF"
    neon_red = "#FF5252"
    emerald_green = "#00E676"
    electric_purple = "#8A2BE2"
    
    # 1. Custom CSS injection for premium visual styling
    st.markdown(
        f"""
        <style>
            /* Hero banner styling */
            .fintech-hero {{
                background: radial-gradient(circle at top right, rgba(138, 43, 226, 0.12) 0%, rgba(0, 229, 255, 0.05) 50%, rgba(8, 10, 15, 0) 100%);
                border: 1px solid rgba(255, 255, 255, 0.03);
                border-radius: 20px;
                padding: 2.5rem;
                margin-bottom: 2rem;
                position: relative;
                overflow: hidden;
            }}
            .hero-tag {{
                color: #00E5FF;
                font-weight: 700;
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 3px;
                margin-bottom: 0.5rem;
            }}
            .hero-title {{
                font-size: 2.4rem;
                font-weight: 800;
                line-height: 1.2;
                margin-bottom: 0.5rem;
                background: linear-gradient(90deg, #F8FAFC 0%, #E2E8F0 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                letter-spacing: -1px;
            }}
            .hero-desc {{
                color: #64748B;
                font-size: 1.05rem;
                font-weight: 400;
            }}
            
            /* Glassmorphic Metric Cards */
            .glass-metric {{
                background: rgba(15, 20, 30, 0.6) !important;
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.04);
                border-radius: 16px;
                padding: 1.5rem;
                box-shadow: 0 10px 30px rgba(0,0,0,0.25);
                transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
                position: relative;
                overflow: hidden;
                margin-bottom: 1.25rem;
            }}
            .glass-metric:hover {{
                transform: translateY(-5px);
                border-color: rgba(138, 43, 226, 0.2);
                box-shadow: 0 15px 40px rgba(138, 43, 226, 0.15);
            }}
            .glass-metric::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, rgba(255,255,255,0.02) 0%, rgba(255,255,255,0) 100%);
                pointer-events: none;
            }}
            .metric-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 0.5rem;
            }}
            .metric-name {{
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                color: #64748B;
                font-weight: 600;
            }}
            .metric-icon {{
                font-size: 1.3rem;
                opacity: 0.85;
            }}
            .metric-number {{
                font-size: 2rem;
                font-weight: 800;
                margin-bottom: 0.25rem;
                letter-spacing: -0.5px;
            }}
            .metric-sub {{
                font-size: 0.75rem;
                color: #64748B;
                font-weight: 500;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # 2. Hero Section
    st.markdown(
        """
        <div class="fintech-hero">
            <div class="hero-tag">FinBud Platform</div>
            <div class="hero-title">Smart Money. Smarter Decisions.</div>
            <div class="hero-desc">Your AI-powered financial wellness platform. Build budgets, track progress, and get tailored strategies.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 3. Upgraded Glassmorphic Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div class="glass-metric" style="border-top: 3px solid {primary_blue};">
                <div class="metric-header">
                    <span class="metric-name">Monthly Inflow</span>
                    <span class="metric-icon" style="color: {primary_blue};">💳</span>
                </div>
                <div class="metric-number" style="color: #FFFFFF;">₹{income:,.2f}</div>
                <div class="metric-sub">Total primary income</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col2:
        st.markdown(
            f"""
            <div class="glass-metric" style="border-top: 3px solid {neon_red};">
                <div class="metric-header">
                    <span class="metric-name">Total Outflow</span>
                    <span class="metric-icon" style="color: {neon_red};">📉</span>
                </div>
                <div class="metric-number" style="color: {neon_red};">₹{total_expenses:,.2f}</div>
                <div class="metric-sub">{(total_expenses/income*100) if income > 0 else 0:.1f}% of income spent</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col3:
        savings_val_color = emerald_green if savings >= 0 else neon_red
        savings_icon = "💰" if savings >= 0 else "🚨"
        st.markdown(
            f"""
            <div class="glass-metric" style="border-top: 3px solid {emerald_green};">
                <div class="metric-header">
                    <span class="metric-name">Net Savings</span>
                    <span class="metric-icon" style="color: {savings_val_color};">{savings_icon}</span>
                </div>
                <div class="metric-number" style="color: {savings_val_color};">₹{savings:,.2f}</div>
                <div class="metric-sub">{savings_rate:.1f}% savings rate</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col4:
        health_colors = {
            "Excellent": emerald_green,
            "Good": "#F1C40F",
            "Fair": "#E67E22",
            "Needs Attention": neon_red
        }
        score_color = health_colors.get(health_status, electric_purple)
        st.markdown(
            f"""
            <div class="glass-metric" style="border-top: 3px solid {score_color};">
                <div class="metric-header">
                    <span class="metric-name">Health Index</span>
                    <span class="metric-icon" style="color: {score_color};">🩺</span>
                </div>
                <div class="metric-number" style="color: {score_color};">{health_score} <span style="font-size: 1rem; color: #64748B;">/100</span></div>
                <div class="metric-sub">Status: {health_status}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Main grid: Plotly gauge (left) and styled savings breakdown list (right)
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("#### 🩺 Financial Health Meter")
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=health_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#475569", 'tickfont': {'family': 'Plus Jakarta Sans', 'size': 11}},
                'bar': {'color': electric_purple, 'thickness': 0.25},
                'bgcolor': "rgba(255,255,255,0.01)",
                'borderwidth': 1,
                'bordercolor': "rgba(255,255,255,0.05)",
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(255, 82, 82, 0.08)'},
                    {'range': [40, 60], 'color': 'rgba(230, 126, 34, 0.08)'},
                    {'range': [60, 80], 'color': 'rgba(241, 196, 15, 0.08)'},
                    {'range': [80, 100], 'color': 'rgba(0, 230, 118, 0.08)'}
                ],
            }
        ))
        fig_gauge.update_layout(
            margin=dict(t=30, b=10, l=30, r=30),
            height=260,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#94A3B8", family="Plus Jakarta Sans")
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_right:
        st.markdown("#### 📝 Monthly Savings Summary")
        
        summary_items = {
            "Allocation Category": ["Monthly Income", "Fixed Costs (Rent)", "Living Expenses (Food, Transport)", "Discretionary (Entertainment, Other)", "Net Savings"],
            "Amount (₹)": [
                income,
                expenses.get("Rent/Hostel", 0.0),
                expenses.get("Food", 0.0) + expenses.get("Transport", 0.0),
                expenses.get("Entertainment", 0.0) + expenses.get("Other", 0.0),
                savings
            ]
        }
        df_summary = pd.DataFrame(summary_items)
        df_summary["Amount (₹)"] = df_summary["Amount (₹)"].map(lambda val: f"₹{val:,.2f}")
        
        # Displaying data inside a clean table
        st.dataframe(df_summary, hide_index=True, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. Coach Insights section with premium styling
    st.markdown("#### 💡 FinBud Coach Insights")
    
    insights = []
    
    if savings_rate <= 0:
        insights.append(
            ("🚨", "CRITICAL", f"Your net savings is negative (₹{savings:,.2f}). You are spending more than you earn. Review category spends in the **Expense Analysis** page.")
        )
    elif savings_rate < 20.0:
        insights.append(
            ("⚠️", "WARNING", f"Your savings rate is {savings_rate:.1f}%, which is below the target baseline of 20%. Try editing budgets in the **Savings Planner** page.")
        )
    else:
        insights.append(
            ("🎉", "SUCCESS", f"Awesome savings habits! You saved {savings_rate:.1f}% (₹{savings:,.2f}) this month. Consider checking investment plans.")
        )

    rent_pct = (expenses.get("Rent/Hostel", 0.0) / income * 100) if income > 0 else 0
    if rent_pct > 35.0:
        insights.append(
            ("🏠", "HOUSING BUDGET", f"Rent consumes {rent_pct:.1f}% of your monthly income. Keeping housing costs under 30% creates more financial breathing room.")
        )

    disc_total = expenses.get("Entertainment", 0.0) + expenses.get("Other", 0.0)
    disc_pct = (disc_total / income * 100) if income > 0 else 0
    if disc_pct > 25.0:
        insights.append(
            ("🎟️", "BUDGET ALERT", f"Discretionary spending (Entertainment + Other) is at {disc_pct:.1f}% of income. Scaling this back is the fastest way to save.")
        )
        
    for emoji, title, text in insights:
        border_col = emerald_green if "SUCCESS" in title or "🎉" in emoji else (neon_red if "🚨" in emoji or "CRITICAL" in title else "#F1C40F")
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, rgba(22, 28, 41, 0.4) 0%, rgba(10, 12, 16, 0.4) 100%);
                border: 1px solid rgba(255, 255, 255, 0.03);
                border-left: 5px solid {border_col};
                padding: 1.2rem;
                margin-bottom: 0.8rem;
                border-radius: 0 10px 10px 0;
                box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            ">
                <strong style="color: {border_col};">{emoji} {title}:</strong> <span style="color: #E2E8F0;">{text}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
