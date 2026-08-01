"use client";

import { useState } from "react";
import { BarChart3, Play, Code2, Clock, FileJson } from "lucide-react";
import { analyticsApi } from "@/lib/api";

const PRESET_QUERIES = [
  {
    label: "Campaign Clicks & Cost",
    query: "SELECT campaign.id, campaign.name, campaign.status, metrics.clicks, metrics.impressions, metrics.cost_micros FROM campaign WHERE campaign.status = 'ENABLED' ORDER BY metrics.clicks DESC"
  },
  {
    label: "Quality Score & CTR Analysis",
    query: "SELECT campaign.name, metrics.ctr, metrics.historical_quality_score, metrics.conversions FROM campaign ORDER BY metrics.historical_quality_score DESC"
  },
  {
    label: "Bidding Strategy Audit",
    query: "SELECT campaign.id, campaign.name, campaign.advertising_channel_type, campaign.bidding_strategy_type FROM campaign"
  }
];

export default function AnalyticsPage() {
  const [query, setQuery] = useState(PRESET_QUERIES[0].query);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);

  const handleRunGAQL = async () => {
    setLoading(true);
    try {
      const res = await analyticsApi.gaql(query);
      setResults(res.data);
    } catch (err) {
      console.error("GAQL error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      
      <div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
          <BarChart3 className="w-7 h-7 text-blue-400" />
          Analytics & GAQL Query Console
        </h1>
        <p className="text-slate-400 text-sm">
          Run raw Google Ads Query Language (GAQL) reporting queries against the simulated performance dataset.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* GAQL Query Input */}
        <div className="lg:col-span-5 space-y-4">
          <div className="glass-card p-6 rounded-2xl space-y-4">
            <h2 className="text-xs font-bold text-slate-300">Preset Sample GAQL Queries:</h2>
            <div className="space-y-2">
              {PRESET_QUERIES.map((preset, idx) => (
                <button
                  key={idx}
                  onClick={() => setQuery(preset.query)}
                  className="w-full text-left p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-xs hover:border-blue-500/40 transition-colors"
                >
                  <span className="font-bold text-white block">{preset.label}</span>
                </button>
              ))}
            </div>

            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-300">Edit GAQL Query Statement:</label>
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                rows={6}
                className="w-full p-3 rounded-xl bg-slate-950 border border-slate-800 text-blue-300 text-xs font-mono focus:outline-none focus:border-blue-500/50 resize-none leading-relaxed"
              ></textarea>
            </div>

            <button
              onClick={handleRunGAQL}
              disabled={loading}
              className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold text-sm shadow-lg shadow-blue-500/20 transition-all flex items-center justify-center gap-2"
            >
              <Play className="w-4 h-4" />
              {loading ? "Executing GAQL..." : "Execute GAQL Query"}
            </button>
          </div>
        </div>

        {/* Results Output */}
        <div className="lg:col-span-7 space-y-6">
          {!results ? (
            <div className="glass-card p-12 rounded-2xl text-center text-slate-500 text-xs">
              Click 'Execute GAQL Query' to run reporting statements and inspect raw API rows.
            </div>
          ) : (
            <div className="glass-card p-6 rounded-2xl space-y-4 border border-blue-500/30">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <span className="text-xs font-mono text-emerald-400">
                  {results.row_count} Rows Returned ({results.execution_time_ms} ms)
                </span>
                <span className="text-xs text-slate-500 font-mono">Simulated GoogleAdsService.search</span>
              </div>

              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 overflow-x-auto max-h-96">
                <pre className="text-xs font-mono text-slate-200">
                  {JSON.stringify(results.results, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </div>

      </div>

    </div>
  );
}
