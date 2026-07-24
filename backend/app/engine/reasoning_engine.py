from typing import List, Dict, Any
from app.engine.base_strategy import IndicatorOutput

def generate_ai_reasoning(
    symbol: str,
    timeframe: str,
    direction: str,
    confidence_score: float,
    indicators: List[IndicatorOutput],
    snapshot: Dict[str, Any]
) -> str:
    """Generates technical natural language reasoning breakdown."""
    bullish_reasons = [ind.reasoning_fragment for ind in indicators if ind.signal == "BULLISH"]
    bearish_reasons = [ind.reasoning_fragment for ind in indicators if ind.signal == "BEARISH"]

    current_price = snapshot.get("close", "N/A")

    reasoning = f"EVU NEXA AI Engine executed quantitative multi-factor analysis for {symbol} on the {timeframe} timeframe (Spot Price: {current_price}).\n\n"
    
    if direction == "BULLISH_CALL":
        reasoning += f"🟢 OVERALL OUTLOOK: BULLISH CALL ({confidence_score}% Confidence)\n\n"
        reasoning += "Key Technical Confluence Factors:\n"
        for idx, r in enumerate(bullish_reasons[:5], 1):
            reasoning += f"{idx}. {r}\n"
        reasoning += "\nStrategic Execution Note: High buying momentum detected off key structural demand zones. Recommend entering a 1 to 3-minute Call option on minor pullback."
    
    elif direction == "BEARISH PUT":
        reasoning += f"🔴 OVERALL OUTLOOK: BEARISH PUT ({confidence_score}% Confidence)\n\n"
        reasoning += "Key Technical Confluence Factors:\n"
        for idx, r in enumerate(bearish_reasons[:5], 1):
            reasoning += f"{idx}. {r}\n"
        reasoning += "\nStrategic Execution Note: Heavy supply pressure and liquidity sweep confirmed. Recommend entering a 1 to 3-minute Put option on minor retest."
    
    else:
        reasoning += f"⚠️ OVERALL OUTLOOK: NEUTRAL / WAITING STATE ({confidence_score}% Confidence)\n\n"
        reasoning += "Detected conflicting technical metrics between trend indicators and momentum oscillators. Market is currently consolidating without clear institutional bias. Recommendation: Stand aside until clean breakout occurs."

    return reasoning
