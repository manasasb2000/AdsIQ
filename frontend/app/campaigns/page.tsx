"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Layers, Plus, Search, Tag, Activity, ArrowUpRight, Cpu } from "lucide-react";
import { campaignApi } from "@/lib/api";

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    campaignApi.list()
      .then((res) => {
        setCampaigns(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching campaigns:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="space-y-8">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">Campaign Manager</h1>
          <p className="text-slate-400 text-sm">Manage Google Ads account hierarchy and AI-generated campaign structures.</p>
        </div>

        <Link
          href="/campaigns/new"
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold shadow-lg shadow-blue-500/20 transition-all hover:scale-105 self-start sm:self-auto"
        >
          <Plus className="w-4 h-4" />
          AI Campaign Builder
        </Link>
      </div>

      {/* Campaigns Table / Cards */}
      <div className="glass-card rounded-2xl overflow-hidden border border-slate-800">
        
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs text-slate-400 w-64">
            <Search className="w-3.5 h-3.5" />
            <input type="text" placeholder="Search campaigns..." className="bg-transparent focus:outline-none w-full text-slate-200" />
          </div>
          <span className="text-xs text-slate-500 font-mono">Showing {campaigns.length} Campaigns</span>
        </div>

        {loading ? (
          <div className="p-12 text-center text-slate-500 text-sm">Loading campaigns...</div>
        ) : campaigns.length === 0 ? (
          <div className="p-12 text-center space-y-3">
            <Layers className="w-10 h-10 text-slate-600 mx-auto" />
            <p className="text-slate-400 text-sm">No campaigns found in demo account.</p>
            <Link href="/campaigns/new" className="text-xs text-blue-400 font-semibold hover:underline">
              Build your first campaign with AI →
            </Link>
          </div>
        ) : (
          <div className="divide-y divide-slate-800/60">
            {campaigns.map((c) => (
              <div key={c.id} className="p-5 hover:bg-slate-900/40 transition-colors flex flex-col md:flex-row md:items-center justify-between gap-4">
                
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className={`w-2.5 h-2.5 rounded-full ${c.status === "ENABLED" ? "bg-emerald-400" : "bg-yellow-400"}`}></span>
                    <h3 className="font-bold text-white text-base">{c.name}</h3>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
                      {c.campaign_type}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 font-mono">{c.resource_name || `customers/1234567890/campaigns/${c.id}`}</p>
                </div>

                <div className="flex items-center gap-6 text-xs text-slate-300">
                  <div>
                    <span className="text-slate-500 block text-[10px]">Daily Budget</span>
                    <span className="font-semibold text-white">₹{(c.daily_budget_micros / 1000000).toLocaleString()}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[10px]">Bidding Strategy</span>
                    <span className="font-semibold text-blue-400">{c.bidding_strategy}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[10px]">Optimization Score</span>
                    <span className="font-semibold text-emerald-400">{c.optimization_score || 85}%</span>
                  </div>
                </div>

              </div>
            ))}
          </div>
        )}

      </div>

    </div>
  );
}
