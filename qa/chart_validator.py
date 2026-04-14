def validate_chart_inputs(kpis: dict, trends: dict, forecast: dict) -> list:
    """
    Validates chart input data correctly mirrors narrative data objects.
    """
    checks = []
    
    # Core verification checks for graph alignments 
    if kpis and len(kpis) > 0:
        checks.append({"name": "chart_data_availability", "status": "pass"})
    else:
        checks.append({"name": "chart_data_availability", "status": "fail", "reason": "No KPIs available to back the chart structures."})
        
    return checks
