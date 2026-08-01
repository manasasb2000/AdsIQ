import "./globals.css";
import Navbar from "@/components/Navbar";

export const metadata = {
  title: "AdsIQ — Google Ads API Intelligence Platform",
  description: "AI-powered multi-agent system built for the Google Product Solutions Engineer Ads API role.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-slate-950 text-slate-100 min-h-screen flex flex-col antialiased selection:bg-blue-500 selection:text-white">
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
        <footer className="border-t border-slate-900 bg-slate-950/50 py-6 text-center text-xs text-slate-500">
          <p>© 2026 AdsIQ Platform — Designed for Google Product Solutions Engineer, Ads API Role</p>
        </footer>
      </body>
    </html>
  );
}
