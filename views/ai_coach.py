import streamlit as st

def render_ai_coach(income, expenses, total_expenses, savings, savings_rate, health_score, health_status):
    st.markdown("### 🤖 FinBud AI Coach")
    st.markdown("*Your intelligent personal finance advisor. powered by advanced AI.*")
    
    # Initialize mock chat history in session state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I am FinBud, your AI Personal Finance Coach. Ask me anything about budgeting, saving, or optimizing your financial health score!"}
        ]
        
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Sidebar / Section triggers for presets
    st.markdown("#### 💡 Quick Questions")
    col1, col2, col3 = st.columns(3)
    
    selected_preset = None
    
    with col1:
        if st.button("How to raise my score?", use_container_width=True):
            selected_preset = "How can I improve my Financial Health Score?"
    with col2:
        if st.button("Explain 50/30/20 rule", use_container_width=True):
            selected_preset = "Can you explain the 50/30/20 budget rule?"
    with col3:
        if st.button("Analyze my current rent", use_container_width=True):
            selected_preset = f"Is my monthly rent of ₹{expenses.get('Rent/Hostel', 0):,.2f} reasonable for my income?"

    # Input text from chat input
    user_query = st.chat_input("Ask FinBud a question...")

    # Process input (either preset button or manual text)
    query_to_process = user_query or selected_preset

    if query_to_process:
        # Add user query to chat history
        st.session_state.chat_history.append({"role": "user", "content": query_to_process})
        with st.chat_message("user"):
            st.markdown(query_to_process)
            
        # Generate mock responses based on input
        with st.chat_message("assistant"):
            with st.spinner("FinBud is thinking..."):
                response = ""
                query_lower = query_to_process.lower()
                
                if "score" in query_lower:
                    response = (
                        f"To improve your current health score of **{health_score}/100**, here are three concrete steps:\n\n"
                        f"1. **Boost your savings rate:** Your current savings rate is **{savings_rate:.1f}%**. Earning a score of 80+ requires aiming for a 20-30% savings rate.\n"
                        f"2. **Reduce fixed costs:** Your rent of **₹{expenses.get('Rent/Hostel', 0):,.2f}** represents **{(expenses.get('Rent/Hostel', 0)/income*100) if income > 0 else 0:.1f}%** of your income. Keeping this under 30% boosts your score by 30 points.\n"
                        f"3. **Cut discretionary costs:** Try setting a hard limit on Entertainment and Other categories."
                    )
                elif "50/30/20" in query_lower:
                    response = (
                        "The **50/30/20 rule** is a simple budgeting guideline:\n\n"
                        "*   **50% Needs:** Essential expenses like housing, groceries, utilities, and insurance.\n"
                        "*   **30% Wants:** Discretionary choices like dining out, entertainment, and shopping.\n"
                        "*   **20% Savings:** Savings, emergency funds, or paying off debt.\n\n"
                        f"Based on your profile, your Needs represent **{((expenses.get('Rent/Hostel', 0) + expenses.get('Food', 0) + expenses.get('Transport', 0)) / income * 100) if income > 0 else 0:.1f}%**, "
                        f"your Wants represent **{((expenses.get('Entertainment', 0) + expenses.get('Other', 0)) / income * 100) if income > 0 else 0:.1f}%**, "
                        f"and your Savings rate is **{savings_rate:.1f}%**."
                    )
                elif "rent" in query_lower:
                    rent_pct = (expenses.get("Rent/Hostel", 0) / income * 100) if income > 0 else 0
                    if rent_pct > 30.0:
                        response = (
                            f"Your rent of **₹{expenses.get('Rent/Hostel', 0):,.2f}** consumes **{rent_pct:.1f}%** of your monthly income.\n\n"
                            f"⚠️ **Yes, this is higher than recommended.** The golden standard is to keep housing under 30% of your gross income. "
                            f"Since you are above this mark, it places pressure on your ability to save. Consider looking for roommates, "
                            f"refinancing, or trimming down on variable costs like Entertainment to offset this high fixed cost."
                        )
                    else:
                        response = (
                            f"Your rent of **₹{expenses.get('Rent/Hostel', 0):,.2f}** consumes **{rent_pct:.1f}%** of your monthly income.\n\n"
                            f"✅ **This is very reasonable!** Keeping housing under 30% of your income is a cornerstone of financial health. "
                            f"It leaves you with plenty of breathing room for food, transportation, and savings."
                        )
                else:
                    response = (
                        "That is a great question! I'm currently running on a rules-based mock engine. "
                        "Once my Gemini AI cognitive core is active, I will be able to answer any custom financial queries, "
                        "analyze upload statements, and build tailored savings plans for you! Stay tuned!"
                    )
                
                # Append to state and display
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.markdown(response)
                
        # Force rerun to show new messages immediately
        st.rerun()

    # Clear chat button
    if len(st.session_state.chat_history) > 1:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Reset Chat"):
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Hello! I am FinBud, your AI Personal Finance Coach. Ask me anything about budgeting, saving, or optimizing your financial health score!"}
            ]
            st.rerun()
