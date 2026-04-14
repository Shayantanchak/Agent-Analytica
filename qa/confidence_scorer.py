def score_confidence(report: dict) -> str:
    """
    Scores the overall trust of the output based on hard failures vs warnings.
    """
    fails = sum(1 for c in report.get("metric_checks", []) if c.get("status") == "fail")
    fails += sum(1 for c in report.get("narrative_checks", []) if c.get("status") == "fail")
    fails += sum(1 for c in report.get("chart_checks", []) if c.get("status") == "fail")
    
    contradictions = len(report.get("contradictions", []))
    
    if fails == 0 and contradictions == 0:
        return "high"
    elif fails == 0 and contradictions > 0:
        return "medium"
    elif fails <= 2:
        return "medium"
    else:
        return "low"

def derive_status(report: dict) -> str:
    """
    Calculates final pass/fail state logic.
    """
    conf = score_confidence(report)
    if conf == "high":
        return "passed"
    elif conf == "medium":
        return "passed_with_warnings"
    else:
        return "failed"
