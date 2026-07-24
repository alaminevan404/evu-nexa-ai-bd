from typing import List, Dict, Any, Tuple
from app.engine.base_strategy import IndicatorOutput

def aggregate_signals(indicator_outputs: List[IndicatorOutput]) -> Tuple[str, float, str]:
    """
    Combines outputs from active indicators into a dynamic weighted signal.
    Returns: (direction, confidence_score, risk_level)
    """
    if not indicator_outputs:
        return "NEUTRAL", 50.0, "MEDIUM"

    total_weighted_score = 0.0
    total_weight = 0.0

    for out in indicator_outputs:
        direction_multiplier = 0.0
        if out.signal == "BULLISH":
            direction_multiplier = 1.0
        elif out.signal == "BEARISH":
            direction_multiplier = -1.0
        
        weighted_val = direction_multiplier * out.score * out.weight
        total_weighted_score += weighted_val
        total_weight += out.weight

    if total_weight == 0:
        return "NEUTRAL", 50.0, "MEDIUM"

    raw_score = total_weighted_score / total_weight  # Range: -100.0 to +100.0

    confidence_score = abs(raw_score)

    if raw_score >= 25.0:
        direction = "BULLISH_CALL"
    elif raw_score <= -25.0:
        direction = "BEARISH_PUT"
    else:
        direction = "NEUTRAL"

    # Determine Risk Level
    if confidence_score >= 80.0:
        risk_level = "LOW"
    elif confidence_score >= 65.0:
        risk_level = "MEDIUM"
    elif confidence_score >= 45.0:
        risk_level = "HIGH"
    else:
        risk_level = "EXTREME"

    return direction, round(confidence_score, 1), risk_level
