import React, { useState } from 'react';
import { useAuthStore } from './store/authStore';
import { useMarketStore } from './store/marketStore';
import { LicenseActivationForm } from './components/activation/LicenseActivationForm';
import { Header } from './components/layout/Header';
import { LiveTickerBar } from './components/dashboard/LiveTickerBar';
import { MarketSearch } from './components/dashboard/MarketSearch';
import { ChartCanvas } from './components/dashboard/ChartCanvas';
import { ReasoningPanel } from './components/dashboard/ReasoningPanel';
import { AdminPanel } from './components/admin/AdminPanel';
import { analysisService } from './services/api';
import { Zap, Clock, ShieldCheck } from 'lucide-react';

export const App: React.FC = () => {
  const { isAuthenticated } = useAuthStore();
  const {
    selectedSymbol,
    selectedTimeframe,
    setSelectedTimeframe,
    activeAnalysis,
    setActiveAnalysis,
    isAnalyzing,
    setIsAnalyzing
  } = useMarketStore();

  const [showAdmin, setShowAdmin] = useState(false);

  if (!isAuthenticated) {
    return <LicenseActivationForm />;
  }

  const handleRunAnalysis = async () => {
    setIsAnalyzing(true);
    try {
      const result = await analysisService.runAnalysis({
        symbol: selectedSymbol,
        timeframe: selectedTimeframe
      });
      setActiveAnalysis(result);
    } catch (err) {
      console.error('Failed to run AI analysis:', err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="h-screen w-screen flex flex-col bg-obsidian-950 text-gray-100 overflow-hidden font-sans">
      {/* Header */}
      <Header onOpenAdmin={() => setShowAdmin(true)} />

      {/* Live Ticker Bar */}
      <LiveTickerBar />

      {/* Main Workspace Layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Market Search */}
        <MarketSearch />

        {/* Center Workspace */}
        <div className="flex-1 flex flex-col bg-obsidian-950 p-4 space-y-4 overflow-y-auto">
          {/* Active Asset Action Header */}
          <div className="glass-panel p-4 flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-white font-mono flex items-center gap-2">
                {selectedSymbol.replace('_', ' ')}
              </h2>
              <p className="text-xs text-gray-400 font-mono mt-0.5">
                Real-Time Candlestick Feed & SMC Liquidity Heatmap
              </p>
            </div>

            {/* Timeframe Bar */}
            <div className="flex items-center gap-1 bg-obsidian-900 p-1 border border-obsidian-700 rounded-lg text-xs font-mono">
              {['1m', '2m', '3m', '5m', '15m'].map((tf) => (
                <button
                  key={tf}
                  onClick={() => setSelectedTimeframe(tf)}
                  className={`px-3 py-1.5 rounded transition-all ${
                    selectedTimeframe === tf
                      ? 'bg-nexa-cyan text-black font-bold shadow-cyan-glow'
                      : 'text-gray-400 hover:text-white'
                  }`}
                >
                  {tf}
                </button>
              ))}
            </div>

            {/* Run Analysis Action Button */}
            <button
              onClick={handleRunAnalysis}
              disabled={isAnalyzing}
              className="px-6 py-3 bg-gradient-to-r from-nexa-cyan to-nexa-violet text-black font-bold text-xs uppercase tracking-wider rounded-xl hover:opacity-90 transition-all flex items-center gap-2 shadow-cyan-glow disabled:opacity-50"
            >
              <Zap className="w-4 h-4 fill-current" />
              <span>{isAnalyzing ? 'ANALYZING...' : 'RUN AI MULTI-FACTOR ANALYSIS'}</span>
            </button>
          </div>

          {/* Interactive Chart Canvas */}
          <div className="flex-1 glass-panel p-2 overflow-hidden min-h-[350px]">
            <ChartCanvas symbol={selectedSymbol} timeframe={selectedTimeframe} />
          </div>
        </div>

        {/* Right AI Intelligence Panel */}
        <ReasoningPanel analysis={activeAnalysis} isAnalyzing={isAnalyzing} />
      </div>

      {/* Admin Panel Modal */}
      {showAdmin && <AdminPanel onClose={() => setShowAdmin(false)} />}
    </div>
  );
};
