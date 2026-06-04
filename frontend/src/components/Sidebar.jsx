import { Database, FileText, Cloud, Leaf } from 'lucide-react'
import { useState } from 'react'

const QUICK_STARTS = [
  { icon: Database, text: 'Postgres → BigQuery', message: 'I want to migrate data from Postgres to BigQuery' },
  { icon: FileText, text: 'CSV → SQLite', message: 'I need to load a CSV file into SQLite' },
  { icon: Cloud, text: 'S3 → Snowflake', message: 'Move data from S3 to Snowflake' },
  { icon: Leaf, text: 'Mongo → S3', message: 'Export a MongoDB collection to S3' },
]

export default function Sidebar({ onQuickStart, onReset, lastMigration }) {
  const [activeIdx, setActiveIdx] = useState(null)

  function handleQuickStart(item, idx) {
    setActiveIdx(idx)
    onQuickStart(item.message)
  }

  return (
    <aside style={{
      width: 220, background: 'var(--lm-dark-navy)',
      display: 'flex', flexDirection: 'column', overflow: 'hidden',
    }}>
      <div style={{ padding: '16px 12px 8px', color: 'rgba(255,255,255,0.45)',
        fontSize: 10, fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase' }}>
        Quick Start
      </div>

      <div style={{ flex: 1 }}>
        {QUICK_STARTS.map((item, idx) => {
          const Icon = item.icon
          const active = activeIdx === idx
          return (
            <button key={item.text} onClick={() => handleQuickStart(item, idx)}
              style={{
                display: 'flex', alignItems: 'center', gap: 10,
                width: '100%', background: active ? 'rgba(255,208,0,0.12)' : 'none',
                border: 'none', borderLeft: active ? '3px solid var(--lm-yellow)' : '3px solid transparent',
                cursor: 'pointer', padding: '10px 12px',
                color: active ? 'var(--lm-yellow)' : 'rgba(255,255,255,0.7)',
                fontSize: 13, textAlign: 'left', transition: 'all 0.15s',
              }}>
              <Icon size={15} />
              {item.text}
            </button>
          )
        })}
      </div>

      {lastMigration && (
        <div style={{ padding: '8px 12px', borderTop: '1px solid rgba(255,255,255,0.08)' }}>
          <div style={{ color: 'rgba(255,255,255,0.35)', fontSize: 10,
            textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: 4 }}>
            Last Migration
          </div>
          <div style={{ color: 'rgba(255,255,255,0.6)', fontSize: 11,
            background: 'rgba(255,255,255,0.06)', borderRadius: 4, padding: '4px 8px' }}>
            {lastMigration.text.slice(0, 60)}…
          </div>
        </div>
      )}

      <div style={{ padding: '12px' }}>
        <button onClick={onReset} style={{
          width: '100%', background: 'var(--lm-yellow)', color: 'var(--lm-blue)',
          border: 'none', borderRadius: 6, padding: '9px 0',
          fontWeight: 700, fontSize: 13, cursor: 'pointer',
          transition: 'background 0.15s',
        }}
          onMouseOver={e => e.target.style.background = 'var(--lm-yellow-hover)'}
          onMouseOut={e => e.target.style.background = 'var(--lm-yellow)'}>
          + New Migration
        </button>
      </div>
    </aside>
  )
}
