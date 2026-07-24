import pandas as pd
import numpy as np
from typing import Dict, Any
from app.engine.base_strategy import BaseStrategyModule, IndicatorOutput

class SMCOrderBlockModule(BaseStrategyModule):
    @property
    def module_id(self) -> str:
        return "smc_order_block"

    @property
    def name(self) -> str:
        return "Smart Money Concepts (SMC) Order Block Detector"

    @property
    def category(self) -> str:
        return "smc_ict"

    def calculate(self, candles_df: pd.DataFrame, config: Dict[str, Any] = None) -> IndicatorOutput:
        if len(candles_df) < 15:
            return IndicatorOutput(
                module_id=self.module_id, name=self.name, category=self.category,
                signal="NEUTRAL", score=50.0, weight=1.0, metrics={}, reasoning_fragment="Insufficient SMC data."
            )

        df = candles_df.tail(10).reset_index(drop=True)
        current_close = df.iloc[-1]['close']

        # Bullish OB: Last down candle before a strong upward impulse move
        bullish_ob_price = None
        for i in range(len(df) - 4, 1, -1):
            if df.iloc[i]['close'] < df.iloc[i]['open']:  # Down candle
                impulse = (df.iloc[i+1]['close'] - df.iloc[i+1]['open']) + (df.iloc[i+2]['close'] - df.iloc[i+2]['open'])
                if impulse > (df.iloc[i]['high'] - df.iloc[i]['low']) * 1.5:
                    bullish_ob_price = df.iloc[i]['low']
                    break

        # Bearish OB: Last up candle before a strong downward impulse move
        bearish_ob_price = None
        for i in range(len(df) - 4, 1, -1):
            if df.iloc[i]['close'] > df.iloc[i]['open']:  # Up candle
                impulse = (df.iloc[i+1]['open'] - df.iloc[i+1]['close']) + (df.iloc[i+2]['open'] - df.iloc[i+2]['close'])
                if impulse > (df.iloc[i]['high'] - df.iloc[i]['low']) * 1.5:
                    bearish_ob_price = df.iloc[i]['high']
                    break

        if bullish_ob_price and abs(current_close - bullish_ob_price) / current_close < 0.002:
            signal = "BULLISH"
            score = 92.0
            reason = f"Price is reacting directly off a Institutional Bullish Order Block level ({bullish_ob_price:.5f})."
        elif bearish_ob_price and abs(current_close - bearish_ob_price) / current_close < 0.002:
            signal = "BEARISH"
            score = 92.0
            reason = f"Price is reacting directly off a Institutional Bearish Order Block level ({bearish_ob_price:.5f})."
        else:
            signal = "NEUTRAL"
            score = 50.0
            reason = "No immediate Order Block reaction detected on current candle."

        return IndicatorOutput(
            module_id=self.module_id, name=self.name, category=self.category,
            signal=signal, score=score, weight=1.5,
            metrics={"bullish_ob": bullish_ob_price, "bearish_ob": bearish_ob_price},
            reasoning_fragment=reason
        )

class SMCFairValueGapModule(BaseStrategyModule):
    @property
    def module_id(self) -> str:
        return "smc_fair_value_gap"

    @property
    def name(self) -> str:
        return "Smart Money Concepts (SMC) Fair Value Gap (FVG) Imbalance"

    @property
    def category(self) -> str:
        return "smc_ict"

    def calculate(self, candles_df: pd.DataFrame, config: Dict[str, Any] = None) -> IndicatorOutput:
        if len(candles_df) < 5:
            return IndicatorOutput(
                module_id=self.module_id, name=self.name, category=self.category,
                signal="NEUTRAL", score=50.0, weight=1.0, metrics={}, reasoning_fragment="Insufficient FVG data."
            )

        c1 = candles_df.iloc[-3]
        c2 = candles_df.iloc[-2]
        c3 = candles_df.iloc[-1]

        # Bullish FVG: Low of candle 3 is greater than High of candle 1
        bullish_fvg = c3['low'] > c1['high']
        # Bearish FVG: High of candle 3 is less than Low of candle 1
        bearish_fvg = c3['high'] < c1['low']

        if bullish_fvg:
            fvg_size = round(c3['low'] - c1['high'], 5)
            signal = "BULLISH"
            score = 88.0
            reason = f"Active Bullish 3-Bar Fair Value Gap (FVG) Imbalance created (Gap size: {fvg_size})."
        elif bearish_fvg:
            fvg_size = round(c1['low'] - c3['high'], 5)
            signal = "BEARISH"
            score = 88.0
            reason = f"Active Bearish 3-Bar Fair Value Gap (FVG) Imbalance created (Gap size: {fvg_size})."
        else:
            signal = "NEUTRAL"
            score = 50.0
            reason = "No active Fair Value Gap (FVG) imbalance on recent 3 candles."

        return IndicatorOutput(
            module_id=self.module_id, name=self.name, category=self.category,
            signal=signal, score=score, weight=1.4,
            metrics={"bullish_fvg": bullish_fvg, "bearish_fvg": bearish_fvg},
            reasoning_fragment=reason
        )
