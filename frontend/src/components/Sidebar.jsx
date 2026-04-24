import { useState } from 'react'
import { LayoutDashboard, Search, FileText, Bot, Database, FlaskConical, Activity, Layers, Settings } from 'lucide-react'
import clsx from 'clsx'

const NAV = [
  { section: 'ANALYSIS', items: [
    { icon: LayoutDashboard, label: 'Dashboard', id: 'dashboard' },
    { icon: Search, label: 'Query', id: 'query' },
    { icon: FileText, label: 'Reports', id: 'reports' },
  ]},
  { section: 'SYSTEM', items: [
    { icon: Bot, label: 'Agents', id: 'agents' },
    { icon: Database, label: 'RAG Pipeline', id: 'rag' },
    { icon: FlaskConical, label: 'MLflow', id: 'mlflow' },
    { icon: Activity, label: 'Monitoring', id: 'monitoring' },
  ]},
  { section: 'CONFIG', items: [
    { icon: Layers, label: 'Data Sources', id: 'sources' },
    { icon: Settings, label: 'Settings', id: 'settings' },
  ]},
]

export default function Sidebar({ health }) {
  const [active, setActive] = useState('dashboard')

  return (
    <aside className="flex flex-col bg-surface border-r border-border h-full" style={{ width: 200, flexShrink: 0 }}>
      <div className="px-5 py-5 border-b border-border">
        <div className="text-accent font-sans font-extrabold text-lg tracking-tight">FinSight AI</div>
        <div className="text-muted font-mono text-[10px] tracking-widest mt-1">INTELLIGENCE PLATFORM</div>
      </div>

      <nav className="flex-1 overflow-y-auto py-2">
        {NAV.map(group => (
          <div key={group.section}>
            <div className="px-5 pt-4 pb-1 text-[10px] font-mono text-muted tracking-widest">{group.section}</div>
            {group.items.map(item => {
              const Icon = item.icon
              const isActive = active === item.id
              return (
                <button
                  key={item.id}
                  onClick={() => setActive(item.id)}
                  className={clsx(
                    'w-full flex items-center gap-2.5 px-5 py-2.5 text-[13px] transition-all border-l-2',
                    isActive
                      ? 'text-accent border-accent bg-accent/5'
                      : 'text-muted border-transparent hover:text-white hover:bg-surface2'
                  )}
                >
                  <Icon size={14} />
                  {item.label}
                </button>
              )
            })}
          </div>
        ))}
      </nav>

      <div className="px-5 py-4 border-t border-border">
        <div className="flex items-center gap-2.5 mb-3">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-accent2 to-accent flex items-center justify-center text-[11px] font-bold text-white flex-shrink-0">AS</div>
          <div>
            <div className="text-[13px] font-medium text-white">Atharv S.</div>
            <div className="text-[11px] text-muted">ML Engineer</div>
          </div>
        </div>
        {health && (
          <div className="flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-accent pulse-dot" />
            <span className="text-[10px] font-mono text-accent">{health.total_vectors?.toLocaleString() ?? 0} vectors</span>
          </div>
        )}
      </div>
    </aside>
  )
}
