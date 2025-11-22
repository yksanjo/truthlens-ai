"""
Utility functions for the hallucination meter.
"""
from typing import Dict, List


def format_score_display(score: float) -> str:
    """
    Format score for display.
    
    Args:
        score: Score from 0.0 to 1.0
        
    Returns:
        Formatted string
    """
    percentage = score * 100
    
    if percentage >= 75:
        emoji = "✅"
        label = "Highly Truthful"
    elif percentage >= 55:
        emoji = "⚠️"
        label = "Mostly Truthful"
    elif percentage >= 35:
        emoji = "❓"
        label = "Uncertain"
    else:
        emoji = "❌"
        label = "Likely Hallucination"
    
    return f"{emoji} {label} ({percentage:.1f}%)"


def format_verdict(verdict: str) -> str:
    """
    Format verdict for display.
    
    Args:
        verdict: Verdict string
        
    Returns:
        Human-readable verdict
    """
    verdict_map = {
        "highly_truthful": "✅ Highly Truthful",
        "mostly_truthful": "⚠️ Mostly Truthful",
        "uncertain": "❓ Uncertain",
        "likely_hallucination": "❌ Likely Hallucination",
        "supported": "✅ Supported",
        "weak_support": "⚠️ Weak Support",
        "contradicted": "❌ Contradicted",
        "no_evidence": "❓ No Evidence",
        "no_claims": "❓ No Claims",
        "error": "❌ Error"
    }
    
    return verdict_map.get(verdict, verdict)


def get_verdict_color(verdict: str) -> str:
    """
    Get color for verdict (for UI).
    
    Args:
        verdict: Verdict string
        
    Returns:
        Color name
    """
    if "truthful" in verdict or "supported" in verdict:
        return "green"
    elif "uncertain" in verdict or "weak" in verdict or "no_evidence" in verdict:
        return "orange"
    else:
        return "red"

