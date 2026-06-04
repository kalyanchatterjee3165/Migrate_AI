'use client'

import type { StatusResponse } from '@/types'

interface HeroProps {
  status: StatusResponse | null
}

const LogoSVG = () => (
  <svg viewBox="0 0 26 26" width="26" height="26" xmlns="http://www.w3.org/2000/svg">
    <rect x="2" y="5" width="8" height="8" rx="2" fill="#1A1446" />
    <rect x="2" y="16" width="8" height="3" rx="1.5" fill="rgba(26,20,70,0.3)" />
    <rect x="16" y="10" width="8" height="8" rx="2" fill="#1A1446" opacity="0.8" />
    <rect x="16" y="21" width="8" height="3" rx="1.5" fill="rgba(26,20,70,0.2)" />
    <path
      d="M10 9L13 9L13 14L16 14"
      stroke="#1A1446"
      strokeWidth="1.8"
      fill="none"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <path
      d="M14 12L16 14L14 16"
      stroke="#1A1446"
      strokeWidth="1.8"
      fill="none"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
)

const pills = [
  { icon: '⚡', label: 'One-time full loads' },
  { icon: '🛡', label: 'Pre & post validation' },
  { icon: '💬', label: 'Chat-driven config' },
  { icon: '🔌', label: '4 sources', suffix: '— Postgres · CSV · S3 · Mongo' },
  { icon: '🗄', label: '4 destinations', suffix: '— BigQuery · SQLite · S3 · Snowflake' },
]

const tabs = ['Chat', 'History', 'Output files', 'Settings']

export default function Hero({ status }: HeroProps) {
  const connected = status?.connected ?? false

  return (
    <div
      style={{
        background: '#1A1446',
        width: '100%',
        padding: '16px 28px 0',
        fontFamily: 'inherit',
        flexShrink: 0,
      }}
    >
      {/* Row 1 — logo + status */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: 12,
        }}
      >
        {/* Logo + wordmark */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <div
            style={{
              width: 42,
              height: 42,
              background: '#FFD000',
              borderRadius: 11,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0,
            }}
          >
            <LogoSVG />
          </div>
          <div>
            <div style={{ fontSize: 20, fontWeight: 500, letterSpacing: '-0.3px', lineHeight: 1.2 }}>
              <span style={{ color: '#fff' }}>Migrate</span>
              <span style={{ color: '#FFD000' }}>AI</span>
            </div>
            <div style={{ fontSize: 11, color: 'rgba(255,255,255,0.45)', marginTop: 1 }}>
              Intelligent data migration · powered by GPT-4o
            </div>
          </div>
        </div>

        {/* Status pill */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: 6,
            padding: '5px 12px',
            background: 'rgba(255,255,255,0.08)',
            border: '0.5px solid rgba(255,255,255,0.15)',
            borderRadius: 20,
            fontSize: 12,
            color: 'rgba(255,255,255,0.85)',
          }}
        >
          <span
            style={{
              width: 7,
              height: 7,
              background: connected ? '#4ADE80' : '#EF4444',
              borderRadius: '50%',
              display: 'inline-block',
              flexShrink: 0,
            }}
          />
          {connected ? 'GPT-4o connected' : 'Disconnected'}
        </div>
      </div>

      {/* Row 2 — headline + body */}
      <div style={{ marginBottom: 14 }}>
        <div style={{ fontSize: 14, fontWeight: 500, color: '#fff', marginBottom: 4 }}>
          Move your data{' '}
          <span style={{ color: '#FFD000' }}>anywhere</span>
          , in minutes — just by having a conversation.
        </div>
        <div
          style={{
            fontSize: 12,
            color: 'rgba(255,255,255,0.5)',
            lineHeight: 1.6,
            maxWidth: 700,
          }}
        >
          No pipelines to build. No scripts to write. No engineers needed. Tell MigrateAI your
          source and destination, answer a few questions, and it handles the rest — schema mapping,
          validation, and delivery included.
        </div>
      </div>

      {/* Row 3 — capability pills */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 14 }}>
        {pills.map((p) => (
          <span
            key={p.label}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 6,
              padding: '5px 11px',
              background: 'rgba(255,255,255,0.07)',
              border: '0.5px solid rgba(255,255,255,0.13)',
              borderRadius: 7,
              fontSize: 12,
              color: 'rgba(255,255,255,0.8)',
            }}
          >
            {p.icon}{' '}
            <strong style={{ color: '#fff' }}>{p.label}</strong>
            {p.suffix && ` ${p.suffix}`}
          </span>
        ))}
      </div>

      {/* Row 4 — tab bar */}
      <div
        style={{
          display: 'flex',
          borderTop: '0.5px solid rgba(255,255,255,0.12)',
          margin: '0 -28px',
        }}
      >
        {tabs.map((tab) => (
          <span
            key={tab}
            style={{
              padding: '10px 20px',
              fontSize: 13,
              color: tab === 'Chat' ? '#fff' : 'rgba(255,255,255,0.4)',
              borderBottom: tab === 'Chat' ? '2px solid #FFD000' : '2px solid transparent',
              cursor: 'default',
            }}
          >
            {tab}
          </span>
        ))}
      </div>
    </div>
  )
}
