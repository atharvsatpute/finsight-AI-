import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'

const PERF_DATA = [
  { name: 'risk', precision: 87 },
  { name: 'sentiment', precision: 81 },
  { name: 'portfolio', precision: 84 },
  { name: 'sec-filing', precision: 76 },
  { name: 'macro', precision: 91 },
]

const VOLUME_DATA = Array.from({ length: 24 }, (_, i) => ({
  hour: i,
  queries: Math.floor(30 + Math.random() * 80),
}))

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="bg-surface border border-border rounded-lg px-3 py-2 text-[11px] font-mono">
      <div className="text-muted mb-0.5">{label}</div>
      <div className="text-accent">{payload[0].value}{payload[0].name === 'precision' ? '%' : ' queries'}</div>
    </div>
  )
}

export default function PerfChart() {
  return (
    <div className="bg-surface border border-border rounded-xl overflow-hidden col-span-2">
      <div className="flex items-center justify-between px-4 py-3 border-b border-border">
        <span className="text-[13px] font-bold">RAG pipeline performance</span>
        <span className="text-[10px] font-mono px-2 py-1 rounded bg-accent/10 text-accent border border-accent/20 tracking-wider">
          FAISS · HUGGINGFACE
        </span>
      </div>
      <div className="grid grid-cols-2 gap-0 divide-x divide-border">
        <div className="p-4">
          <div className="text-[10px] font-mono text-muted tracking-widest mb-3">PRECISION BY QUERY TYPE</div>
          <ResponsiveContainer width="100%" height={140}>
            <BarChart data={PERF_DATA} barSize={24}>
              <XAxis dataKey="name" tick={{ fontSize: 10, fontFamily: 'DM Mono', fill: '#64748b' }} axisLine={false} tickLine={false} />
              <YAxis domain={[60, 100]} tick={{ fontSize: 10, fontFamily: 'DM Mono', fill: '#64748b' }} axisLine={false} tickLine={false} />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
              <Bar dataKey="precision" radius={[3, 3, 0, 0]}>
                {PERF_DATA.map((entry, i) => (
                  <Cell key={i} fill={entry.precision >= 85 ? '#00e5a0' : entry.precision >= 80 ? '#7c6ef5' : '#f59e0b'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="p-4">
          <div className="text-[10px] font-mono text-muted tracking-widest mb-3">QUERY VOLUME — 24H</div>
          <ResponsiveContainer width="100%" height={140}>
            <BarChart data={VOLUME_DATA} barSize={8}>
              <XAxis dataKey="hour" tick={{ fontSize: 9, fontFamily: 'DM Mono', fill: '#64748b' }} axisLine={false} tickLine={false} interval={5} />
              <YAxis hide />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
              <Bar dataKey="queries" radius={[2, 2, 0, 0]}>
                {VOLUME_DATA.map((_, i) => (
                  <Cell key={i} fill={i >= 20 ? '#00e5a0' : '#1e2d45'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
