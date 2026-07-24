from typing import Dict, List, Type
import pandas as pd
from app.engine.base_strategy import BaseStrategyModule, IndicatorOutput
from app.engine.modules.trend_modules import EMACrossoverModule, ADXStrengthModule
from app.engine.modules.momentum_modules import RSIClassicModule, MACDCrossoverModule
from app.engine.modules.smc_modules import SMCOrderBlockModule, SMCFairValueGapModule

class StrategyRegistry:
    def __init__(self):
        self._modules: Dict[str, BaseStrategyModule] = {}
        self._register_default_modules()

    def _register_default_modules(self):
        modules = [
            EMACrossoverModule(),
            ADXStrengthModule(),
            RSIClassicModule(),
            MACDCrossoverModule(),
            SMCOrderBlockModule(),
            SMCFairValueGapModule()
        ]
        for mod in modules:
            self._modules[mod.module_id] = mod

    def get_all_modules(self) -> List[BaseStrategyModule]:
        return list(self._modules.values())

    def get_module(self, module_id: str) -> BaseStrategyModule:
        return self._modules.get(module_id)

    def execute_all(self, candles_df: pd.DataFrame, enabled_ids: List[str] = None) -> List[IndicatorOutput]:
        outputs = []
        for mod_id, mod in self._modules.items():
            if enabled_ids and mod_id not in enabled_ids:
                continue
            try:
                out = mod.calculate(candles_df)
                outputs.append(out)
            except Exception as e:
                print(f"Error executing module {mod_id}: {e}")
        return outputs

strategy_registry = StrategyRegistry()
