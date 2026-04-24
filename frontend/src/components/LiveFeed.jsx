import { useEffect, useState } from 'react'

const MOCK_FEED = [
  { dot: '#00e5a0', title: 'HSBC Q3 earnings beat estimates by 8%', source: 'Reuters', time: '2m ago' },
  { dot: '#7c6ef5', title: 'Bank of England holds rates at 5.25%', source: 'FT', time: '11m ago' },
  { dot: '#f59e0b', title: 'Monzo reaches 10M UK customers', source: 'TechCrunch', time: '24m ago' },
  { dot: '#ef4444', title: 'Credit risk spreads widening — report', source: 'Bloomberg', time: '38m ago' },
  { dot: '#00e5a0', title: 'UK fintech investment up 23% YoY', source: 'KPMG', time: '1h ago' },
]

export default function LiveFeed() {
  const [feed, setFeed] = useState(MOCK_FEED)

  useEffect(() => {
    const interval = setInterval(() => {
      const newItem = {
        dot: ['#00e5a0', '#7c6ef5', '#f59e0b'][Math.floor(Math.random() * 3)],
        title: ['JPMorgan raises UK bank targets', 'ECB signals rate pause ahead', 'Starling Bank eyes London IPO'][Math.floor(Math.random() * 3)],
        source: ['Reuters', 'FT', 'Bloomberg'][Math.floor(Math.random() * 3)],
        time: 'just now',
      }
      setFeed(prev => [newItem, ...prev.slice(0, 4)])
    }, 8000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="bg-surface border border-border rounded-xl overflow-hidden">
      <div className="flex items-center justify-between px-4 py-3 border-b border-border">
        <span className="text-[13px] font-bold">Live data feed</span>
        <span className="text-[10px] font-mono px-2 py-1 rounded bg-warn/10 text-warn border border-warn/20 tracking-wider flex items-center gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-warn pulse-dot" />
          KAFKA
        </span>
      </div>
      <div className="flex flex-col gap-1.5 p-3">
        {feed.map((item, i) => (
          <div
            key={i}
            className="flex gap-2.5 items-start p-2.5 rounded-lg border border-border bg-surface2 hover:border-accent2/50 transition-colors cursor-pointer"
            style={i === 0 ? { animation: 'slide-up 0.3s ease' } : {}}
          >
            <span className="w-2 h-2 rounded-full flex-shrink-0 mt-1" style={{ background: item.dot }} />
            <div className="flex-1 min-w-0">
              <div className="text-[12px] font-medium truncate">{item.title}</div>
              <div className="text-[10px] font-mono text-muted mt-0.5">{item.source} · {item.time}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
