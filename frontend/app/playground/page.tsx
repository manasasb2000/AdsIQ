"use client";

import { useState } from "react";
import { Code2, Copy, Check, Terminal } from "lucide-react";
import { codegenApi } from "@/lib/api";

export default function PlaygroundPage() {
  const [language, setLanguage] = useState("python");
  const [action, setAction] = useState("create_campaign");
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleGenerateCode = async () => {
    setLoading(true);
    try {
      const res = await codegenApi.generate({ action, language });
      setCode(res.data.code_snippet);
    } catch (err) {
      console.error("Codegen error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (code) {
      navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="space-y-8">
      
      <div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
          <Code2 className="w-7 h-7 text-blue-400" />
          Google Ads API Code Playground
        </h1>
        <p className="text-slate-400 text-sm">
          Generate executable client library snippets across Python and Node.js for common Google Ads API integration tasks.
        </p>
      </div>

      <div className="glass-card p-6 rounded-2xl space-y-6">
        
        <div className="flex flex-wrap items-center justify-between gap-4">
          
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5 p-1 rounded-xl bg-slate-900 border border-slate-800 text-xs">
              <button
                onClick={() => setLanguage("python")}
                className={`px-3 py-1.5 rounded-lg font-semibold capitalize ${
                  language === "python" ? "bg-blue-600 text-white" : "text-slate-400 hover:text-white"
                }`}
              >
                Python SDK
              </button>
              <button
                onClick={() => setLanguage("javascript")}
                className={`px-3 py-1.5 rounded-lg font-semibold capitalize ${
                  language === "javascript" ? "bg-blue-600 text-white" : "text-slate-400 hover:text-white"
                }`}
              >
                Node.js Client
              </button>
            </div>
          </div>

          <button
            onClick={handleGenerateCode}
            disabled={loading}
            className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold shadow-lg shadow-blue-500/20"
          >
            {loading ? "Generating Snippet..." : "Generate Code Snippet"}
          </button>

        </div>

        {/* Code Output Window */}
        <div className="rounded-xl bg-slate-950 border border-slate-800 overflow-hidden">
          <div className="px-4 py-2 bg-slate-900/80 border-b border-slate-800 flex items-center justify-between text-xs text-slate-400 font-mono">
            <div className="flex items-center gap-2">
              <Terminal className="w-3.5 h-3.5 text-blue-400" />
              <span>{language === "python" ? "example_ads_api.py" : "example_ads_api.js"}</span>
            </div>
            {code && (
              <button onClick={handleCopy} className="hover:text-white flex items-center gap-1">
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                {copied ? "Copied" : "Copy"}
              </button>
            )}
          </div>

          <div className="p-4 overflow-x-auto min-h-[300px]">
            {code ? (
              <pre className="text-xs font-mono text-blue-300 leading-relaxed">{code}</pre>
            ) : (
              <div className="text-slate-600 text-xs text-center py-24">
                Click 'Generate Code Snippet' to view client library initialization and reporting code.
              </div>
            )}
          </div>
        </div>

      </div>

    </div>
  );
}
