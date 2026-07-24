import axios from 'axios';

const API_BASE = '/api/v1';

export const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('nexa_access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export interface ActivatePayload {
  license_key: string;
  client_fingerprint: string;
}

export interface RunAnalysisPayload {
  symbol: string;
  timeframe: string;
}

export const authService = {
  activate: async (payload: ActivatePayload) => {
    const res = await api.post('/auth/activate', payload);
    return res.data;
  },
  getMe: async () => {
    const res = await api.get('/auth/me');
    return res.data;
  }
};

export const marketService = {
  getAssets: async (category?: string) => {
    const res = await api.get('/markets/assets', { params: { category } });
    return res.data;
  },
  getCandles: async (symbol: string, timeframe: string) => {
    const res = await api.get('/markets/candles', { params: { symbol, timeframe, limit: 100 } });
    return res.data;
  }
};

export const analysisService = {
  runAnalysis: async (payload: RunAnalysisPayload) => {
    const res = await api.post('/analysis/run', payload);
    return res.data;
  }
};

export const adminService = {
  getLicenses: async () => {
    const res = await api.get('/admin/licenses');
    return res.data;
  },
  createLicense: async (payload: any) => {
    const res = await api.post('/admin/licenses/create', payload);
    return res.data;
  }
};
