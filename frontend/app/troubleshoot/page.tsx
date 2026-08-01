"use client";

import { useState } from "react";
import { 
  Wrench, 
  CheckCircle2, 
  AlertTriangle, 
  Code2, 
  BookOpen, 
  Copy, 
  Check, 
  Sparkles, 
  ShieldAlert, 
  FileText,
  Search
} from "lucide-react";
import { troubleshootApi } from "@/lib/api";

const COMMON_ERRORS = [
  { code: "AUTHENTICATION_ERROR.OAUTH_TOKEN_EXPIRED", label: "OAuth Token Expired", category: "Auth" },
  { code: "AUTHENTICATION_ERROR.DEVELOPER_TOKEN_NOT_APPROVED", label: "Developer Token Not Approved", category: "Auth" },
  { code: "QUOTA_ERROR.RESOURCE_EXHAUSTED", label: "API Rate Limit Exhausted", category: "Quota" },
  { code: "REQUEST_ERROR.INVALID_FIELD_NAME", label: "Invalid Field Name in GAQL", category: "GAQL" },
  { code: "AD_ERROR.LINE_TOO_LONG", label: "Ad Text Exceeds Character Limit", category: "Ad Copy" },
  { code: "BIDDING_ERRORS.BID_TOO_LOW", label: "Keyword Bid Below Minimum", category: "Bidding" },
  { code: "REQUEST_ERROR.RESOURCE_NOT_FOUND", label: "API Resource Not Found", category: "Resource" }
];

export default function TroubleshootPage() {
  const [selectedErrorCode, setSelectedErrorCode] = useState(COMMON_ERRORS[0].code);
  const [rawLog, setRawLog] = useState("");
  const [language, setLanguage] = useState("python");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [copied, setCopied] = useState(false);

  const handleDiagnose = async () => {
    setLoading(true);
    try {
      const res = await troubleshootApi.diagnose({
        error_code: selectedErrorCode,
        raw_log: rawLog,
        programming_language: language
      });
      setResult(res.data);
    } catch (err) {
      console.error("Diagnosis error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyCode = () => {
    if (result?.code_fix) {
      navigator.clipboard.writeText(result.code_fix);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="space-y-8">
      
      {/* Header */}
      <div className="space-y-2">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold">
          <Wrench className="w-3.5 h-3.5" />
          Flagship Feature — Technical Solutions Tool
        </div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">
          Google Ads API <span className="text-emerald-400">Troubleshooter</span>
        </h1>
        <p className="text-slate-400 text-sm max-w-3xl">
          Diagnose API failures, inspect <code className="text-blue-400 font-mono bg-slate-900 px-1.5 py-0.5 rounded">request_id</code> details, and generate production-ready code fixes across Python, Node.js, Java, and PHP.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Column: Error Selector & Inputs */}
        <div className="lg:col-span-5 space-y-6">
          
          <div className="glass-card p-6 rounded-2xl space-y-5">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <ShieldAlert className="w-5 h-5 text-emerald-400" />
              1. Select or Paste Error
            </h2>

            {/* Quick Selector */}
            <div className="space-y-2">
              <label className="text-xs font-medium text-slate-300">Common Google Ads API Errors:</label>
              <div className="space-y-2 max-h-56 overflow-y-auto pr-1">
                {COMMON_ERRORS.map((err) => (
                  <button
                    key={err.code}
                    onClick={() => {
                      setSelectedErrorCode(err.code);
                      setRawLog("");
                    }}
                    className={`w-full text-left p-3 rounded-xl text-xs font-medium transition-all flex items-center justify-between border ${
                      selectedErrorCode === err.code
                        ? "bg-emerald-500/10 border-emerald-500/40 text-emerald-300"
                        : "bg-slate-900/60 border-slate-800 text-slate-400 hover:bg-slate-800/60 hover:text-slate-200"
                    }`}
                  >
                    <div className="flex flex-col">
                      <span className="font-semibold text-white">{err.label}</span>
                      <span className="font-mono text-[10px] text-slate-500">{err.code}</span>
                    </div>
                    <span className="px-2 py-0.5 rounded bg-slate-800 text-[10px] text-slate-400 border border-slate-700">
                      {err.category}
                    </span>
                  </button>
                ))}
              </div>
            </div>

            {/* Language Selector */}
            <div className="space-y-2">
              <label className="text-xs font-medium text-slate-300">Target Programming Language:</label>
              <div className="grid grid-cols-4 gap-2">
                {["python", "javascript", "java", "php"].map((lang) => (
                  <button
                    key={lang}
                    onClick={() => setLanguage(lang)}
                    className={`py-2 text-xs font-semibold rounded-lg capitalize border transition-all ${
                      language === lang
                        ? "bg-blue-600/20 border-blue-500/50 text-blue-400"
                        : "bg-slate-900 border-slate-800 text-slate-400 hover:bg-slate-800"
                    }`}
                  >
                    {lang}
                  </button>
                ))}
              </div>
            </div>

            {/* Raw Log Input */}
            <div className="space-y-2">
              <label className="text-xs font-medium text-slate-300">Or Paste Raw Log / Stack Trace:</label>
              <textarea
                value={rawLog}
                onChange={(e) => setRawLog(e.target.value)}
                placeholder="Paste JSON GoogleAdsFailure response or stack trace..."
                rows={3}
                className="w-full p-3 rounded-xl bg-slate-950 border border-slate-800 text-slate-200 text-xs font-mono focus:outline-none focus:border-emerald-500/50 resize-none"
              ></textarea>
            </div>

            <button
              onClick={handleDiagnose}
              disabled={loading}
              className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white font-bold text-sm shadow-lg shadow-emerald-500/20 transition-all flex items-center justify-center gap-2"
            >
              {loading ? (
                <span>Diagnosing Error...</span>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  Diagnose with AI Troubleshooter
                </>
              )}
            </button>

          </div>

        </div>

        {/* Right Column: AI Diagnosis & Code Fix Output */}
        <div className="lg:col-span-7 space-y-6">
          
          {!result ? (
            <div className="glass-card p-12 rounded-2xl text-center space-y-4 border border-dashed border-slate-800">
              <Wrench className="w-12 h-12 text-slate-600 mx-auto" />
              <h3 className="text-lg font-bold text-slate-400">Ready to Diagnose API Issues</h3>
              <p className="text-xs text-slate-500 max-w-md mx-auto">
                Select an error code on the left or paste your raw error log to generate official resolutions and code fixes.
              </p>
            </div>
          ) : (
            <div className="space-y-6">
              
              {/* Diagnosis Overview Card */}
              <div className="glass-card p-6 rounded-2xl space-y-4 border border-emerald-500/30 bg-emerald-950/10">
                <div className="flex items-start justify-between gap-4">
                  <div className="space-y-1">
                    <span className="px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                      {result.category} • {result.severity} Severity
                    </span>
                    <h2 className="text-xl font-bold text-white">{result.title}</h2>
                    <p className="text-xs text-slate-400 font-mono">{result.error_code}</p>
                  </div>
                </div>
                <p className="text-sm text-slate-300">{result.description}</p>
              </div>

              {/* Root Causes */}
              <div className="glass-card p-6 rounded-2xl space-y-3">
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-yellow-400" />
                  Root Causes
                </h3>
                <ul className="space-y-2 text-xs text-slate-300">
                  {result.root_causes?.map((cause: string, i: number) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-yellow-400 mt-1.5"></span>
                      <span>{cause}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Code Fix Panel */}
              <div className="glass-card p-6 rounded-2xl space-y-4 border border-blue-500/30">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold text-white flex items-center gap-2">
                    <Code2 className="w-4 h-4 text-blue-400" />
                    Corrected Code Fix ({language.toUpperCase()})
                  </h3>
                  <button
                    onClick={handleCopyCode}
                    className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-xs font-semibold text-slate-300 flex items-center gap-1.5 border border-slate-800 transition-colors"
                  >
                    {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                    {copied ? "Copied!" : "Copy Code"}
                  </button>
                </div>

                <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 overflow-x-auto">
                  <pre className="text-xs font-mono text-blue-300 leading-relaxed">
                    {result.code_fix}
                  </pre>
                </div>
              </div>

              {/* Docs Link */}
              <div className="p-4 rounded-xl glass-card flex items-center justify-between text-xs">
                <div className="flex items-center gap-2 text-slate-300">
                  <BookOpen className="w-4 h-4 text-blue-400" />
                  <span>Official Google Ads API Documentation</span>
                </div>
                <a
                  href={result.docs_url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-blue-400 hover:underline font-semibold"
                >
                  View Docs →
                </a>
              </div>

            </div>
          )}

        </div>

      </div>

    </div>
  );
}
