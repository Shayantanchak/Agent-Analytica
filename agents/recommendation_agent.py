class RecommendationAgent:
    """
    Phase 5: Recommendation Engine
    Maps anomalies and forecasts into actionable executive steps ranked by impact.
    """
    def __init__(self, api_key=None):
        self.api_key = api_key
        
    def execute(self, anomalies: dict, forecast: dict) -> dict:
        recommendations = []
        
        # 1. Anomaly-Driven Recommendations
        high_severity = [a for a in anomalies.get("flags", []) if a.get("severity") == "high"]
        if high_severity:
            targets = list(set([str(a.get('column')) for a in high_severity]))
            recommendations.append({
                "action": f"Immediate Audit of data inputs affecting: {', '.join(targets)}",
                "impact": "High",
                "effort": "Medium",
                "reasoning": f"Detected {len(high_severity)} high-severity deviations requiring critical business review."
            })
            
        # 2. Forecast-Driven Recommendations
        if not forecast.get("error"):
            target = forecast.get("target")
            points = forecast.get("forecast", [])
            if len(points) >= 2:
                trend_diff = points[-1]["Predicted_Value"] - points[0]["Predicted_Value"]
                if trend_diff < 0:
                    recommendations.append({
                        "action": f"Implement cost-controls or pivot strategy for {target}",
                        "impact": "High",
                        "effort": "High",
                        "reasoning": f"Negative linear trend projected (-{abs(trend_diff):.2f}) over the forecasted horizon for {target}."
                    })
                else:
                    recommendations.append({
                        "action": f"Scale operational bandwidth corresponding to {target} growth",
                        "impact": "Medium",
                        "effort": "High",
                        "reasoning": f"Positive trajectory forecasting +{trend_diff:.2f} value appreciation over future horizons."
                    })
                    
        # 3. Fallback Steady-State Action
        if not recommendations:
            recommendations.append({
                "action": "Maintain current operational parameters",
                "impact": "Low",
                "effort": "Low",
                "reasoning": "No extreme statistical deviations or detrimental trend shifts detected in current data bounds."
            })
            
        # Rank by Impact Score
        priority_map = {"High": 3, "Medium": 2, "Low": 1}
        recommendations.sort(key=lambda x: priority_map.get(x["impact"], 0), reverse=True)
            
        return {"actionable_steps": recommendations}
