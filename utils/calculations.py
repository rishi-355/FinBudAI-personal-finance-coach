"""
calculations.py - Financial formulas and health scoring logic for FinBud.
"""

def calculate_total_expenses(rent: float, food: float, transport: float, entertainment: float, other: float) -> float:
    """Calculate the total expenses from individual category values."""
    return float(rent + food + transport + entertainment + other)

def calculate_savings(income: float, total_expenses: float) -> float:
    """Calculate the net savings (income - expenses). Can be negative."""
    return float(income - total_expenses)

def calculate_savings_rate(income: float, savings: float) -> float:
    """
    Calculate the savings rate as a percentage of income.
    If income is <= 0, savings rate is 0.0%.
    """
    if income <= 0:
        return 0.0
    # Even if savings are negative, return the actual percentage
    return float((savings / income) * 100)

def calculate_financial_health_score(income: float, rent: float, entertainment: float, other: float, savings_rate: float) -> tuple[int, str]:
    """
    Calculate a Financial Health Score (0 - 100) and return it along with a status string.
    
    Scoring system:
    1. Savings Rate (max 50 points):
       - >= 30% savings rate = 50 pts
       - <= 0% savings rate = 0 pts
       - In between: linear scale
    2. Rent/Hostel ratio to income (max 30 points):
       - <= 30% of income = 30 pts
       - >= 50% of income = 0 pts
       - In between: linear decline
    3. Discretionary Spending ratio (Entertainment + Other) (max 20 points):
       - <= 20% of income = 20 pts
       - >= 40% of income = 0 pts
       - In between: linear decline
    """
    if income <= 0:
        return 0, "Needs Attention (No Income)"
    
    # 1. Savings Rate Score
    if savings_rate <= 0:
        savings_score = 0.0
    elif savings_rate >= 30.0:
        savings_score = 50.0
    else:
        savings_score = (savings_rate / 30.0) * 50.0
        
    # 2. Rent Ratio Score
    rent_ratio = rent / income
    if rent_ratio <= 0.30:
        rent_score = 30.0
    elif rent_ratio >= 0.50:
        rent_score = 0.0
    else:
        rent_score = 30.0 * (1.0 - (rent_ratio - 0.30) / 0.20)
        
    # 3. Discretionary spending score (Entertainment + Other)
    disc_spend = entertainment + other
    disc_ratio = disc_spend / income
    if disc_ratio <= 0.20:
        disc_score = 20.0
    elif disc_ratio >= 0.40:
        disc_score = 0.0
    else:
        disc_score = 20.0 * (1.0 - (disc_ratio - 0.20) / 0.20)
        
    total_score = round(savings_score + rent_score + disc_score)
    total_score = max(0, min(100, total_score)) # Ensure within bounds
    
    # Categorize status
    if total_score >= 80:
        status = "Excellent"
    elif total_score >= 60:
        status = "Good"
    elif total_score >= 40:
        status = "Fair"
    else:
        status = "Needs Attention"
        
    return total_score, status

def get_largest_expense_category(expenses: dict) -> tuple[str, float]:
    """
    Identify the category with the highest spending from a dictionary of expenses.
    Returns a tuple of (category_name, amount).
    """
    if not expenses:
        return "None", 0.0
    # Find the max expense category
    largest_cat = max(expenses, key=expenses.get)
    return largest_cat, float(expenses[largest_cat])

