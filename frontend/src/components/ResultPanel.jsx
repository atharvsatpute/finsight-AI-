import { AlertTriangle, TrendingUp, Briefcase, ChevronRight } from 'lucide-react'
import clsx from 'clsx'

function RiskBadge({ level }) {
  const colors = {
    low: 'bg-accent/10 text-accent border-accent/20',
    medium: 'bg-warn/10 text-warn border-warn/20',
    high: 'bg-danger/10 text-danger border-danger/20',
    critical: 'bg-danger/20 text-danger border-danger/30',
  }
  return (
    <span className={clsx('text-[10px] font-mono px-2 py-0.5 rounded border uppercase tracking-wider', colors[level] || colors.medium)}>
      {level}
    </span>
  )
}

function Section({ icon: Icon, title, color, children }) {
  return (
    <div className="bg-surface2 border border-border rounded-lg p-3">
      <div className="flex items-center gap-2 mb-2">
        <Icon size={12} style={{ color }} />
        <span className="text-[10px] font-mono text-muted tracking-widest">{title}</span>
      </div>
      {children}
    </div>
  )
}

export default function ResultPanel({ result, error }) {
  if (error) {
    return (
      <div className="bg-danger/5 border border-danger/30 rounded-xl p-4 slide-up">
        <div className="flex items-center gap-2 text-danger text-[13px] font-bold mb-1">
          <AlertTriangle size={14} />
          Analysis failed
        </div>
        <p className="text-[12px] text-muted font-mono">{error}</p>
        <p className="text-[11px] text-muted mt-2">Make sure the backend is running at localhost:8000</p>
      </div>
    )
  }

  if (!result) return null

  const { risk_analysis: risk, sentiment_analysis: sentiment, portfolio_insight: portfolio, confidence_score, sources_used } = result

  return (
    <div className="flex flex-col gap-3 slide-up">
      <div className="flex items-center justify-between px-1">
        <span className="text-[11px] font-mono text-muted">
          {sources_used} sources · confidence {Math.round(confidence_score * 100)}%
        </span>
        <div className="h-1 flex-1 mx-3 bg-border rounded-full overflow-hidden">
          <div className="h-full bg-accent rounded-full transition-all" style={{ width: `${Math.round(confidence_score * 100)}%` }} />
        </div>
      </div>

      <Section icon={AlertTriangle} title="RISK ANALYSIS" color="var(--warn)">
        <div className="flex items-center gap-2 mb-2">
          <RiskBadge level={risk?.risk_level} />
          <span className="text-[11px] font-mono text-muted">score: {risk?.risk_score?.toFixed(1)}/10</span>
        </div>
        <p className="text-[12px] text-white/80 leading-relaxed mb-2">{risk?.summary}</p>
        <div className="flex flex-col gap-1">
          {risk?.key_risks?.map((r, i) => (
            <div key={i} className="flex items-start gap-2 text-[11px] text-muted">
              <ChevronRight size={10} className="text-warn mt-0.5 flex-shrink-0" />
              {r}
            </div>
          ))}
        </div>
        <div className="mt-2 h-1.5 bg-border rounded-full overflow-hidden">
          <div className="h-full rounded-full bg-warn transition-all" style={{ width: `${Math.round((risk?.risk_score || 0) * 10)}%` }} />
        </div>
      </Section>

      <Section icon={TrendingUp} title="SENTIMENT ANALYSIS" color="var(--accent2)">
        <div className="flex items-center gap-3 mb-2">
          <span className={clsx('text-[11px] font-mono px-2 py-0.5 rounded border',
            sentiment?.overall_sentiment === 'positive' ? 'text-accent bg-accent/10 border-accent/20' :
            sentiment?.overall_sentiment === 'negative' ? 'text-danger bg-danger/10 border-danger/20' :
            'text-muted bg-surface border-border'
          )}>
            {sentiment?.overall_sentiment}
          </span>
          <span className="text-[11px] font-mono text-muted">
            score: {sentiment?.sentiment_score?.toFixed(2)}
          </span>
        </div>
        <p className="text-[12px] text-white/80 leading-relaxed mb-2">{sentiment?.summary}</p>
        <p className="text-[11px] text-muted">{sentiment?.market_outlook}</p>
      </Section>

      <Section icon={Briefcase} title="PORTFOLIO SIGNAL" color="var(--accent)">
        <p className="text-[12px] text-white/80 leading-relaxed mb-2">{portfolio?.executive_summary}</p>
        {portfolio?.buy_signals?.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mb-1.5">
            {portfolio.buy_signals.map(s => (
              <span key={s} className="text-[10px] font-mono px-2 py-0.5 rounded bg-accent/10 text-accent border border-accent/20">BUY {s}</span>
            ))}
          </div>
        )}
        {portfolio?.hold_recommendations?.length > 0 && (
          <div className="flex flex-wrap gap-1.5">
            {portfolio.hold_recommendations.map(s => (
              <span key={s} className="text-[10px] font-mono px-2 py-0.5 rounded bg-warn/10 text-warn border border-warn/20">HOLD {s}</span>
            ))}
          </div>
        )}
      </Section>
    </div>
  )
}
