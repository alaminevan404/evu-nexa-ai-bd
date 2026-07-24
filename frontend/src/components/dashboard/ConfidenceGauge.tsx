import React from 'react';
import { motion } from 'framer-motion';

interface ConfidenceGaugeProps {
  score: number; // 0 to 100
  direction: 'BULLISH_CALL' | 'BEARISH_PUT' | 'NEUTRAL';
}

export const ConfidenceGauge: React.FC<ConfidenceGaugeProps> = ({ score, direction }) => {
  const radius = 60;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  let gaugeColor = '#FFAB00'; // Amber Neutral
  if (direction === 'BULLISH_CALL') gaugeColor = '#00E676';
  if (direction === 'BEARISH_PUT') gaugeColor = '#FF1744';

  return (
    <div className="flex flex-col items-center justify-center p-4 relative">
      <svg className="w-36 h-36 transform -rotate-90">
        <circle
          cx="72"
          cy="72"
          r={radius}
          stroke="#141C2E"
          strokeWidth="10"
          fill="transparent"
        />
        <motion.circle
          cx="72"
          cy="72"
          r={radius}
          stroke={gaugeColor}
          strokeWidth="10"
          fill="transparent"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 1.2, ease: "easeOut" }}
          strokeLinecap="round"
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center text-center pointer-events-none">
        <span className="text-2xl font-bold font-mono text-white">{score.toFixed(1)}%</span>
        <span className="text-[10px] font-mono tracking-widest text-gray-400 uppercase">CONFIDENCE</span>
      </div>
    </div>
  );
};
