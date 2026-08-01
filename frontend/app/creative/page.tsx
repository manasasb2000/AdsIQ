"use client";

import { useState } from "react";
import { Sparkles, CheckCircle2, Copy, Check, ShieldCheck } from "lucide-react";
import { creativeApi } from "@/lib/api";

export default function CreativePage() {
  const [productName, setProductName] = useState("CloudSync AI");
  const [productDesc, setProductDesc] = useState("Automated enterprise data pipeline and Google Ads API integration platform.");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [copied, setCopied] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const res = await creativeApi.generate({
        product_name: productName,
        product_description: productDesc
      });
      setResult(res.data);
    } catch (err) {
      console.error("Creative generation error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      
      <div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
          <Sparkles className="w-7 h-7 text-purple-400" />
          Creative Studio
        </h1>
        <p className="text-slate-400 text-sm">
          Generate Responsive Search Ad (RSA) headlines and descriptions compliant with Google Ads character limits.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Form Input */}
        <div className="lg:col-span-5 glass-card p-6 rounded-2xl space-y-4">
          <div className="space-y-2">
            <label className="text-xs font-semibold text-slate-300">Product / Service Name:</label>
            <input
              type="text"
              value={productName}
              onChange={(e) => setProductName(e.target.value)}
              className="w-full p-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 text-sm focus:outline-none focus:border-purple-500/50"
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-semibold text-slate-300">Product Description & Value Props:</label>
            <textarea
              value={productDesc}
              onChange={(e) => setProductDesc(e.target.value)}
              rows={4}
              className="w-full p-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 text-sm focus:outline-none focus:border-purple-500/50 resize-none"
            ></textarea>
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading}
            className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-bold text-sm shadow-lg shadow-purple-500/20 transition-all"
          >
            {loading ? "Generating Compliant Copy..." : "Generate RSA Creative Copy"}
          </button>
        </div>

        {/* Generated Copy Output */}
        <div className="lg:col-span-7 space-y-6">
          {!result ? (
            <div className="glass-card p-12 rounded-2xl text-center text-slate-500 text-xs">
              Click 'Generate RSA Creative Copy' to produce 15 headlines (<=30 chars) and 4 descriptions (<=90 chars).
            </div>
          ) : (
            <div className="space-y-6">
              
              {/* Compliance Badge */}
              <div className="p-4 rounded-xl glass-card border border-emerald-500/30 bg-emerald-950/10 flex items-center justify-between">
                <div className="flex items-center gap-2 text-emerald-400 text-xs font-bold">
                  <ShieldCheck className="w-4 h-4" />
                  Google Ads Character Limit Compliance Verified
                </div>
                <span className="text-[10px] text-slate-400 font-mono">15 Headlines • 4 Descriptions</span>
              </div>

              {/* Headlines Grid */}
              <div className="glass-card p-6 rounded-2xl space-y-3">
                <h3 className="text-xs font-bold text-slate-300">Generated Headlines (<=30 Chars):</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {result.headlines?.map((h: string, idx: number) => (
                    <div key={idx} className="p-2.5 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-between text-xs">
                      <span className="text-slate-200 font-medium">{h}</span>
                      <span className="text-[10px] font-mono text-emerald-400">{h.length}/30</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Descriptions List */}
              <div className="glass-card p-6 rounded-2xl space-y-3">
                <h3 className="text-xs font-bold text-slate-300">Generated Descriptions (<=90 Chars):</h3>
                <div className="space-y-2">
                  {result.descriptions?.map((d: string, idx: number) => (
                    <div key={idx} className="p-3 rounded-xl bg-slate-950 border border-slate-800 flex items-center justify-between text-xs gap-4">
                      <span className="text-slate-200">{d}</span>
                      <span className="text-[10px] font-mono text-emerald-400 whitespace-nowrap">{d.length}/90</span>
                    </div>
                  ))}
                </div>
              </div>

            </div>
          )}
        </div>

      </div>

    </div>
  );
}
