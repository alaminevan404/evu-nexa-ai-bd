import React, { useState, useEffect } from 'react';
import { Search, Star, Zap } from 'lucide-react';
import { marketService } from '../../services/api';
import { useMarketStore, MarketAsset } from '../../store/marketStore';

export const MarketSearch: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [activeTab, setActiveTab] = useState('ALL');
  const { assets, setAssets, selectedSymbol, setSelectedSymbol } = useMarketStore();

  useEffect(() => {
    const fetchAssets = async () => {
      try {
        const data = await marketService.getAssets(activeTab);
        setAssets(data);
      } catch (err) {
        console.error('Failed to load assets:', err);
      }
    };
    fetchAssets();
  }, [activeTab]);

  const filtered = assets.filter(
    (a) =>
      a.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
      a.display_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="w-80 bg-obsidian-900 border-r border-obsidian-800 flex flex-col shrink-0">
      {/* Search Header */}
      <div className="p-4 border-b border-obsidian-800">
        <div className="relative mb-3">
          <Search className="absolute left-3 top-3 w-4 h-4 text-gray-500" />
          <input
            type="text"
            placeholder="Search Assets... (/)"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-obsidian-950 border border-obsidian-700 rounded-lg pl-9 pr-3 py-2 text-xs text-white placeholder-gray-500 focus:outline-none focus:border-nexa-cyan transition-all font-mono"
          />
        </div>

        {/* Category Tabs */}
        <div className="flex gap-1 overflow-x-auto pb-1 no-scrollbar text-[11px] font-mono">
          {['ALL', 'FOREX', 'CRYPTO', 'OTC'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-3 py-1 rounded-md transition-all whitespace-nowrap ${
                activeTab === tab
                  ? 'bg-nexa-cyan/20 text-nexa-cyan font-semibold border border-nexa-cyan/40'
                  : 'text-gray-400 hover:text-white hover:bg-obsidian-800'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {/* Asset List */}
      <div className="flex-1 overflow-y-auto p-2 space-y-1">
        {filtered.map((asset) => {
          const isSelected = selectedSymbol === asset.symbol;
          return (
            <div
              key={asset.id}
              onClick={() => setSelectedSymbol(asset.symbol)}
              className={`p-3 rounded-lg cursor-pointer transition-all flex items-center justify-between border ${
                isSelected
                  ? 'bg-nexa-cyan/10 border-nexa-cyan/50 shadow-cyan-glow'
                  : 'bg-obsidian-850/50 hover:bg-obsidian-850 border-transparent hover:border-obsidian-700'
              }`}
            >
              <div>
                <div className="flex items-center gap-1.5 font-semibold text-xs text-white">
                  <span>{asset.display_name}</span>
                  {asset.is_otc && (
                    <span className="px-1.5 py-0.5 bg-nexa-violet/20 border border-nexa-violet/40 text-nexa-violet text-[9px] rounded font-mono font-bold">
                      OTC
                    </span>
                  )}
                </div>
                <div className="text-[10px] font-mono text-gray-400 mt-0.5">
                  Payout: <span className="text-nexa-emerald font-semibold">{asset.payout_percentage}%</span>
                </div>
              </div>

              <Star className="w-3.5 h-3.5 text-gray-600 hover:text-nexa-amber transition-colors" />
            </div>
          );
        })}
      </div>
    </div>
  );
};
