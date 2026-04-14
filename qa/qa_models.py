def init_qa_report() -> dict:
    """Initializes the empty schema for a QA Validation test."""
    return {
        "overall_status": "pending",
        "confidence": "high",
        "metric_checks": [],
        "narrative_checks": [],
        "chart_checks": [],
        "contradictions": [],
        "warnings": []
    }
