'use client'

import type { LastMigration } from '@/types'

interface SidebarProps {
  lastMigrations: LastMigration[]
  onQuickStart: (text: string) => void
  onReset: () => void
}

const quickStarts = [
  { emoji: '🗄', label: 'Postgres → BigQuery', msg: 'I want to migrate data from Postgres to BigQuery' },
  { emoji: '📄', label: 'CSV → SQLite',         msg: 'I need to load a CSV file into SQLite' },
  { emoji: '☁️', label: 'S3 → Snowflake',       msg: 'I want to migrate data from S3 to Snowflake' },
  { emoji: '🍃', label: 'Mongo → S3',            msg: 'I want to export a MongoDB collection to S3' },
]

const btnBase: React.CSSProperties = {
  background: 'transparent',
  color: 'rgba(255,255,255,0.75)',
  border: 'none',
  borderRadius: 8,
  textAlign: 'left',
  width: '100%',
  fontSize: 13,
  padding: '8px 12px',
  boxShadow: 'none',
  marginBottom: 2,
  cursor: 'pointer',
  display: 'block',
}

export default function Sidebar({ lastMigrations, onQuickStart, onReset }: SidebarProps) {
  return (
    <div
      style={{
        width: 240,
        flexShrink: 0,
        height: '100%',
        background: '#002663',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
      }}
    >
      {/* Quick Start */}
      <div style={{ padding: '14px 10px 6px' }}>
        <div
          style={{
            fontSize: 10,
            textTransform: 'uppercase',
            letterSpacing: '0.08em',
            color: 'rgba(255,255,255,0.35)',
            marginBottom: 6,
            fontWeight: 500,
          }}
        >
          Quick Start
        </div>
        {quickStarts.map((qs) => (
          <button
            key={qs.label}
            style={btnBase}
            onMouseEnter={(e) => {
              ;(e.currentTarget as HTMLButtonElement).style.background = 'rgba(255,255,255,0.1)'
              ;(e.currentTarget as HTMLButtonElement).style.color = '#fff'
            }}
            onMouseLeave={(e) => {
              ;(e.currentTarget as HTMLButtonElement).style.background = 'transparent'
              ;(e.currentTarget as HTMLButtonElement).style.color = 'rgba(255,255,255,0.75)'
            }}
            onClick={() => onQuickStart(qs.msg)}
          >
            {qs.emoji}{'  '}{qs.label}
          </button>
        ))}
      </div>

      {/* Divider */}
      <div
        style={{
          borderTop: '0.5px solid rgba(255,255,255,0.1)',
          margin: '12px 10px',
        }}
      />

      {/* Last Migration */}
      <div style={{ padding: '0 10px' }}>
        <div
          style={{
            fontSize: 10,
            textTransform: 'uppercase',
            letterSpacing: '0.08em',
            color: 'rgba(255,255,255,0.35)',
            marginBottom: 8,
            fontWeight: 500,
          }}
        >
          Last Migration
        </div>
        {lastMigrations.length === 0 ? (
          <div style={{ fontSize: 11, fontStyle: 'italic', color: 'rgba(255,255,255,0.3)' }}>
            No migrations yet
          </div>
        ) : (
          lastMigrations.map((m, i) => (
            <div
              key={i}
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                padding: '5px 8px',
                background: 'rgba(255,255,255,0.05)',
                borderRadius: 6,
                marginBottom: 3,
                fontSize: 11,
                color: 'rgba(255,255,255,0.6)',
              }}
            >
              <span>
                <span
                  style={{
                    width: 5,
                    height: 5,
                    background: '#FFD000',
                    borderRadius: '50%',
                    display: 'inline-block',
                    marginRight: 5,
                    verticalAlign: 'middle',
                  }}
                />
                {m.label}
              </span>
              <span>{m.detail}</span>
            </div>
          ))
        )}
      </div>

      {/* Spacer */}
      <div style={{ flex: 1 }} />

      {/* New Migration button */}
      <div style={{ margin: 12 }}>
        <button
          style={{
            width: '100%',
            background: '#FFD000',
            color: '#1A1446',
            fontWeight: 600,
            borderRadius: 8,
            border: 'none',
            padding: 9,
            cursor: 'pointer',
            fontSize: 13,
          }}
          onMouseEnter={(e) => {
            ;(e.currentTarget as HTMLButtonElement).style.background = '#E6BB00'
          }}
          onMouseLeave={(e) => {
            ;(e.currentTarget as HTMLButtonElement).style.background = '#FFD000'
          }}
          onClick={onReset}
        >
          ＋ New Migration
        </button>
      </div>
    </div>
  )
}
