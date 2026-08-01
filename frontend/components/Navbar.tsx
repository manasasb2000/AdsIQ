"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  Wrench, 
  Layers, 
  Sparkles, 
  BarChart3, 
  Code2, 
  MessageSquare, 
  Bot,
  Activity
} from "lucide-react";

export default function Navbar() {
  const pathname = usePathname();

  const navItems = [
    { name: "Dashboard", href: "/", icon: Activity },
    { name: "API Troubleshooter", href: "/troubleshoot", icon: Wrench, highlight: true },
    { name: "Campaigns", href: "/campaigns", icon: Layers },
    { name: "Creative Studio", href: "/creative", icon: Sparkles },
    { name: "Analytics & GAQL", href: "/analytics", icon: BarChart3 },
    { name: "Code Playground", href: "/playground", icon: Code2 },
    { name: "AI Consultant", href: "/consultant", icon: MessageSquare },
  ];

  return (
    <header className="sticky top-0 z-50 glass-card border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo & Google PSE Badge */}
          <div className="flex items-center gap-3">
            <Link href="/" className="flex items-center gap-2 group">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-500 to-emerald-400 p-[2px]">
                <div className="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
                  <Bot className="w-5 h-5 text-blue-400 group-hover:scale-110 transition-transform" />
                </div>
              </div>
              <div className="flex flex-col">
                <span className="text-xl font-bold tracking-tight text-white flex items-center gap-1.5">
                  Ads<span className="text-blue-400">IQ</span>
                </span>
                <span className="text-[10px] text-slate-400 font-medium tracking-wider uppercase">
                  Google Ads API Engine
                </span>
              </div>
            </Link>

            <div className="hidden md:flex items-center gap-2 ml-4 px-2.5 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-300 text-xs font-medium">
              <span className="w-2 h-2 rounded-full bg-emerald-400 agent-live-indicator"></span>
              Product Solutions Engineer Edition
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden lg:flex items-center gap-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    isActive
                      ? "bg-blue-600/20 text-blue-400 border border-blue-500/30"
                      : "text-slate-300 hover:text-white hover:bg-slate-800/50"
                  } ${item.highlight ? "border border-emerald-500/30 text-emerald-400 bg-emerald-500/10" : ""}`}
                >
                  <Icon className={`w-4 h-4 ${item.highlight ? "text-emerald-400" : ""}`} />
                  {item.name}
                </Link>
              );
            })}
          </nav>

          {/* Status Indicator */}
          <div className="flex items-center gap-3">
            <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-xs text-slate-300">
              <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
              FastAPI: <span className="text-emerald-400 font-mono">Port 8000</span>
            </div>
          </div>

        </div>
      </div>
    </header>
  );
}
