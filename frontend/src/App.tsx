import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, DollarSign, Users, Award, ShieldCheck, 
  BarChart3, PieChart, Layers, ArrowUpRight, ArrowDownRight, 
  Globe, SlidersHorizontal, RefreshCw, Zap, Target
} from 'lucide-react';

interface Rep {
  id: string;
  name: string;
  region: string;
  quota_attainment_pct: number;
  closed_won_usd: number;
  deals_won: number;
  win_rate_pct: number;
}

interface Stage {
  stage: string;
  deals: number;
  value_usd: number;
  win_prob_pct: number;
}

export default function App() {
  const [selectedRegion, setSelectedRegion] = useState<string>("All Regions");
  const [selectedQuarter, setSelectedQuarter] = useState<string>("Q3 2026");
  const [activeTab, setActiveTab] = useState<'pipeline' | 'reps' | 'forecast' | 'cohorts'>('pipeline');
  const [isSyncing, setIsSyncing] = useState<boolean>(false);

  const reps: Rep[] = [
    { id: "rep-01", name: "Sarah Jenkins", region: "North America", quota_attainment_pct: 142, closed_won_usd: 2840000, deals_won: 28, win_rate_pct: 44 },
    { id: "rep-02", name: "Marcus Vance", region: "EMEA", quota_attainment_pct: 128, closed_won_usd: 2560000, deals_won: 24, win_rate_pct: 39 },
    { id: "rep-03", name: "Elena Rostova", region: "APAC", quota_attainment_pct: 115, closed_won_usd: 2300000, deals_won: 21, win_rate_pct: 36 },
    { id: "rep-04", name: "David Chen", region: "North America", quota_attainment_pct: 98, closed_won_usd: 1960000, deals_won: 19, win_rate_pct: 31 },
    { id: "rep-05", name: "Ananya Sharma", region: "LATAM & India", quota_attainment_pct: 108, closed_won_usd: 2160000, deals_won: 22, win_rate_pct: 35 }
  ];

  const stages: Stage[] = [
    { stage: "Discovery & Qualification", deals: 142, value_usd: 8520000, win_prob_pct: 20 },
    { stage: "Demo & Technical Validation", deals: 98, value_usd: 11400000, win_prob_pct: 45 },
    { stage: "Security & Legal Review", deals: 64, value_usd: 9600000, win_prob_pct: 75 },
    { stage: "Contract & Negotiation", deals: 36, value_usd: 8930000, win_prob_pct: 90 },
    { stage: "Closed Won (YTD)", deals: 218, value_usd: 14850000, win_prob_pct: 100 }
  ];

  const formatUSD = (num: number) => {
    return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(num);
  };

  const handleSync = () => {
    setIsSyncing(true);
    setTimeout(() => setIsSyncing(false), 800);
  };

  return (
    <div className="min-h-screen bg-[#030712] text-slate-100 flex flex-col font-sans selection:bg-cyan-500 selection:text-black">
      {/* Top Navbar */}
      <header className="border-b border-cyan-500/20 bg-[#070d1e]/80 backdrop-blur-xl px-6 py-3.5 flex items-center justify-between sticky top-0 z-50 shadow-2xl shadow-cyan-950/40">
        <div className="flex items-center space-x-3.5">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 via-indigo-500 to-fuchsia-500 p-0.5 shadow-lg shadow-cyan-500/30 flex items-center justify-center">
            <div className="w-full h-full bg-[#070d1e] rounded-[10px] flex items-center justify-center">
              <DollarSign className="w-5 h-5 text-cyan-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-black tracking-wider text-base bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 via-indigo-300 to-fuchsia-400">
                APEXSALES 360
              </span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-300 font-mono">
                ENTERPRISE v5.0
              </span>
            </div>
            <p className="text-xs text-slate-400 font-medium">Revenue Intelligence, Pipeline Telemetry & Sales Optimization</p>
          </div>
        </div>

        {/* Global Filter Bar */}
        <div className="flex items-center space-x-3">
          <select
            value={selectedRegion}
            onChange={(e) => setSelectedRegion(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-1.5 font-medium outline-none focus:border-cyan-400"
          >
            <option>All Regions</option>
            <option>North America</option>
            <option>EMEA</option>
            <option>APAC</option>
            <option>LATAM & India</option>
          </select>

          <select
            value={selectedQuarter}
            onChange={(e) => setSelectedQuarter(e.target.value)}
            className="bg-slate-900 border border-slate-700 text-xs text-slate-200 rounded-lg px-3 py-1.5 font-medium outline-none focus:border-cyan-400"
          >
            <option>Q3 2026</option>
            <option>Q2 2026</option>
            <option>Q1 2026</option>
            <option>Full Year 2026</option>
          </select>

          <button
            onClick={handleSync}
            disabled={isSyncing}
            className="px-3.5 py-1.5 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 border border-cyan-500/40 text-cyan-300 text-xs font-semibold flex items-center space-x-1.5 transition-all active:scale-95"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isSyncing ? 'animate-spin' : ''}`} />
            <span>Sync Live</span>
          </button>
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6 flex flex-col space-y-6">
        {/* KPI Row */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="rounded-2xl bg-[#091124]/90 border border-cyan-500/20 p-4 shadow-xl flex flex-col justify-between">
            <div className="flex justify-between items-start">
              <span className="text-xs font-mono text-slate-400 uppercase">Annual Recurring Revenue (ARR)</span>
              <div className="p-1.5 rounded-lg bg-cyan-500/10 text-cyan-400">
                <TrendingUp className="w-4 h-4" />
              </div>
            </div>
            <div className="mt-3">
              <p className="text-2xl font-black text-cyan-300 font-mono tracking-tight">$14,850,000</p>
              <div className="flex items-center space-x-1 text-xs text-emerald-400 mt-1">
                <ArrowUpRight className="w-3.5 h-3.5" />
                <span>+18.4% YoY Growth</span>
              </div>
            </div>
          </div>

          <div className="rounded-2xl bg-[#091124]/90 border border-indigo-500/20 p-4 shadow-xl flex flex-col justify-between">
            <div className="flex justify-between items-start">
              <span className="text-xs font-mono text-slate-400 uppercase">Monthly Recurring Revenue (MRR)</span>
              <div className="p-1.5 rounded-lg bg-indigo-500/10 text-indigo-400">
                <DollarSign className="w-4 h-4" />
              </div>
            </div>
            <div className="mt-3">
              <p className="text-2xl font-black text-indigo-300 font-mono tracking-tight">$1,237,500</p>
              <div className="flex items-center space-x-1 text-xs text-emerald-400 mt-1">
                <ArrowUpRight className="w-3.5 h-3.5" />
                <span>+$45,200 New MRR</span>
              </div>
            </div>
          </div>

          <div className="rounded-2xl bg-[#091124]/90 border border-fuchsia-500/20 p-4 shadow-xl flex flex-col justify-between">
            <div className="flex justify-between items-start">
              <span className="text-xs font-mono text-slate-400 uppercase">Net Revenue Retention (NRR)</span>
              <div className="p-1.5 rounded-lg bg-fuchsia-500/10 text-fuchsia-400">
                <ShieldCheck className="w-4 h-4" />
              </div>
            </div>
            <div className="mt-3">
              <p className="text-2xl font-black text-fuchsia-300 font-mono tracking-tight">118.4%</p>
              <div className="flex items-center space-x-1 text-xs text-emerald-400 mt-1">
                <Zap className="w-3.5 h-3.5" />
                <span>Negative Churn Benchmark</span>
              </div>
            </div>
          </div>

          <div className="rounded-2xl bg-[#091124]/90 border border-emerald-500/20 p-4 shadow-xl flex flex-col justify-between">
            <div className="flex justify-between items-start">
              <span className="text-xs font-mono text-slate-400 uppercase">LTV to CAC Ratio</span>
              <div className="p-1.5 rounded-lg bg-emerald-500/10 text-emerald-400">
                <Target className="w-4 h-4" />
              </div>
            </div>
            <div className="mt-3">
              <p className="text-2xl font-black text-emerald-300 font-mono tracking-tight">4.6x</p>
              <div className="flex items-center space-x-1 text-xs text-emerald-400 mt-1">
                <span>Payback: 8.2 Months</span>
              </div>
            </div>
          </div>
        </div>

        {/* Tab Controls */}
        <div className="flex items-center space-x-2 border-b border-slate-800 pb-2">
          <button
            onClick={() => setActiveTab('pipeline')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center space-x-2 ${
              activeTab === 'pipeline' ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-lg shadow-cyan-500/10' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Layers className="w-4 h-4" />
            <span>Pipeline Funnel & Stages</span>
          </button>
          <button
            onClick={() => setActiveTab('reps')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center space-x-2 ${
              activeTab === 'reps' ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/40 shadow-lg shadow-indigo-500/10' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Award className="w-4 h-4" />
            <span>Sales Rep Leaderboard</span>
          </button>
        </div>

        {/* Dynamic Content Views */}
        {activeTab === 'pipeline' && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Pipeline Stage Visualizer */}
            <div className="lg:col-span-8 rounded-2xl bg-[#091124]/90 border border-cyan-500/20 p-6 shadow-xl">
              <div className="flex justify-between items-center mb-6">
                <div>
                  <h3 className="text-base font-bold text-white tracking-tight">Weighted Revenue Funnel by Stage</h3>
                  <p className="text-xs text-slate-400">Total Unweighted Pipeline: $38.45M | Weighted Expectancy: $24.12M</p>
                </div>
                <span className="text-xs font-mono text-cyan-400 bg-cyan-950/60 px-2.5 py-1 rounded-lg border border-cyan-800/50">
                  Active Deals: 558
                </span>
              </div>

              <div className="space-y-4">
                {stages.map((st, i) => (
                  <div key={i} className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-cyan-500/30 transition-all">
                    <div className="flex justify-between text-xs font-semibold mb-2">
                      <span className="text-slate-200">{st.stage}</span>
                      <div className="flex items-center space-x-4">
                        <span className="text-slate-400 font-mono">{st.deals} deals</span>
                        <span className="text-cyan-300 font-mono font-bold">{formatUSD(st.value_usd)}</span>
                        <span className="text-emerald-400 font-mono">{st.win_prob_pct}% Win Rate</span>
                      </div>
                    </div>
                    <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-cyan-500 via-indigo-500 to-fuchsia-500 h-full rounded-full transition-all duration-500"
                        style={{ width: `${(st.value_usd / 15000000) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Win-Rate & Regional Velocity Card */}
            <div className="lg:col-span-4 rounded-2xl bg-[#091124]/90 border border-indigo-500/20 p-6 shadow-xl flex flex-col justify-between">
              <div>
                <h3 className="text-base font-bold text-white tracking-tight mb-1">Regional Contribution</h3>
                <p className="text-xs text-slate-400 mb-4">Revenue distribution across global operating units</p>

                <div className="space-y-3 font-mono text-xs">
                  <div className="flex justify-between p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
                    <span className="text-slate-300">North America (NA)</span>
                    <span className="text-cyan-300 font-bold">$7.24M (48.7%)</span>
                  </div>
                  <div className="flex justify-between p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
                    <span className="text-slate-300">EMEA (Europe/ME)</span>
                    <span className="text-indigo-300 font-bold">$4.12M (27.7%)</span>
                  </div>
                  <div className="flex justify-between p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
                    <span className="text-slate-300">APAC (Asia-Pacific)</span>
                    <span className="text-fuchsia-300 font-bold">$2.38M (16.0%)</span>
                  </div>
                  <div className="flex justify-between p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
                    <span className="text-slate-300">LATAM & India</span>
                    <span className="text-emerald-300 font-bold">$1.11M (7.6%)</span>
                  </div>
                </div>
              </div>

              <div className="mt-6 pt-4 border-t border-slate-800">
                <div className="flex justify-between items-center text-xs">
                  <span className="text-slate-400">Average Sales Cycle</span>
                  <span className="text-white font-mono font-bold">34 Days (-6d)</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'reps' && (
          <div className="rounded-2xl bg-[#091124]/90 border border-cyan-500/20 p-6 shadow-xl">
            <h3 className="text-base font-bold text-white tracking-tight mb-4">Enterprise Account Executive Leaderboard</h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs font-mono">
                <thead>
                  <tr className="border-b border-slate-800 text-slate-400 uppercase">
                    <th className="pb-3 font-semibold">Account Executive</th>
                    <th className="pb-3 font-semibold">Region</th>
                    <th className="pb-3 font-semibold">Quota Attainment</th>
                    <th className="pb-3 font-semibold">Closed Won (USD)</th>
                    <th className="pb-3 font-semibold">Deals Won</th>
                    <th className="pb-3 font-semibold">Win Rate</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {reps.map((r, idx) => (
                    <tr key={r.id} className="hover:bg-slate-900/40 transition-colors">
                      <td className="py-3.5 font-bold text-white flex items-center space-x-2">
                        <span className="w-5 h-5 rounded-full bg-cyan-500/20 text-cyan-300 flex items-center justify-center text-[10px]">
                          {idx + 1}
                        </span>
                        <span>{r.name}</span>
                      </td>
                      <td className="py-3.5 text-slate-300">{r.region}</td>
                      <td className="py-3.5">
                        <span className={`px-2 py-0.5 rounded-full font-bold ${
                          r.quota_attainment_pct >= 120 ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' : 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30'
                        }`}>
                          {r.quota_attainment_pct}%
                        </span>
                      </td>
                      <td className="py-3.5 text-cyan-300 font-bold">{formatUSD(r.closed_won_usd)}</td>
                      <td className="py-3.5 text-slate-300">{r.deals_won} deals</td>
                      <td className="py-3.5 text-emerald-400 font-bold">{r.win_rate_pct}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
