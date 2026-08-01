"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { 
  Wrench, 
  Layers, 
  Sparkles, 
  BarChart3, 
  ArrowUpRight, 
  Activity, 
  CheckCircle2, 
  Cpu, 
  TrendingUp, 
  Zap, 
  ShieldCheck,
  AlertCircle
} from "lucide-react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import { analyticsApi } from "@/lib/api";
import { AgentWebSocketClient } from "@/lib/ws";

export default function DashboardPage() {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [agentLogs, setAgentLogs] = useState<any[]>([]);
  const [wsConnected, setWsConnected] = useState(false);

  useEffect(() => {
    // Fetch analytics metrics
    analyticsApi.dashboard()
      .then((res) => {
        setMetrics(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching metrics:", err);
        setLoading(false);
      });

    // Connect to Real-time WebSocket Stream
    const wsClient = new AgentWebSocketClient();
    wsClient.connect((data) => {
      if (data.type === "connection_established") {
        setWsConnected(true);
      }
      if (data.type === "agent_step" || data.type === "agent_complete") {
        setAgentLogs((prev) => [data, ...prev.slice(0, 9)]);
      }
    });

    return () => wsClient.disconnect();
  }, []);

  return (
    <div className="space-y-8">
      
      {/* Hero Welcome Banner */}
      <div className="relative overflow-hidden rounded-2xl glass-card border border-blue-500/20 p-8 bg-gradient-to-r from-slate-900 via-blue-950/40 to-slate-900">
        <div className="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-400 text-xs font-semibold">
              <Zap className="w-3.5 h-3.5 text-yellow-400" />
              Multi-Agent AI Intelligence Engine
            </div>
            <h1 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
              Google Ads API <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">Control Center</span>
            </h1>
            <p className="text-slate-400 text-sm max-w-2xl">
              Automating API error troubleshooting, GAQL reporting, campaign generation, and creative asset compliance for enterprise advertising engineering teams.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <Link
              href="/troubleshoot"
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white text-sm font-semibold shadow-lg shadow-emerald-500/20 transition-all hover:scale-105"
            >
              <Wrench className="w-4 h-4" />
              Troubleshoot Error
            </Link>
            <Link
              href="/campaigns/new"
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold shadow-lg shadow-blue-500/20 transition-all hover:scale-105"
            >
              <Layers className="w-4 h-4" />
              Build Campaign
            </Link>
          </div>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        
        <div className="glass-card glass-card-hover p-5 rounded-2xl space-y-3">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium">
            <span>Total Campaign Spend</span>
            <TrendingUp className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-white">
            ₹{metrics ? (metrics.total_cost_inr).toLocaleString() : "16,37,500"}
          </div>
          <div className="text-xs text-emerald-400 flex items-center gap-1 font-medium">
            <ArrowUpRight className="w-3.5 h-3.5" /> +14.2% vs last week
          </div>
        </div>

        <div className="glass-card glass-card-hover p-5 rounded-2xl space-y-3">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium">
            <span>Account ROAS</span>
            <Zap className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-2xl font-bold text-white">
            {metrics ? `${metrics.average_roas}x` : "4.67x"}
          </div>
          <div className="text-xs text-blue-400 font-medium">
            Target ROAS: 4.00x (Exceeding Goal)
          </div>
        </div>

        <div className="glass-card glass-card-hover p-5 rounded-2xl space-y-3">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium">
            <span>Avg Quality Score</span>
            <ShieldCheck className="w-4 h-4 text-yellow-400" />
          </div>
          <div className="text-2xl font-bold text-white">
            {metrics ? `${metrics.average_quality_score} / 10` : "8.25 / 10"}
          </div>
          <div className="text-xs text-yellow-400 font-medium">
            Top 10% Industry Quality Score
          </div>
        </div>

        <div className="glass-card glass-card-hover p-5 rounded-2xl space-y-3">
          <div className="flex items-center justify-between text-slate-400 text-xs font-medium">
            <span>Active Campaigns</span>
            <Activity className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-bold text-white">
            {metrics ? metrics.active_campaigns : "3"} / {metrics ? metrics.total_campaigns : "4"}
          </div>
          <div className="text-xs text-slate-400 font-medium">
            1 Campaign Paused for Budget Optimization
          </div>
        </div>

      </div>

      {/* Main Content Grid: Chart + Live Agent Stream */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Analytics Chart */}
        <div className="lg:col-span-2 glass-card p-6 rounded-2xl space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-white flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-blue-400" />
                Performance Trends (GAQL Stream)
              </h2>
              <p className="text-xs text-slate-400">Daily Impressions & Clicks from Google Ads Reporting API</p>
            </div>
            <Link href="/analytics" className="text-xs text-blue-400 hover:underline flex items-center gap-1 font-medium">
              Run GAQL Query <ArrowUpRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="h-72 w-full pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={metrics?.chart_series || []}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="date" stroke="#64748b" fontSize={12} />
                <YAxis stroke="#64748b" fontSize={12} />
                <Tooltip 
                  contentStyle={{ backgroundColor: "#0f172a", borderColor: "#1e293b", borderRadius: "12px", color: "#fff" }}
                />
                <Line type="monotone" dataKey="clicks" stroke="#4285F4" strokeWidth={3} dot={{ r: 4 }} name="Clicks" />
                <Line type="monotone" dataKey="conversions" stroke="#34A853" strokeWidth={3} dot={{ r: 4 }} name="Conversions" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Real-Time AI Agent Stream */}
        <div className="glass-card p-6 rounded-2xl space-y-4 flex flex-col justify-between">
          <div className="space-y-3">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <Cpu className="w-5 h-5 text-emerald-400" />
                <h2 className="text-base font-bold text-white">Live Agent Activity</h2>
              </div>
              <span className="flex items-center gap-1.5 text-xs text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/20 font-medium">
                <span className="w-2 h-2 rounded-full bg-emerald-400 agent-live-indicator"></span>
                {wsConnected ? "WebSocket Live" : "Connecting..."}
              </span>
            </div>

            {/* Log Feed */}
            <div className="space-y-3 max-h-64 overflow-y-auto pr-1 text-xs">
              {agentLogs.length === 0 ? (
                <div className="text-slate-500 text-center py-8 space-y-2">
                  <CheckCircle2 className="w-8 h-8 text-emerald-500/40 mx-auto" />
                  <p>All 6 agents online and ready.</p>
                  <p className="text-[11px] text-slate-600">Trigger an agent from Troubleshooter or Consultant to stream steps live.</p>
                </div>
              ) : (
                agentLogs.map((log, idx) => (
                  <div key={idx} className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800 space-y-1">
                    <div className="flex items-center justify-between text-[11px] font-semibold text-blue-400">
                      <span>{log.step || "AGENT_STEP"}</span>
                      <span className="text-slate-500">Just now</span>
                    </div>
                    <p className="text-slate-300 text-[11px]">{log.message}</p>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="pt-3 border-t border-slate-800">
            <Link
              href="/consultant"
              className="w-full py-2 px-3 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs font-semibold flex items-center justify-center gap-2 border border-slate-800 transition-colors"
            >
              Open AI Solutions Consultant Chat
            </Link>
          </div>

        </div>

      </div>

    </div>
  );
}
