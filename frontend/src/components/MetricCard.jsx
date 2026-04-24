import clsx from 'clsx'

export default function MetricCard({ label, value, change, changeType = 'up', valueColor }) {
  return (
    <div className="bg-surface border border-border rounded-xl p-4 hover:border-accent/50 transition-colors cursor-default group">
      <div className="text-[10px] font-mono text-muted tracking-widest mb-2">{label}</div>
      <div className="text-[22px] font-extrabold tracking-tight" style={{ color: valueColor }}>
        {value}
      </div>
      {change && (
        <div className={clsx('text-[11px] font-mono mt-1', {
          'text-accent': changeType === 'up',
          'text-danger': changeType === 'down',
          'text-muted': changeType === 'flat',
        })}>
          {change}
        </div>
      )}
    </div>
  )
}
