import re

def validate_narratives(insights: str, kpis: dict, trends: dict) -> list:
    """
    Validates that NLP generated textual narratives factually represent the underlying trend data.
    """
    checks = []
    if not insights:
        return checks
        
    lower_insights = insights.lower()
    
    # Semantic rules checking for contradiction against trend direction
    if "increase" in lower_insights or "growth" in lower_insights:
        if trends and trends.get('direction') == 'down':
             checks.append({"name": "direction_up", "status": "fail", "reason": "Text implicitly claims 'increase' but quantitative trends show downward direction."})
        else:
             checks.append({"name": "direction_up", "status": "pass"})
             
    if "decrease" in lower_insights or "drop" in lower_insights:
        if trends and trends.get('direction') == 'up':
             checks.append({"name": "direction_down", "status": "fail", "reason": "Text implicitly claims 'decrease' but quantitative trends show upward direction."})
        else:
             checks.append({"name": "direction_down", "status": "pass"})
             
    # Strict hallucination mitigation: Check unverified numbers
    numbers_in_text = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b', insights)
    all_kpi_text = " ".join([str(v) for v in kpis.values()])
    hallucination_fail = False
    
    for num in set(numbers_in_text):
        try:
            parsed_num = float(num.replace(',',''))
            # Ignore rank / percentage syntax structure figures under 100
            if parsed_num > 100: 
                if num not in all_kpi_text:
                    checks.append({
                        "name": f"number_verification_{num}", 
                        "status": "fail", 
                        "reason": f"Hallucination Warning: Number {num} cited but not found in verified quantitative KPI outputs."
                    })
                    hallucination_fail = True
        except ValueError:
            pass
            
    if not hallucination_fail:
        checks.append({"name": "hallucination_check", "status": "pass"})
        
    return checks
