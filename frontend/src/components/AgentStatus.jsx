import clsx from 'clsx'

const AGENTS = [
  { id: 'risk', label: 'Risk', initial: 'R', color: 'accent', bg: 'rgba(0,229,160,0.15)' },
  { id: 'sentiment', label: 'Sentiment', initial: 'S', color: 'accent2', bg: 'rgba(124,110,245,0.15)' },
  { id: 'portfolio', label: 'Portfolio', initial: 'P', color: 'warn', bg: 'rgba(245,158,11,0.15)' },
]

const STATUS_COLORS = {
  idle: 'text-muted',
  running: 'text-accent',
  done: 'text-accent',
  error: 'text-danger',
}

const STATUS_LABELS = {
  idle: 'Idle',
  running: 'Running',
  done: 'Done',
  error: 'Error',
}

export default function AgentStatus({ agentStates }) {
  return (
    <div className="bg-surface border border-border rounded-xl overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b border-border">
        <span className="text-[13px] font-bold">Agent status</span>
        <span className="text-[10px] font-mono px-2 py-1 rounded bg-[rgba(124,110,245,0.12)] text-[#a899ff] border border-[rgba(124,110,245,0.2)] tracking-wider">
          3 ACTIVE
        </span>
      </div>
      <div className="grid grid-cols-3 gap-2 p-4">
        {AGENTS.map(agent => {
          const status = agentStates[agent.id] || 'idle'
          const isRunning = status === 'running'
          return (
            <div
              key={agent.id}
              className={clsx(
                'flex flex-col items-center bg-surface2 border rounded-lg p-3 transition-all',
                isRunning ? 'border-accent border-pulse' : 'border-border'
              )}
            >
              <div
                className="w-8 h-8 rounded-full flex items-center justify-center text-[14px] font-bold mb-2"
                style={{ background: agent.bg, color: `var(--${agent.color})` }}
              >
                {agent.initial}
              </div>
              <div className="text-[12px] font-bold mb-1">{agent.label}</div>
              <div className={clsx('text-[10px] font-mono', STATUS_COLORS[status])}>
                {STATUS_LABELS[status]}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
