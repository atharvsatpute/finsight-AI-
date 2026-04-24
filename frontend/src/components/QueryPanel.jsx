import { useState } from 'react'
import { Send, Loader2 } from 'lucide-react'
import clsx from 'clsx'

const CHIPS = [
  'What are HSBC key risks this quarter?',
  'Monzo Revolut fintech sentiment UK',
  'Federal Reserve rate impact on banking',
  'London stock market outlook 2025',
  'AAPL MSFT earnings risk analysis',
]

export default function QueryPanel({ query, setQuery, loading, onAnalyze }) {
  return (
    <div className="bg-surface border border-border rounded-xl overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b border-border">
        <span className="text-[13px] font-bold tracking-wide">Financial intelligence query</span>
        <span className="text-[10px] font-mono px-2 py-1 rounded bg-accent/10 text-accent border border-accent/20 tracking-wider">
          RAG + AGENTS LIVE
        </span>
      </div>

      <div className="p-4">
        <div className="flex gap-2 mb-3">
          <input
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && !loading && onAnalyze()}
            placeholder="Ask any financial question..."
            className="flex-1 bg-surface2 border border-border text-white font-mono text-[12px] px-3 py-2.5 rounded-lg outline-none focus:border-accent transition-colors placeholder:text-muted"
          />
          <button
            onClick={() => onAnalyze()}
            disabled={loading}
            className={clsx(
              'flex items-center gap-2 px-4 py-2.5 rounded-lg font-bold text-[12px] transition-all',
              loading
                ? 'bg-surface2 text-muted cursor-not-allowed'
                : 'bg-accent text-bg hover:bg-[#00ffb3] active:scale-95'
            )}
          >
            {loading ? <Loader2 size={14} className="animate-spin" /> : <Send size={14} />}
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>

        <div className="flex gap-2 flex-wrap">
          {CHIPS.map(chip => (
            <button
              key={chip}
              onClick={() => { setQuery(chip); onAnalyze(chip) }}
              className="text-[11px] font-mono px-3 py-1 rounded bg-surface2 border border-border text-muted hover:border-accent2 hover:text-[#a899ff] transition-all"
            >
              {chip.length > 30 ? chip.slice(0, 28) + '…' : chip}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
