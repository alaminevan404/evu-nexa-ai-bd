import pandas as pd
import numpy as np
from typing import Dict, Any
from app.engine.base_strategy import BaseStrategyModule, IndicatorOutput

class RSIClassicModule(BaseStrategyModule):
    @property
    def module_id(self) -> str:
        return "rsi_classic"

    @property
    def name(self) -> str:
        return "RSI Classic Overbought/Oversold (14)"

    @property
    def category(self) -> str:
        return "momentum"

    def calculate(self, candles_df: pd.DataFrame, config: Dict[str, Any] = None) -> IndicatorOutput:
        if len(candles_df) < 20:
            return IndicatorOutput(
                module_id=self.module_id, name=self.name, category=self.category,
                signal="NEUTRAL", score=50.0, weight=1.0, metrics={}, reasoning_fragment="Insufficient RSI data."
            )

        close = candles_df['close']
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

        rs = gain / (loss + 1e-8)
        rsi = 100 - (100 / (1 + rs))
        current_rsi = rsi.iloc[-1]

        if current_rsi <= 30.0:
            signal = "BULLISH"
            score = 85.0 + (30.0 - current_rsi)
            reason = f"RSI reached Oversold territory ({current_rsi:.1f}), signaling strong upward mean reversion."
        elif current_rsi >= 70.0:
            signal = "BEARISH"
            score = 85.0 + (current_rsi - 70.0)
            reason = f"RSI reached Overbought territory ({current_rsi:.1f}), signaling strong downward mean reversion."
        elif current_rsi > 50.0:
            signal = "BULLISH"
            score = 65.0
            reason = f"RSI is above neutral midpoint ({current_rsi:.1f})."
        else:
            signal = "BEARISH"
            score = 65.0
            reason = f"RSI is below neutral midpoint ({current_rsi:.1f})."

        return IndicatorOutput(
            module_id=self.module_id, name=self.name, category=self.category,
            signal=signal, score=min(round(score, 1), 98.0), weight=1.1,
            metrics={"rsi_14": round(current_rsi, 2)}, reasoning_fragment=reason
        )

class MACDCrossoverModule(BaseStrategyModule):
    @property
    def module_id(self) -> str:
        return "macd_signal_crossover"

    @property
    def name(self) -> str:
        return "MACD Signal Crossover & Histogram Impulse"

    @property
    def category(self) -> str:
        return "momentum"

    def calculate(self, candles_df: pd.DataFrame, config: Dict[str, Any] = None) -> IndicatorOutput:
        if len(candles_df) < 35:
            return IndicatorOutput(
                module_id=self.module_id, name=self.name, category=self.category,
                signal="NEUTRAL", score=50.0, weight=1.0, metrics={}, reasoning_fragment="Insufficient MACD data."
            )

        close = candles_df['close']
        ema_12 = close.ewm(span=12, adjust=False).mean()
        ema_26 = close.ewm(span=26, adjust=False).mean()
        macd = ema_12 - ema_26
        signal_line = macd.ewm(span=9, adjust=False).mean()
        hist = macd - signal_line

        last_macd = macd.iloc[-1]
        last_sig = signal_line.iloc[-1]
        last_hist = hist.iloc[-1]
        prev_hist = hist.iloc[-2]

        if last_macd > last_sig:
            signal = "BULLISH"
            score = 80.0 if last_hist > prev_hist else 70.0
            reason = "MACD line is above Signal line with expanding bullish momentum."
        else:
            signal = "BEARISH"
            score = 80.0 if last_hist < prev_hist else 70.0
            reason = "MACD line is below Signal line with expanding bearish momentum."

        return IndicatorOutput(
            module_id=self.module_id, name=self.name, category=self.category,
            signal=signal, score=score, weight=1.2,
            metrics={"macd": round(last_macd, 5), "signal": round(last_sig, 5), "hist": round(last_hist, 5)},
            reasoning_fragment=reason
        )
