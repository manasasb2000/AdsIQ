"use client";

import { useState } from "react";
import { MessageSquare, Send, Bot, User, Sparkles, CheckCircle2 } from "lucide-react";
import { agentsApi } from "@/lib/api";

export default function ConsultantPage() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<any[]>([
    {
      role: "assistant",
      content: "Hello! I am your AI Google Ads API Solutions Consultant. How can I assist you today with API integration, error troubleshooting, or campaign strategy?"
    }
  ]);

  const handleSend = async () => {
    if (!prompt.trim()) return;

    const userMsg = { role: "user", content: prompt };
    setMessages((prev) => [...prev, userMsg]);
    const currentPrompt = prompt;
    setPrompt("");
    setLoading(true);

    try {
      const res = await agentsApi.run({
        agent_type: "CONSULTANT",
        prompt: currentPrompt
      });

      const advice = res.data.output_data?.consultant_result?.advice || "I evaluated your inquiry. Recommendation: check Google Ads API quotas and ensure OAuth scope permissions.";
      setMessages((prev) => [...prev, { role: "assistant", content: advice }]);
    } catch (err) {
      console.error("Consultant error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      
      <div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
          <MessageSquare className="w-7 h-7 text-blue-400" />
          AI Solutions Consultant Chat
        </h1>
        <p className="text-slate-400 text-sm">
          Simulating the customer-facing technical advisory role of a Google Product Solutions Engineer.
        </p>
      </div>

      {/* Chat Box */}
      <div className="glass-card rounded-2xl border border-slate-800 flex flex-col h-[520px] overflow-hidden">
        
        {/* Messages Scroll Area */}
        <div className="flex-1 p-6 overflow-y-auto space-y-4">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex items-start gap-3 ${msg.role === "user" ? "flex-row-reverse" : ""}`}
            >
              <div
                className={`w-8 h-8 rounded-xl flex items-center justify-center text-xs font-bold ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-gradient-to-tr from-blue-600 to-emerald-400 text-white"
                }`}
              >
                {msg.role === "user" ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
              </div>

              <div
                className={`p-4 rounded-2xl text-xs max-w-xl leading-relaxed ${
                  msg.role === "user"
                    ? "bg-blue-600/20 text-slate-100 border border-blue-500/30 rounded-tr-none"
                    : "bg-slate-900/90 text-slate-200 border border-slate-800 rounded-tl-none whitespace-pre-wrap"
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex items-center gap-2 text-xs text-blue-400 font-mono animate-pulse">
              <Sparkles className="w-4 h-4" />
              <span>Consultant agent thinking...</span>
            </div>
          )}
        </div>

        {/* Input Bar */}
        <div className="p-4 bg-slate-950/80 border-t border-slate-800 flex items-center gap-3">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Ask a technical or strategic Google Ads API question..."
            className="flex-1 p-3 rounded-xl bg-slate-900 border border-slate-800 text-slate-100 text-xs focus:outline-none focus:border-blue-500/50"
          />
          <button
            onClick={handleSend}
            disabled={loading || !prompt.trim()}
            className="p-3 rounded-xl bg-blue-600 hover:bg-blue-700 text-white transition-all disabled:opacity-50"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>

      </div>

    </div>
  );
}
