def detect_contradictions(kpis: dict, trends: dict, forecast: dict) -> list:
    """
    Identifies logical contradictions (e.g. Sales Up however Profit Down reported as an overall win).
    """
    contradictions = []
    
    direction = trends.get('direction') if trends else None
    forecast_confidence = forecast.get('confidence_note', '').lower() if forecast else ""
    
    if direction == 'up' and 'negative' in forecast_confidence:
        contradictions.append({
            "name": "growth_vs_forecast_conflict", 
            "status": "flagged", 
            "reason": "Recent trends are positive but the generated forecast represents a sharp decline."
        })
        
    keys = {k.lower() for k in kpis.keys()}
    if any('revenue' in k for k in keys) and any('profit' in k for k in keys):
        rev_trend = trends.get('revenue_trend', '') if trends else ''
        profit_trend = trends.get('profit_trend', '') if trends else ''
        
        if rev_trend == 'up' and profit_trend == 'down':
            contradictions.append({
                "name": "revenue_profit_divergence",
                "status": "flagged",
                "reason": "Revenue increased while profitability decreased. Potential margin erosion detected."
            })

    return contradictions
