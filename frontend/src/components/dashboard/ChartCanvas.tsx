import React, { useEffect, useRef } from 'react';
import { createChart, IChartApi, ISeriesApi } from 'lightweight-charts';
import { marketService } from '../../services/api';

interface ChartCanvasProps {
  symbol: string;
  timeframe: string;
}

export const ChartCanvas: React.FC<ChartCanvasProps> = ({ symbol, timeframe }) => {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const candlestickSeriesRef = useRef<ISeriesApi<"Candlestick"> | null>(null);

  useEffect(() => {
    if (!chartContainerRef.current) return;

    // Initialize Lightweight Chart
    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height: chartContainerRef.current.clientHeight,
      layout: {
        background: { color: '#090D16' },
        textColor: '#9CA3AF',
      },
      grid: {
        vertLines: { color: '#141C2E' },
        horzLines: { color: '#141C2E' },
      },
      crosshair: {
        mode: 1,
      },
      timeScale: {
        borderColor: '#1F2B44',
        timeVisible: true,
        secondsVisible: false,
      },
    });

    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#00E676',
      downColor: '#FF1744',
      borderVisible: false,
      wickUpColor: '#00E676',
      wickDownColor: '#FF1744',
    });

    chartRef.current = chart;
    candlestickSeriesRef.current = candlestickSeries;

    // Load initial candle data
    const loadCandles = async () => {
      try {
        const data = await marketService.getCandles(symbol, timeframe);
        const formatted = data.map((c: any) => ({
          time: c.timestamp,
          open: c.open,
          high: c.high,
          low: c.low,
          close: c.close,
        }));
        candlestickSeries.setData(formatted);
      } catch (err) {
        console.error('Failed to load chart candles:', err);
      }
    };

    loadCandles();

    const handleResize = () => {
      if (chartContainerRef.current && chartRef.current) {
        chartRef.current.applyOptions({
          width: chartContainerRef.current.clientWidth,
          height: chartContainerRef.current.clientHeight,
        });
      }
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [symbol, timeframe]);

  return <div ref={chartContainerRef} className="w-full h-full min-h-[350px]" />;
};
