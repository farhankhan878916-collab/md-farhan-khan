import React, { useState } from 'react';
import { API_ENDPOINTS } from '../data/apiDocs';
import { Lock, Unlock, Search, Copy, Check } from 'lucide-react';
import { ApiEndpoint } from '../types';

export const ApiDocsTab: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedMethod, setSelectedMethod] = useState<string>('ALL');
  const [copiedPath, setCopiedPath] = useState<string | null>(null);

  const filtered = API_ENDPOINTS.filter(ep => {
    const matchesMethod = selectedMethod === 'ALL' || ep.method === selectedMethod;
    const matchesSearch =
      ep.path.toLowerCase().includes(searchTerm.toLowerCase()) ||
      ep.summary.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesMethod && matchesSearch;
  });

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedPath(text);
    setTimeout(() => setCopiedPath(null), 2000);
  };

  const getMethodBadgeClass = (method: ApiEndpoint['method']) => {
    switch (method) {
      case 'GET':
        return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
      case 'POST':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'PUT':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      case 'DELETE':
        return 'bg-red-500/10 text-red-400 border-red-500/30';
    }
  };

  return (
    <div className="space-y-6">
      {/* Search & Filters */}
      <div className="flex flex-col sm:flex-row gap-3 items-center justify-between">
        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search endpoints..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg bg-slate-900 border border-slate-800 text-white placeholder-slate-500 focus:outline-none focus:border-red-500"
          />
        </div>

        <div className="flex items-center gap-1.5 w-full sm:w-auto overflow-x-auto">
          {['ALL', 'GET', 'POST', 'PUT', 'DELETE'].map(m => (
            <button
              key={m}
              onClick={() => setSelectedMethod(m)}
              className={`px-3 py-1 text-xs font-mono font-bold rounded-lg border transition ${
                selectedMethod === m
                  ? 'bg-red-600 text-white border-red-500'
                  : 'bg-slate-900 text-slate-400 border-slate-800 hover:text-white'
              }`}
            >
              {m}
            </button>
          ))}
        </div>
      </div>

      {/* Endpoint List */}
      <div className="space-y-3">
        {filtered.map(ep => (
          <div
            key={`${ep.method}-${ep.path}`}
            className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition"
          >
            <div className="flex flex-wrap items-center justify-between gap-2">
              <div className="flex items-center gap-3">
                <span
                  className={`px-2.5 py-0.5 text-xs font-mono font-bold rounded border ${getMethodBadgeClass(
                    ep.method
                  )}`}
                >
                  {ep.method}
                </span>
                <span className="font-mono text-sm font-semibold text-white">{ep.path}</span>
                <button
                  onClick={() => handleCopy(`http://localhost:8080${ep.path}`)}
                  className="text-slate-500 hover:text-slate-300 transition"
                  title="Copy full URL"
                >
                  {copiedPath === `http://localhost:8080${ep.path}` ? (
                    <Check className="w-3.5 h-3.5 text-emerald-400" />
                  ) : (
                    <Copy className="w-3.5 h-3.5" />
                  )}
                </button>
              </div>

              <div className="flex items-center gap-2">
                {ep.authRequired ? (
                  <span className="flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-mono bg-purple-500/10 text-purple-300 border border-purple-500/20">
                    <Lock className="w-3 h-3" />
                    {ep.role ? ep.role : 'JWT Required'}
                  </span>
                ) : (
                  <span className="flex items-center gap-1 px-2 py-0.5 rounded text-[11px] font-mono bg-slate-800 text-slate-400">
                    <Unlock className="w-3 h-3 text-slate-400" /> Public
                  </span>
                )}
              </div>
            </div>

            <p className="text-xs text-slate-300 mt-2">{ep.summary}</p>

            {(ep.requestBody || ep.responseBody) && (
              <div className="mt-3 grid grid-cols-1 md:grid-cols-2 gap-3 pt-3 border-t border-slate-800/60 text-xs">
                {ep.requestBody && (
                  <div>
                    <span className="text-[10px] uppercase font-mono text-slate-500 block mb-1">
                      Request Payload (JSON)
                    </span>
                    <pre className="p-2.5 rounded bg-slate-950 font-mono text-[11px] text-emerald-300 overflow-x-auto border border-slate-850">
                      {ep.requestBody}
                    </pre>
                  </div>
                )}
                {ep.responseBody && (
                  <div>
                    <span className="text-[10px] uppercase font-mono text-slate-500 block mb-1">
                      Response Sample (JSON)
                    </span>
                    <pre className="p-2.5 rounded bg-slate-950 font-mono text-[11px] text-blue-300 overflow-x-auto border border-slate-850">
                      {ep.responseBody}
                    </pre>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
