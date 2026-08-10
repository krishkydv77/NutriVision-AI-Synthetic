def calculate_health_score(calories: float, protein: float, carbs: float, fat: float) -> float:
    """
    Calculates a heuristic Health Score out of 10 based on macronutrient balance.
    """
    score = 10.0
    
    # Penalty for excessive calories
    if calories > 400:
        score -= 2.0
    elif calories > 250:
        score -= 1.0
        
    # Penalty for high fat content
    if fat > 12:
        score -= 2.5
    elif fat > 6:
        score -= 1.0
        
    # Penalty for high carbs with low protein
    if carbs > 30 and protein < 3:
        score -= 2.0
        
    # Bonus for high protein
    if protein > 10:
        score += 1.0
        
    # Keep score bounded between 1.0 and 10.0
    return round(max(1.0, min(10.0, score)), 1)