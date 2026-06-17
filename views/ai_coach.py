import streamlit as st
import os
from utils.gemini_service import get_api_key, generate_coach_advice

def render_ai_coach(income, expenses, total_expenses, savings, savings_rate, health_score, health_status):
    st.markdown("### 🤖 FinBud AI Financial Coach")
    st.markdown("*Custom personalized financial strategies powered by Google Gemini AI.*")
    st.markdown("---")

    # 1. API Key Check & Configuration helper
    api_key = get_api_key()
    temp_key = st.session_state.get("temp_gemini_key", "")
    
    # Check if we have any key
    has_key = bool(api_key or temp_key)

    if not has_key:
        st.warning("⚠️ **Gemini API Key Missing**")
        st.markdown(
            """
            To activate your AI Financial Coach, you need to configure a Google Gemini API Key.
            
            **How to configure:**
            1. Create a folder named `.streamlit` in the root of your project directory.
            2. Inside it, create a file named `secrets.toml`.
            3. Add your key like this:
               ```toml
               GEMINI_API_KEY = "your_actual_api_key_here"
               ```
            
            *Alternatively, you can paste your key in the temporary field below to test it immediately:*
            """
        )
        input_key = st.text_input("Temporary Gemini API Key", type="password", help="This key is only stored in memory for this session.")
        if input_key:
            st.session_state.temp_gemini_key = input_key
            # Inject temporarily into environment for the service wrapper to pick up
            os.environ["GEMINI_API_KEY"] = input_key
            st.rerun()
            
        st.markdown("---")

    # 2. Display User Financial Data to be sent
    st.subheader("📋 Shareable Financial Profile")
    st.markdown("Here is the data that will be analyzed by your FinBud AI Coach:")

    col_data1, col_data2 = st.columns(2)
    
    with col_data1:
        st.markdown(
            f"""
            <div style="background-color: rgba(255, 255, 255, 0.02); padding: 1.25rem; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.05);">
                <strong>Inflow Profile:</strong><br>
                • Monthly Income: ₹{income:,.2f}<br>
                • Net Savings: ₹{savings:,.2f}<br>
                • Savings Rate: {savings_rate:.1f}%
            </div>
            """,
            unsafe_allow_html=True
        )
        
    with col_data2:
        st.markdown(
            f"""
            <div style="background-color: rgba(255, 255, 255, 0.02); padding: 1.25rem; border-radius: 8px; border: 1px solid rgba(255, 255, 255, 0.05);">
                <strong>Outflow Breakdown:</strong><br>
                • Rent / Hostel: ₹{expenses.get('Rent/Hostel', 0.0):,.2f}<br>
                • Food: ₹{expenses.get('Food', 0.0):,.2f}<br>
                • Transport: ₹{expenses.get('Transport', 0.0):,.2f}<br>
                • Entertainment: ₹{expenses.get('Entertainment', 0.0):,.2f}<br>
                • Other: ₹{expenses.get('Other', 0.0):,.2f}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Action button: Generate AI Advice
    col_btn_l, col_btn_r = st.columns([1, 4])
    
    with col_btn_l:
        # Enable button only if we have a key
        generate_btn = st.button("Generate AI Advice ⚡", disabled=not has_key, use_container_width=True)
        
    with col_btn_r:
        if not has_key:
            st.caption("Please configure a Gemini API key to enable advice generation.")
        else:
            st.caption("Ready to generate. Analysis usually takes 2-3 seconds.")

    # 4. Handle Generation & API invocation
    if generate_btn:
        with st.spinner("FinBud AI is auditing your budgets and planning strategies..."):
            try:
                # Call gemini service
                advice = generate_coach_advice(income, expenses)
                # Store in session state to persist across reruns
                st.session_state.gemini_advice = advice
                st.success("🎉 Financial strategy report compiled successfully!")
            except Exception as e:
                st.error(f"Failed to generate advice: {str(e)}")

    st.markdown("---")

    # 5. Display Structured Advice
    if "gemini_advice" in st.session_state:
        advice = st.session_state.gemini_advice
        
        st.subheader("🏆 Your Personalized Wealth Report")
        
        # Styles for the professional response cards
        st.markdown("""
            <style>
                .advice-card {
                    background: linear-gradient(135deg, rgba(20, 24, 33, 0.8) 0%, rgba(10, 12, 16, 0.8) 100%);
                    border: 1px solid rgba(255, 255, 255, 0.05);
                    border-radius: 12px;
                    padding: 1.5rem;
                    margin-bottom: 1.25rem;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.25);
                }
                .advice-title {
                    font-size: 1.15rem;
                    font-weight: 600;
                    margin-bottom: 0.75rem;
                    display: flex;
                    align-items: center;
                }
                .advice-body {
                    font-size: 0.95rem;
                    color: #CBD5E1;
                    line-height: 1.6;
                }
            </style>
        """, unsafe_allow_html=True)
        
        # Grid layout for structured outputs (2 columns, 2 rows)
        col_row1_l, col_row1_r = st.columns(2)
        
        with col_row1_l:
            st.markdown(
                f"""
                <div class="advice-card" style="border-top: 3px solid #00E5FF;">
                    <div class="advice-title" style="color: #00E5FF;">📊 Spending Analysis</div>
                    <div class="advice-body">{advice.spending_analysis}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col_row1_r:
            st.markdown(
                f"""
                <div class="advice-card" style="border-top: 3px solid #00E676;">
                    <div class="advice-title" style="color: #00E676;">💡 Savings Recommendations</div>
                    <div class="advice-body">{advice.savings_recommendations}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        col_row2_l, col_row2_r = st.columns(2)
        
        with col_row2_l:
            st.markdown(
                f"""
                <div class="advice-card" style="border-top: 3px solid #f1c40f;">
                    <div class="advice-title" style="color: #f1c40f;">🩺 Financial Health Assessment</div>
                    <div class="advice-body">{advice.health_assessment}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col_row2_r:
            st.markdown(
                f"""
                <div class="advice-card" style="border-top: 3px solid #8A2BE2;">
                    <div class="advice-title" style="color: #8A2BE2;">🎛️ Budget Optimization Tips</div>
                    <div class="advice-body">{advice.budget_optimization}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        # Option to clear advice and run again
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Clear Report"):
            del st.session_state.gemini_advice
            st.rerun()
    else:
        st.info("💡 Click the 'Generate AI Advice' button above to receive custom budgeting strategies from Gemini.")
