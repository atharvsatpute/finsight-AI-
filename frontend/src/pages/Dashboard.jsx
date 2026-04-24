import MetricCard from '../components/MetricCard'
import QueryPanel from '../components/QueryPanel'
import AgentStatus from '../components/AgentStatus'
import ResultPanel from '../components/ResultPanel'
import LiveFeed from '../components/LiveFeed'
import PerfChart from '../components/PerfChart'
import { useFinSight } from '../hooks/useFinSight'
import { RefreshCw } from 'lucide-react'

export default function Dashboard() {
  const {
    query, setQuery,
    loading, result, error,
    health, agentStates,
    analyze, fetchHealth,
  } = useFinSight()

  const vectors = health?.total_vectors?.toLocaleString() ?? '—'
  const isReady = health?.vector_store_ready

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* Topbar */}
      <div className="flex items-center gap-4 px-6 py-3.5 bg-surface border-b border-border flex-shrink-0">
        <div className="text-[15px] font-bold flex-1">Dashboard</div>
        <div className="flex items-center gap-1.5 text-[11px] font-mono text-accent bg-accent/8 border border-accent/20 rounded-full px-3 py-1">
          <span className="w-1.5 h-1.5 rounded-full bg-accent pulse-dot" />
          {isReady ? '3 agents live' : 'connecting...'}
        </div>
        <button
          onClick={fetchHealth}
          className="flex items-center gap-1.5 text-[12px] px-3 py-1.5 rounded-lg bg-surface2 border border-border text-muted hover:text-white hover:border-accent transition-all"
        >
          <RefreshCw size={12} />
          Refresh
        </button>
        <button
          onClick={() => analyze()}
          className="text-[12px] px-3 py-1.5 rounded-lg border border-accent/40 text-accent hover:bg-accent/10 transition-all"
        >
          + New analysis
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-5 flex flex-col gap-4">

        {/* Metrics Row */}
        <div className="grid grid-cols-4 gap-3">
          <MetricCard label="VECTORS INDEXED" value={vectors} change="+1,240 today" changeType="up" valueColor="#00e5a0" />
          <MetricCard label="RAG PRECISION" value="84%" change="+2.1% this week" changeType="up" valueColor="#a899ff" />
          <MetricCard label="QUERIES TODAY" value="1,847" change="avg 312ms latency" changeType="flat" valueColor="#f59e0b" />
          <MetricCard label="AGENT SUCCESS" value="98.4%" change="12 failed today" changeType="up" valueColor="#00e5a0" />
        </div>

        {/* Query Panel - full width */}
        <QueryPanel
          query={query}
          setQuery={setQuery}
          loading={loading}
          onAnalyze={analyze}
        />

        {/* Result + Agents row */}
        <div className="grid grid-cols-2 gap-4">
          <div className="flex flex-col gap-4">
            <AgentStatus agentStates={agentStates} />
            <LiveFeed />
          </div>
          <div>
            {(result || error) ? (
              <div className="bg-surface border border-border rounded-xl overflow-hidden">
                <div className="flex items-center justify-between px-4 py-3 border-b border-border">
                  <span className="text-[13px] font-bold">Analysis report</span>
                  {result && (
                    <span className="text-[10px] font-mono text-accent">
                      {result.generated_at ? new Date(result.generated_at).toLocaleTimeString() : ''}
                    </span>
                  )}
                </div>
                <div className="p-4">
                  <ResultPanel result={result} error={error} />
                </div>
              </div>
            ) : (
              <div className="bg-surface border border-border border-dashed rounded-xl h-full flex flex-col items-center justify-center p-8 text-center min-h-[300px]">
                <div className="text-[32px] mb-3 opacity-30">🧠</div>
                <div className="text-[13px] font-bold text-muted mb-1">No analysis yet</div>
                <div className="text-[12px] text-muted/60">Type a query above and click Analyze to run the multi-agent pipeline</div>
              </div>
            )}
          </div>
        </div>

        {/* Performance Charts */}
        <div className="grid grid-cols-2 gap-4">
          <PerfChart />
        </div>

      </div>
    </div>
  )
}
