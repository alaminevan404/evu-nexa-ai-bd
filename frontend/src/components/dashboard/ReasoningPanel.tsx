import React from 'react';
import { ConfidenceGauge } from './ConfidenceGauge';
import { AnalysisResult } from '../../store/marketStore';
import { ArrowUpRight, ArrowDownRight, Clock, ShieldAlert, Cpu } from 'lucide-react';

interface ReasoningPanelProps {
  analysis: AnalysisResult | null;
  isAnalyzing: boolean;
}

export const ReasoningPanel: React.FC<ReasoningPanelProps> = ({ analysis, isAnalyzing }) => {
  if (isAnalyzing) {
    return (
      <div className="w-96 bg-obsidian-900 border-l border-obsidian-800 p-6 flex flex-col items-center justify-center text-center shrink-0">
        <div className="w-12 h-12 border-4 border-nexa-cyan border-t-transparent rounded-full animate-spin mb-4" />
        <div className="text-sm font-semibold text-white font-mono animate-pulse">
          RUNNING 200+ AI STRATEGY MODULES...
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Evaluating SMC Order Blocks, FVG Imbalances, and Momentum Confluence.
        </p>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="w-96 bg-obsidian-900 border-l border-obsidian-800 p-6 flex flex-col items-center justify-center text-center shrink-0">
        <Cpu className="w-12 h-12 text-gray-700 mb-3" />
        <div className="text-sm font-semibold text-gray-400">READY FOR ANALYSIS</div>
        <p className="text-xs text-gray-600 mt-1">
          Select asset and timeframe, then click "RUN AI MULTI-FACTOR ANALYSIS".
        </p>
      </div>
    );
  }

  const isBullish = analysis.direction === 'BULLISH_CALL';
  const isBearish = analysis.direction === 'BEARISH_PUT';

  return (
    <div className="w-96 bg-obsidian-900 border-l border-obsidian-800 flex flex-col overflow-y-auto shrink-0 p-5 space-y-5">
      {/* Directional Header Card */}
      <div
        className={`p-4 rounded-xl border flex items-center justify-between shadow-lg ${
          isBullish
            ? 'bg-nexa-emerald/10 border-nexa-emerald/40 shadow-bullish-glow'
            : isBearish
            ? 'bg-nexa-crimson/10 border-nexa-crimson/40 shadow-bearish-glow'
            : 'bg-nexa-amber/10 border-nexa-amber/40'
        }`}
      >
        <div>
          <div className="text-[10px] font-mono text-gray-400 tracking-wider uppercase">
            AI SIGNAL OUTLOOK
          </div>
          <div
            className={`text-xl font-bold font-mono mt-0.5 ${
              isBullish ? 'text-nexa-emerald' : isBearish ? 'text-nexa-crimson' : 'text-nexa-amber'
            }`}
          >
            {analysis.direction.replace('_', ' ')}
          </div>
        </div>
        {isBullish ? (
          <ArrowUpRight className="w-8 h-8 text-nexa-emerald" />
        ) : isBearish ? (
          <ArrowDownRight className="w-8 h-8 text-nexa-crimson" />
        ) : (
          <ShieldAlert className="w-8 h-8 text-nexa-amber" />
        )}
      </div>

      {/* Confidence SVG Gauge */}
      <div className="glass-panel">
        <ConfidenceGauge score={analysis.confidence_score} direction={analysis.direction} />
      </div>

      {/* Meta Badges */}
      <div className="grid grid-cols-2 gap-3">
        <div className="bg-obsidian-850 p-3 rounded-lg border border-obsidian-700">
          <div className="text-[10px] font-mono text-gray-400">RECOMMENDED EXPIRY</div>
          <div className="text-xs font-bold text-white font-mono mt-1 flex items-center gap-1.5">
            <Clock className="w-3.5 h-3.5 text-nexa-cyan" />
            {analysis.recommended_expiry}
          </div>
        </div>
        <div className="bg-obsidian-850 p-3 rounded-lg border border-obsidian-700">
          <div className="text-[10px] font-mono text-gray-400">RISK LEVEL</div>
          <div className="text-xs font-bold text-nexa-emerald font-mono mt-1">
            {analysis.risk_level} RISK
          </div>
        </div>
      </div>

      {/* AI Reasoning Console */}
      <div className="glass-panel p-4">
        <div className="text-xs font-mono font-semibold text-nexa-cyan uppercase mb-2 flex items-center gap-1.5">
          <Cpu className="w-3.5 h-3.5" />
          AI Reasoning Breakdown
        </div>
        <p className="text-xs text-gray-300 leading-relaxed font-sans whitespace-pre-line">
          {analysis.ai_reasoning}
        </p>
      </div>
    </div>
  );
};
