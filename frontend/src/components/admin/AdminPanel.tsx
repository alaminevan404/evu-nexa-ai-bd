import React, { useState, useEffect } from 'react';
import { adminService } from '../../services/api';
import { ShieldCheck, Plus, Key, X, Users, RefreshCw } from 'lucide-react';

interface AdminPanelProps {
  onClose: () => void;
}

export const AdminPanel: React.FC<AdminPanelProps> = ({ onClose }) => {
  const [licenses, setLicenses] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [ownerName, setOwnerName] = useState('');
  const [ownerContact, setOwnerContact] = useState('');
  const [durationDays, setDurationDays] = useState(30);

  const fetchLicenses = async () => {
    setLoading(true);
    try {
      const data = await adminService.getLicenses();
      setLicenses(data);
    } catch (err) {
      console.error('Failed to fetch admin licenses:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLicenses();
  }, []);

  const handleCreateLicense = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await adminService.createLicense({
        owner_name: ownerName,
        owner_contact: ownerContact,
        tier: 'PRO',
        duration_days: durationDays,
        max_devices: 2
      });
      setShowModal(false);
      setOwnerName('');
      setOwnerContact('');
      fetchLicenses();
    } catch (err) {
      alert('Failed to generate license.');
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-md flex items-center justify-center p-6">
      <div className="w-full max-w-5xl bg-obsidian-900 border border-obsidian-700 rounded-2xl shadow-2xl flex flex-col max-h-[85vh] overflow-hidden">
        {/* Header */}
        <div className="p-6 border-b border-obsidian-800 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <ShieldCheck className="w-6 h-6 text-nexa-cyan" />
            <h2 className="text-xl font-bold text-white font-sans">
              EVU NEXA AI - Master Admin Panel
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-white rounded-lg hover:bg-obsidian-800"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Action Bar */}
        <div className="p-4 bg-obsidian-950 border-b border-obsidian-850 flex items-center justify-between">
          <div className="flex items-center gap-2 text-xs font-mono text-gray-400">
            <Users className="w-4 h-4 text-nexa-cyan" />
            <span>Total Issued Keys: <strong className="text-white">{licenses.length}</strong></span>
          </div>
          <button
            onClick={() => setShowModal(true)}
            className="px-4 py-2 bg-nexa-cyan text-black font-semibold text-xs rounded-lg hover:opacity-90 transition-all flex items-center gap-2"
          >
            <Plus className="w-4 h-4" />
            <span>Generate New License</span>
          </button>
        </div>

        {/* License Table */}
        <div className="flex-1 overflow-y-auto p-4">
          {loading ? (
            <div className="flex justify-center p-12">
              <RefreshCw className="w-6 h-6 text-nexa-cyan animate-spin" />
            </div>
          ) : (
            <table className="w-full text-left text-xs font-mono text-gray-300">
              <thead className="bg-obsidian-850 text-gray-400 uppercase text-[10px]">
                <tr>
                  <th className="p-3">License Key</th>
                  <th className="p-3">Owner</th>
                  <th className="p-3">Tier</th>
                  <th className="p-3">Status</th>
                  <th className="p-3">Expires At</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-obsidian-800">
                {licenses.map((lic) => (
                  <tr key={lic.id} className="hover:bg-obsidian-850/50">
                    <td className="p-3 font-bold text-nexa-cyan">{lic.license_key}</td>
                    <td className="p-3 text-white">{lic.owner_name || 'N/A'}</td>
                    <td className="p-3">{lic.tier}</td>
                    <td className="p-3">
                      <span className="px-2 py-0.5 bg-nexa-emerald/20 text-nexa-emerald rounded font-bold">
                        {lic.status}
                      </span>
                    </td>
                    <td className="p-3 text-gray-400">
                      {new Date(lic.expires_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Modal Generator */}
      {showModal && (
        <div className="fixed inset-0 z-60 bg-black/70 flex items-center justify-center p-4">
          <div className="w-full max-w-md bg-obsidian-900 border border-glass-border rounded-xl p-6 shadow-2xl">
            <h3 className="text-base font-bold text-white mb-4">Generate License Key</h3>
            <form onSubmit={handleCreateLicense} className="space-y-4 text-xs font-mono">
              <div>
                <label className="block text-gray-400 mb-1">Owner Name</label>
                <input
                  type="text"
                  required
                  value={ownerName}
                  onChange={(e) => setOwnerName(e.target.value)}
                  className="w-full bg-obsidian-950 border border-obsidian-700 rounded p-2 text-white"
                />
              </div>
              <div>
                <label className="block text-gray-400 mb-1">Telegram / Contact</label>
                <input
                  type="text"
                  required
                  value={ownerContact}
                  onChange={(e) => setOwnerContact(e.target.value)}
                  className="w-full bg-obsidian-950 border border-obsidian-700 rounded p-2 text-white"
                />
              </div>
              <div>
                <label className="block text-gray-400 mb-1">Duration (Days)</label>
                <input
                  type="number"
                  value={durationDays}
                  onChange={(e) => setDurationDays(Number(e.target.value))}
                  className="w-full bg-obsidian-950 border border-obsidian-700 rounded p-2 text-white"
                />
              </div>
              <div className="flex gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="flex-1 py-2 bg-obsidian-800 text-gray-300 rounded hover:bg-obsidian-700"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 py-2 bg-nexa-cyan text-black font-bold rounded hover:opacity-90"
                >
                  Generate
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
