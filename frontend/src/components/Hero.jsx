import { useEffect, useState } from 'react'
import { Zap, ShieldCheck, MessageSquare, Plug, Database } from 'lucide-react'

const TABS = ['Chat', 'History', 'Output files', 'Settings']

const ABLogo = ({ size = 44 }) => (
  <svg width={size} height={size} viewBox="0 0 44 44" fill="none">
    <rect width="44" height="44" rx="8" fill="#FFD000" />
    <rect x="6" y="9" width="12" height="14" rx="2.5" fill="#1A1446" />
    <rect x="26" y="9" width="12" height="14" rx="2.5" fill="#1A1446" opacity="0.85" />
    <rect x="6" y="26" width="4" height="3" rx="1" fill="#1A1446" opacity="0.3" />
    <rect x="11" y="26" width="4" height="3" rx="1" fill="#1A1446" opacity="0.3" />
    <rect x="26" y="26" width="4" height="3" rx="1" fill="#1A1446" opacity="0.2" />
    <rect x="31" y="26" width="4" height="3" rx="1" fill="#1A1446" opacity="0.2" />
    <path d="M18 16 L22 12 L26 16" stroke="#FFD000" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" fill="none" />
    <line x1="22" y1="12" x2="22" y2="22" stroke="#FFD000" strokeWidth="2" strokeLinecap="round" />
  </svg>
)

const pills = [
  { icon: Zap, label: 'One-time full loads' },
  { icon: ShieldCheck, label: 'Pre & post validation' },
  { icon: MessageSquare, label: 'Chat-driven config' },
  { icon: Plug, label: '4 sources — Postgres · CSV · S3 · Mongo' },
  { icon: Database, label: '4 destinations — BigQuery · SQLite · S3 · Snowflake' },
]

export default function Hero({ activeTab, onTabChange, status }) {
  return (
    <header style={{ background: 'var(--lm-blue)', width: '100%', flexShrink: 0 }}>
      <div style={{ padding: '20px 28px 0' }}>
        {/* Top row: logo + wordmark + status */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 14, marginBottom: 16 }}>
          <ABLogo size={44} />
          <div>
            <div style={{ fontSize: 21, fontWeight: 700, lineHeight: 1.2 }}>
              <span style={{ color: '#fff' }}>Migrate</span>
              <span style={{ color: 'var(--lm-yellow)' }}>AI</span>
            </div>
            <div style={{ color: 'rgba(255,255,255,0.65)', fontSize: 12, marginTop: 2 }}>
              Intelligent data migration · powered by GPT-4o
            </div>
          </div>
          <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 6,
            background: 'rgba(255,255,255,0.1)', borderRadius: 20, padding: '5px 12px' }}>
            <span style={{ width: 8, height: 8, borderRadius: '50%',
              background: status?.connected ? '#4ade80' : '#6b7280', display: 'inline-block' }} />
            <span style={{ color: '#fff', fontSize: 12 }}>
              {status?.model || 'GPT-4o'} {status?.connected ? 'connected' : 'disconnected'}
            </span>
          </div>
        </div>

        {/* Headline + body */}
        <div style={{ marginBottom: 14 }}>
          <div style={{ color: '#fff', fontSize: 17, fontWeight: 600, marginBottom: 6 }}>
            Move your data{' '}
            <span style={{ color: 'var(--lm-yellow)' }}>anywhere</span>
            , in minutes.
          </div>
          <div style={{ color: 'rgba(255,255,255,0.7)', fontSize: 13, lineHeight: 1.5 }}>
            No pipelines to build. No scripts to write. Just describe what you need and let the agent handle it.
          </div>
        </div>

        {/* Capability pills */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 18 }}>
          {pills.map(({ icon: Icon, label }) => (
            <div key={label} style={{
              display: 'flex', alignItems: 'center', gap: 6,
              background: 'rgba(255,255,255,0.08)', border: '1px solid rgba(255,255,255,0.12)',
              borderRadius: 20, padding: '4px 12px', color: 'rgba(255,255,255,0.85)', fontSize: 12,
            }}>
              <Icon size={13} />
              {label}
            </div>
          ))}
        </div>
      </div>

      {/* Tab bar */}
      <div style={{ display: 'flex', borderTop: '1px solid rgba(255,255,255,0.1)' }}>
        {TABS.map(tab => (
          <button key={tab} onClick={() => onTabChange(tab.toLowerCase())}
            style={{
              background: 'none', border: 'none', cursor: 'pointer',
              padding: '12px 20px', fontSize: 13, fontWeight: 500,
              color: activeTab === tab.toLowerCase() ? 'var(--lm-yellow)' : 'rgba(255,255,255,0.6)',
              borderBottom: activeTab === tab.toLowerCase()
                ? '2px solid var(--lm-yellow)' : '2px solid transparent',
              transition: 'color 0.15s',
            }}>
            {tab}
          </button>
        ))}
      </div>
    </header>
  )
}
