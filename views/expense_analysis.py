import streamlit as st
import pandas as pd
import plotly.express as px
from utils.calculations import get_largest_expense_category

def render_expense_analysis(income, expenses, total_expenses):
    st.markdown("### 📈 Expense Analysis")
    
    if total_expenses <= 0:
        st.info("Please enter your expenses in the sidebar to view analysis charts.")
        return
        
    # Prepare data
    categories = list(expenses.keys())
    amounts = list(expenses.values())
    
    df = pd.DataFrame({
        "Category": categories,
        "Amount (₹)": amounts,
        "Percentage (%)": [(amt / total_expenses * 100) if total_expenses > 0 else 0 for amt in amounts]
    })
    
    # Clean zero expenses
    df_filtered = df[df["Amount (₹)"] > 0]
    
    if df_filtered.empty:
        st.info("No expenses entered yet.")
        return
        
    # Largest expense analysis
    largest_cat, largest_amt = get_largest_expense_category(expenses)
    largest_pct = (largest_amt / total_expenses * 100) if total_expenses > 0 else 0
    largest_income_pct = (largest_amt / income * 100) if income > 0 else 0
    
    # Display highlight banner for Largest Category
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, rgba(138, 43, 226, 0.1) 0%, rgba(0, 229, 255, 0.05) 100%);
            border: 1px solid rgba(138, 43, 226, 0.2);
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 2rem;
        ">
            <h4 style="margin: 0; color: #8A2BE2;">🔍 Largest Expense Target</h4>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; line-height: 1.6;">
                Your largest spending category is <strong>{largest_cat}</strong> at <strong>₹{largest_amt:,.2f}</strong>. 
                This accounts for <strong>{largest_pct:.1f}%</strong> of your total expenses and <strong>{largest_income_pct:.1f}%</strong> of your monthly income.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Columns for side-by-side charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("#### 🍩 Expense Share")
        fig_pie = px.pie(
            df_filtered,
            names="Category",
            values="Amount (₹)",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_pie.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8892b0", family="Outfit")
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_chart2:
        st.markdown("#### 📊 Category Comparison")
        # Horizontal Bar Chart
        fig_bar = px.bar(
            df_filtered.sort_values(by="Amount (₹)", ascending=True),
            x="Amount (₹)",
            y="Category",
            orientation="h",
            text="Amount (₹)",
            color="Category",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_bar.update_traces(
            texttemplate='₹%{x:,.2f}', 
            textposition='outside',
            cliponaxis=False
        )
        fig_bar.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", title=""),
            yaxis=dict(title=""),
            font=dict(color="#8892b0", family="Outfit")
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # Table breakdown
    st.markdown("#### 📋 Category Details")
    df_details = df_filtered.sort_values(by="Amount (₹)", ascending=False).reset_index(drop=True)
    df_details["Amount (₹)"] = df_details["Amount (₹)"].map(lambda v: f"₹{v:,.2f}")
    df_details["Percentage (%)"] = df_details["Percentage (%)"].map(lambda v: f"{v:.1f}%")
    st.dataframe(df_details, use_container_width=True, hide_index=True)
