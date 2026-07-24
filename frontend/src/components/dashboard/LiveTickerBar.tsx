import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

const TICKERS = [
  { symbol: 'EUR/USD (OTC)', price: '1.08420', change: '+0.15%', isUp: true },
  { symbol: 'GBP/JPY', price: '202.450', change: '-0.22%', isUp: false },
  { symbol: 'BTC/USDT', price: '67,420.50', change: '+2.40%', isUp: true },
  { symbol: 'ETH/USDT', price: '3,540.10', change: '+1.80%', isUp: true },
  { symbol: 'AUD/CAD', price: '0.91230', change: '-0.08%', isUp: false },
  { symbol: 'Gold (XAU)', price: '2,385.40', change: '+0.45%', isUp: true },
];

export const LiveTickerBar: React.FC = () => {
  return (
    <div className="h-9 bg-obsidian-950 border-b border-obsidian-850 px-4 flex items-center overflow-hidden text-xs font-mono text-gray-300">
      <div className="flex items-center gap-8 animate-pulse">
        {TICKERS.map((t, idx) => (
          <div key={idx} className="flex items-center gap-2">
            <span className="text-gray-400 font-semibold">{t.symbol}</span>
            <span className="text-white">{t.price}</span>
            <span className={`flex items-center gap-0.5 font-medium ${t.isUp ? 'text-nexa-emerald' : 'text-nexa-crimson'}`}>
              {t.isUp ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
              {t.change}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
