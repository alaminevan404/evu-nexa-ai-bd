import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { ShieldCheck, Key, AlertCircle, Send, Cpu, Lock } from 'lucide-react';
import { getHardwareFingerprint } from '../../utils/fingerprint';
import { authService } from '../../services/api';
import { useAuthStore } from '../../store/authStore';

export const LicenseActivationForm: React.FC = () => {
  const [licenseKey, setLicenseKey] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const setAuth = useAuthStore((state) => state.setAuth);

  const handleActivate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!licenseKey.trim()) return;

    setLoading(true);
    setErrorMsg(null);

    try {
      const fingerprint = await getHardwareFingerprint();
      const res = await authService.activate({
        license_key: licenseKey.trim(),
        client_fingerprint: fingerprint
      });

      setAuth(res.access_token, res.license_key, res.tier, res.is_admin);
    } catch (err: any) {
      const detail = err.response?.data?.detail || 'Activation failed. Please verify key.';
      if (detail === 'ERR_DEVICE_LIMIT_EXCEEDED') {
        setErrorMsg('Maximum device activation limit reached for this License Key.');
      } else if (detail === 'LICENSE_EXPIRED') {
        setErrorMsg('Your License Key has expired. Please renew subscription.');
      } else {
        setErrorMsg('Invalid License Key. Access denied.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-obsidian-950 p-4 relative overflow-hidden">
      {/* Background Animated Glow Grids */}
      <div className="absolute w-[500px] h-[500px] bg-nexa-cyan/10 rounded-full blur-[120px] -top-40 -left-40 pointer-events-none" />
      <div className="absolute w-[500px] h-[500px] bg-nexa-violet/10 rounded-full blur-[120px] -bottom-40 -right-40 pointer-events-none" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md glass-panel p-8 relative z-10 shadow-2xl border border-glass-border"
      >
        {/* Header Emblem */}
        <div className="flex flex-col items-center mb-8">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-nexa-violet to-nexa-cyan flex items-center justify-center shadow-cyan-glow mb-3">
            <Cpu className="w-9 h-9 text-white" />
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-white font-sans flex items-center gap-2">
            EVU NEXA <span className="text-nexa-cyan">AI</span>
          </h1>
          <p className="text-xs text-gray-400 mt-1 tracking-wider uppercase">
            Binary Option Intelligence Platform v2.4
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleActivate} className="space-y-5">
          <div>
            <label className="block text-xs font-mono uppercase text-gray-300 mb-2">
              Enter License Key
            </label>
            <div className="relative">
              <Key className="absolute left-3.5 top-3.5 w-4 h-4 text-nexa-cyan" />
              <input
                type="text"
                value={licenseKey}
                onChange={(e) => setLicenseKey(e.target.value.toUpperCase())}
                placeholder="NEXA-PRO-XXXX-XXXX"
                className="w-full bg-obsidian-900 border border-obsidian-700 rounded-lg pl-10 pr-4 py-3 text-sm text-white font-mono placeholder-gray-600 focus:outline-none focus:border-nexa-cyan focus:ring-1 focus:ring-nexa-cyan transition-all"
                required
              />
            </div>
          </div>

          {errorMsg && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="p-3.5 bg-nexa-crimson/10 border border-nexa-crimson/30 rounded-lg flex items-start gap-3"
            >
              <AlertCircle className="w-5 h-5 text-nexa-crimson shrink-0 mt-0.5" />
              <div className="text-xs text-red-200 leading-relaxed">
                {errorMsg}
              </div>
            </motion.div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 bg-gradient-to-r from-nexa-cyan to-nexa-violet text-black font-semibold text-sm rounded-lg hover:opacity-90 transition-all flex items-center justify-center gap-2 shadow-cyan-glow disabled:opacity-50"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-black border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <Lock className="w-4 h-4" />
                <span>ACTIVATE TERMINAL</span>
              </>
            )}
          </button>
        </form>

        {/* Telegram Contact Box */}
        <div className="mt-8 pt-6 border-t border-obsidian-800 text-center">
          <p className="text-xs text-gray-400 mb-3">
            Need a License Key or Subscription Renewal?
          </p>
          <a
            href="https://t.me/et_evu"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-4 py-2 bg-obsidian-850 hover:bg-obsidian-800 border border-nexa-cyan/30 hover:border-nexa-cyan text-nexa-cyan text-xs font-medium rounded-lg transition-all"
          >
            <Send className="w-3.5 h-3.5" />
            <span>Contact Support (@et_evu)</span>
          </a>
        </div>
      </motion.div>
    </div>
  );
};
