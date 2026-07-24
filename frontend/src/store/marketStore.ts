import { create } from 'zustand';

export interface MarketAsset {
  id: string;
  symbol: string;
  display_name: string;
  category: string;
  is_otc: boolean;
  payout_percentage: number;
}

export interface AnalysisResult {
  id: string;
  asset_symbol: string;
  timeframe: string;
  direction: 'BULLISH_CALL' | 'BEARISH_PUT' | 'NEUTRAL';
  confidence_score: number;
  risk_level: string;
  ai_reasoning: str;
  indicators_used: any[];
  recommended_expiry: string;
}

interface MarketState {
  assets: MarketAsset[];
  selectedSymbol: string;
  selectedTimeframe: string;
  activeAnalysis: AnalysisResult | null;
  isAnalyzing: boolean;
  setAssets: (assets: MarketAsset[]) => void;
  setSelectedSymbol: (symbol: string) => void;
  setSelectedTimeframe: (tf: string) => void;
  setActiveAnalysis: (analysis: AnalysisResult | null) => void;
  setIsAnalyzing: (val: boolean) => void;
}

export const useMarketStore = create<MarketState>((set) => ({
  assets: [],
  selectedSymbol: 'EURUSD_OTC',
  selectedTimeframe: '1m',
  activeAnalysis: null,
  isAnalyzing: false,

  setAssets: (assets) => set({ assets }),
  setSelectedSymbol: (selectedSymbol) => set({ selectedSymbol }),
  setSelectedTimeframe: (selectedTimeframe) => set({ selectedTimeframe }),
  setActiveAnalysis: (activeAnalysis) => set({ activeAnalysis }),
  setIsAnalyzing: (isAnalyzing) => set({ isAnalyzing }),
}));
