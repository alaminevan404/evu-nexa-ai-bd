import { create } from 'zustand';

interface AuthState {
  token: string | null;
  licenseKey: string | null;
  tier: string | null;
  isAdmin: boolean;
  isAuthenticated: boolean;
  setAuth: (token: string, licenseKey: string, tier: string, isAdmin: bool) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem('nexa_access_token'),
  licenseKey: localStorage.getItem('nexa_license_key'),
  tier: localStorage.getItem('nexa_tier'),
  isAdmin: localStorage.getItem('nexa_is_admin') === 'true',
  isAuthenticated: !!localStorage.getItem('nexa_access_token'),

  setAuth: (token, licenseKey, tier, isAdmin) => {
    localStorage.setItem('nexa_access_token', token);
    localStorage.setItem('nexa_license_key', licenseKey);
    localStorage.setItem('nexa_tier', tier);
    localStorage.setItem('nexa_is_admin', String(isAdmin));
    set({ token, licenseKey, tier, isAdmin, isAuthenticated: true });
  },

  logout: () => {
    localStorage.removeItem('nexa_access_token');
    localStorage.removeItem('nexa_license_key');
    localStorage.removeItem('nexa_tier');
    localStorage.removeItem('nexa_is_admin');
    set({ token: null, licenseKey: null, tier: null, isAdmin: false, isAuthenticated: false });
  }
}));
