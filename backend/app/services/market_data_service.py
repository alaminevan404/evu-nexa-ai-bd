import time
import numpy as np
import pandas as pd
from typing import List, Dict, Any

class MarketDataService:
    @staticmethod
    def generate_synthetic_candles(symbol: str, timeframe: str = "1m", limit: int = 100) -> pd.DataFrame:
        """Generates realistic OHLCV price DataFrame for analysis."""
        np.random.seed(int(time.time() // 60) + sum(ord(c) for c in symbol))

        base_price = 1.08500 if "EUR" in symbol else (65000.0 if "BTC" in symbol else 2350.0)
        volatility = 0.0003 if "EUR" in symbol else (150.0 if "BTC" in symbol else 2.5)

        current_time = int(time.time()) - (limit * 60)
        candles = []
        price = base_price

        for i in range(limit):
            change = np.random.normal(0, volatility)
            open_p = price
            close_p = price + change
            high_p = max(open_p, close_p) + abs(np.random.normal(0, volatility * 0.5))
            low_p = min(open_p, close_p) - abs(np.random.normal(0, volatility * 0.5))
            volume = float(np.random.randint(100, 5000))

            candles.append({
                "timestamp": current_time + (i * 60),
                "open": round(open_p, 5),
                "high": round(high_p, 5),
                "low": round(low_p, 5),
                "close": round(close_p, 5),
                "volume": volume
            })
            price = close_p

        df = pd.DataFrame(candles)
        return df

market_data_service = MarketDataService()
