import type { ConfigCardData } from '@/types'

interface ConfigCardProps {
  data: ConfigCardData
}

export default function ConfigCard({ data }: ConfigCardProps) {
  return (
    <div
      style={{
        background: '#FFFFFF',
        border: '0.5px solid rgba(26,20,70,0.13)',
        borderLeft: '3px solid #FFD000',
        borderRadius: '0 8px 8px 0',
        padding: '10px 12px',
        marginTop: 7,
      }}
    >
      <div
        style={{
          fontSize: 10,
          textTransform: 'uppercase',
          letterSpacing: '0.07em',
          color: 'rgba(26,20,70,0.5)',
          marginBottom: 7,
          fontWeight: 500,
        }}
      >
        {data.title}
      </div>
      {data.rows.map((row, i) => (
        <div
          key={row.key}
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            padding: '3px 0',
            borderBottom:
              i < data.rows.length - 1 ? '0.5px solid rgba(26,20,70,0.13)' : 'none',
          }}
        >
          <span style={{ color: 'rgba(26,20,70,0.55)', fontSize: 12 }}>{row.key}</span>
          <span
            style={{ fontFamily: 'monospace', fontSize: 11, color: '#1A1446' }}
          >
            {row.value}
          </span>
        </div>
      ))}
    </div>
  )
}
