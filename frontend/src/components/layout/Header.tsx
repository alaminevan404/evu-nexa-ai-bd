import React from 'react';
import { Cpu, ShieldCheck, LogOut, Settings, User } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';

interface HeaderProps {
  onOpenAdmin: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onOpenAdmin }) => {
  const { licenseKey, tier, isAdmin, logout } = useAuthStore();

  return (
    <header className="h-16 bg-obsidian-900 border-b border-obsidian-800 px-6 flex items-center justify-between shrink-0">
      {/* Brand Logo */}
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-nexa-violet to-nexa-cyan flex items-center justify-center shadow-cyan-glow">
          <Cpu className="w-5 h-5 text-white" />
        </div>
        <div>
          <div className="text-base font-bold tracking-tight text-white flex items-center gap-1.5">
            EVU NEXA <span className="text-nexa-cyan">AI</span>
          </div>
          <div className="text-[10px] font-mono text-gray-400">PRO TERMINAL v2.4</div>
        </div>
      </div>

      {/* Action Indicators */}
      <div className="flex items-center gap-4">
        {/* Tier Badge */}
        <div className="flex items-center gap-2 px-3 py-1.5 bg-obsidian-850 border border-glass-border rounded-lg text-xs font-mono">
          <ShieldCheck className="w-4 h-4 text-nexa-emerald" />
          <span className="text-gray-300">{tier} LICENSE</span>
        </div>

        {/* Admin Panel Button */}
        {isAdmin && (
          <button
            onClick={onOpenAdmin}
            className="px-3.5 py-1.5 bg-nexa-violet/20 hover:bg-nexa-violet/30 border border-nexa-violet/40 text-nexa-violet text-xs font-semibold rounded-lg transition-all flex items-center gap-1.5"
          >
            <Settings className="w-3.5 h-3.5" />
            <span>ADMIN PANEL</span>
          </button>
        )}

        {/* Logout */}
        <button
          onClick={logout}
          className="p-2 text-gray-400 hover:text-red-400 hover:bg-obsidian-800 rounded-lg transition-all"
          title="Logout"
        >
          <LogOut className="w-4 h-4" />
        </button>
      </div>
    </header>
  );
};
