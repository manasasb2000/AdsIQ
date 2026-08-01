"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Sparkles, Layers, CheckCircle2, ArrowRight, Code2 } from "lucide-react";
import { agentsApi, campaignApi } from "@/lib/api";

export default function NewCampaignPage() {
  const router = useRouter();
  const [brief, setBrief] = useState("");
  const [loading, setLoading] = useState(false);
  const [generatedCampaign, setGeneratedCampaign] = useState<any>(null);

  const handleGenerate = async () => {
    if (!brief) return;
    setLoading(true);
    try {
      const res = await agentsApi.run({
        agent_type: "CAMPAIGN_BUILDER",
        prompt: brief
      });
      const data = res.data.output_data?.campaign_builder_result;
      setGeneratedCampaign(data);
    } catch (err) {
      console.error("Campaign builder error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveToAccount = async () => {
    if (!generatedCampaign) return;
    try {
      await campaignApi.create({
        name: generatedCampaign.name,
        campaign_type: generatedCampaign.campaign_type,
        bidding_strategy: generatedCampaign.bidding_strategy,
        daily_budget_micros: generatedCampaign.daily_budget_micros,
        campaign_goal: "LEADS",
        ai_brief: brief
      });
      router.push("/campaigns");
    } catch (err) {
      console.error("Save campaign error:", err);
    }
  };

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      
      <div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
          <Sparkles className="w-7 h-7 text-blue-400" />
          AI Campaign Builder
        </h1>
        <p className="text-slate-400 text-sm">
          Describe your campaign goal in plain English. The Campaign Builder Agent will construct the entire Google Ads object hierarchy.
        </p>
      </div>

      {/* Input Prompt Card */}
      <div className="glass-card p-6 rounded-2xl space-y-4">
        <label className="text-xs font-semibold text-slate-300">Enter Business Brief / Campaign Objective:</label>
        <textarea
          value={brief}
          onChange={(e) => setBrief(e.target.value)}
          placeholder="e.g. Build a Search campaign for a Hyderabad SaaS cloud platform targeting tech professionals with a ₹2,500 daily budget..."
          rows={4}
          className="w-full p-4 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 text-sm focus:outline-none focus:border-blue-500/50 resize-none"
        ></textarea>

        <button
          onClick={handleGenerate}
          disabled={loading || !brief}
          className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold text-sm shadow-lg shadow-blue-500/20 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
        >
          {loading ? "Agent Constructing Hierarchy..." : "Generate Google Ads Campaign Hierarchy"}
        </button>
      </div>

      {/* Generated Campaign Output */}
      {generatedCampaign && (
        <div className="space-y-6">
          
          <div className="glass-card p-6 rounded-2xl space-y-4 border border-emerald-500/30">
            <div className="flex items-center justify-between">
              <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                Structure Generated
              </span>
              <button
                onClick={handleSaveToAccount}
                className="px-4 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white text-xs font-bold flex items-center gap-2 shadow-lg shadow-emerald-500/20"
              >
                Save Campaign to Account <ArrowRight className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-2">
              <h2 className="text-xl font-bold text-white">{generatedCampaign.name}</h2>
              <div className="flex gap-3 text-xs text-slate-400 font-mono">
                <span>Type: {generatedCampaign.campaign_type}</span>
                <span>•</span>
                <span>Bidding: {generatedCampaign.bidding_strategy}</span>
                <span>•</span>
                <span>Daily Budget: ₹{generatedCampaign.daily_budget_inr}</span>
              </div>
            </div>

            {/* Ad Groups Tree */}
            <div className="space-y-3 pt-3 border-t border-slate-800">
              <h3 className="text-xs font-bold text-slate-300">Generated Ad Groups & Keywords:</h3>
              {generatedCampaign.ad_groups?.map((ag: any, idx: number) => (
                <div key={idx} className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-3">
                  <div className="font-bold text-blue-400 text-sm flex items-center gap-2">
                    <Layers className="w-4 h-4" /> {ag.name}
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {ag.keywords?.map((kw: any, kIdx: number) => (
                      <span key={kIdx} className="px-2.5 py-1 rounded bg-slate-900 text-slate-300 text-xs font-mono border border-slate-800">
                        [{kw.match_type}] {kw.text}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>

          </div>

          {/* Generated Python SDK Code */}
          <div className="glass-card p-6 rounded-2xl space-y-3 border border-blue-500/30">
            <h3 className="text-xs font-bold text-white flex items-center gap-2">
              <Code2 className="w-4 h-4 text-blue-400" />
              Python Client Library Executable Snippet
            </h3>
            <pre className="p-4 rounded-xl bg-slate-950 text-blue-300 text-xs font-mono overflow-x-auto">
              {generatedCampaign.python_sdk_code}
            </pre>
          </div>

        </div>
      )}

    </div>
  );
}
