import pandas as pd
import numpy as np
from typing import Dict, Any
from app.engine.base_strategy import BaseStrategyModule, IndicatorOutput

class EMACrossoverModule(BaseStrategyModule):
    @property
    def module_id(self) -> str:
        return "ema_crossover"

    @property
    def name(self) -> str:
        return "Fast/Slow EMA Crossover (9/21)"

    @property
    def category(self) -> str:
        return "trend"

    def calculate(self, candles_df: pd.DataFrame, config: Dict[str, Any] = None) -> IndicatorOutput:
        if len(candles_df) < 25:
            return IndicatorOutput(
                module_id=self.module_id, name=self.name, category=self.category,
                signal="NEUTRAL", score=50.0, weight=1.0, metrics={},
                reasoning_fragment="Insufficient candle data for EMA calculation."
            )

        close = candles_df['close']
        ema_fast = close.ewm(span=9, adjust=False).mean()
        ema_slow = close.ewm(span=21, adjust=False).mean()

        last_fast = ema_fast.iloc[-1]
        last_slow = ema_slow.iloc[-1]
        prev_fast = ema_fast.iloc[-2]
        prev_slow = ema_slow.iloc[-2]

        diff_pct = (last_fast - last_slow) / last_slow * 100

        if last_fast > last_slow:
            if prev_fast <= prev_slow:
                signal = "BULLISH"
                score = 90.0
                reason = "Fresh Bullish Golden Cross of EMA 9 over EMA 21."
            else:
                signal = "BULLISH"
                score = 75.0
                reason = f"EMA 9 is trading above EMA 21 (Spread: {diff_pct:.2f}%)."
        elif last_fast < last_slow:
            if prev_fast >= prev_slow:
                signal = "BEARISH"
                score = 90.0
                reason = "Fresh Bearish Death Cross of EMA 9 under EMA 21."
            else:
                signal = "BEARISH"
                score = 75.0
                reason = f"EMA 9 is trading below EMA 21 (Spread: {diff_pct:.2f}%)."
        else:
            signal = "NEUTRAL"
            score = 50.0
            reason = "EMA 9 and EMA 21 lines are converged."

        return IndicatorOutput(
            module_id=self.module_id,
            name=self.name,
            category=self.category,
            signal=signal,
            score=score,
            weight=1.2,
            metrics={"ema_9": round(last_fast, 5), "ema_21": round(last_slow, 5)},
            reasoning_fragment=reason
        )

class ADXStrengthModule(BaseStrategyModule):
    @property
    def module_id(self) -> str:
        return "adx_trend_strength"

    @property
    def name(self) -> str:
        return "ADX Trend Strength & Direction"

    @property
    def category(self) -> str:
        return "trend"

    def calculate(self, candles_df: pd.DataFrame, config: Dict[str, Any] = None) -> IndicatorOutput:
        if len(candles_df) < 30:
            return IndicatorOutput(
                module_id=self.module_id, name=self.name, category=self.category,
                signal="NEUTRAL", score=50.0, weight=1.0, metrics={},
                reasoning_fragment="Insufficient data for ADX calculation."
            )

        high = candles_df['high']
        low = candles_df['low']
        close = candles_df['close']

        up_move = high - high.shift(1)
        down_move = low.shift(1) - low

        plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
        minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)

        tr = np.maximum(high - low, np.maximum(abs(high - close.shift(1)), abs(low - close.shift(1))))
        tr_smooth = pd.Series(tr).ewm(span=14, adjust=False).mean()

        plus_di = 100 * pd.Series(plus_dm).ewm(span=14, adjust=False).mean() / tr_smooth
        minus_di = 100 * pd.Series(minus_dm).ewm(span=14, adjust=False).mean() / tr_smooth

        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di + 1e-8)
        adx = pd.Series(dx).ewm(span=14, adjust=False).mean().iloc[-1]

        p_di = plus_di.iloc[-1]
        m_di = minus_di.iloc[-1]

        if adx > 25:
            if p_di > m_di:
                signal = "BULLISH"
                score = min(50.0 + adx, 95.0)
                reason = f"Strong Bullish Trend confirmed by ADX ({adx:.1f}) with +DI > -DI."
            else:
                signal = "BEARISH"
                score = min(50.0 + adx, 95.0)
                reason = f"Strong Bearish Trend confirmed by ADX ({adx:.1f}) with -DI > +DI."
        else:
            signal = "NEUTRAL"
            score = 50.0
            reason = f"Weak/Ranging Trend state indicated by low ADX ({adx:.1f})."

        return IndicatorOutput(
            module_id=self.module_id, name=self.name, category=self.category,
            signal=signal, score=round(score, 1), weight=1.1,
            metrics={"adx": round(adx, 2), "plus_di": round(p_di, 2), "minus_di": round(m_di, 2)},
            reasoning_fragment=reason
        )
