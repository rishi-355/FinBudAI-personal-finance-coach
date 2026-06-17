import os
import streamlit as st
import google.generativeai as genai
from pydantic import BaseModel


class FinanceAdvice(BaseModel):
    spending_analysis: str
    savings_recommendations: str
    health_assessment: str
    budget_optimization: str


def get_api_key() -> str:
    try:
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return os.environ.get("GEMINI_API_KEY", "")


def generate_coach_advice(income: float, expenses: dict) -> FinanceAdvice:
    api_key = get_api_key()

    if not api_key:
        raise ValueError("Gemini API key not found. Add GEMINI_API_KEY in .streamlit/secrets.toml")

    genai.configure(api_key=api_key)

    total_expenses = sum(expenses.values())
    savings = income - total_expenses
    savings_rate = (savings / income * 100) if income > 0 else 0

    prompt = f"""
You are FinBud, an AI Personal Finance Coach for students and young professionals in India.

User Financial Data:
Monthly Income: ₹{income:,.2f}
Rent/Hostel: ₹{expenses.get('Rent/Hostel', 0):,.2f}
Food: ₹{expenses.get('Food', 0):,.2f}
Transport: ₹{expenses.get('Transport', 0):,.2f}
Entertainment: ₹{expenses.get('Entertainment', 0):,.2f}
Other: ₹{expenses.get('Other', 0):,.2f}

Total Expenses: ₹{total_expenses:,.2f}
Net Savings: ₹{savings:,.2f}
Savings Rate: {savings_rate:.1f}%

Give output in this exact format:

Spending Analysis:
...

Savings Recommendations:
...

Health Assessment:
...

Budget Optimization:
- ...
- ...
- ...
"""

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        text = response.text

        return FinanceAdvice(
            spending_analysis=extract_section(text, "Spending Analysis", "Savings Recommendations"),
            savings_recommendations=extract_section(text, "Savings Recommendations", "Health Assessment"),
            health_assessment=extract_section(text, "Health Assessment", "Budget Optimization"),
            budget_optimization=extract_section(text, "Budget Optimization", None),
        )

    except Exception as e:
        raise RuntimeError(f"Error calling Gemini API: {str(e)}")


def extract_section(text: str, start: str, end: str | None) -> str:
    try:
        start_index = text.index(start) + len(start)
        if end:
            end_index = text.index(end)
            return text[start_index:end_index].replace(":", "").strip()
        return text[start_index:].replace(":", "").strip()
    except ValueError:
        return text