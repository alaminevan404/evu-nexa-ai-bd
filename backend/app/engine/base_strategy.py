from abc import ABC, abstractmethod
from typing import Dict, Any
import pandas as pd
from pydantic import BaseModel

class IndicatorOutput(BaseModel):
    module_id: str
    name: str
    category: str
    signal: str  # BULLISH, BEARISH, NEUTRAL
    score: float  # 0.0 - 100.0
    weight: float = 1.0
    metrics: Dict[str, Any]
    reasoning_fragment: str

class BaseStrategyModule(ABC):
    @property
    @abstractmethod
    def module_id(self) -> str:
        """Unique identifier, e.g. 'ema_crossover'"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human readable name, e.g. 'Exponential Moving Average (EMA) Crossover'"""
        pass

    @property
    @abstractmethod
    def category(self) -> str:
        """Category: trend, momentum, volatility, volume, structure, smc_ict, stats, binary_timing"""
        pass

    @abstractmethod
    def calculate(self, candles_df: pd.DataFrame, config: Dict[str, Any] = None) -> IndicatorOutput:
        """Calculates indicator signal on OHLCV pandas DataFrame."""
        pass
