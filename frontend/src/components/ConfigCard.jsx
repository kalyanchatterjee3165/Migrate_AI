export default function ConfigCard({ title, rows }) {
  return (
    <div style={{
      background: '#fff', borderLeft: '3px solid var(--lm-yellow)',
      borderRadius: '0 8px 8px 0', marginTop: 8, overflow: 'hidden',
      border: '1px solid var(--lm-border)', borderLeft: '3px solid var(--lm-yellow)',
    }}>
      <div style={{
        padding: '6px 12px', fontSize: 10, fontWeight: 700,
        textTransform: 'uppercase', letterSpacing: '0.08em',
        color: 'rgba(26,20,70,0.45)', borderBottom: '1px solid var(--lm-border)',
      }}>
        {title}
      </div>
      {rows.map((row, i) => (
        <div key={row.key} style={{
          display: 'flex', gap: 12, padding: '6px 12px',
          borderBottom: i < rows.length - 1 ? '1px solid var(--lm-border)' : 'none',
          fontSize: 12,
        }}>
          <span style={{ color: 'rgba(26,20,70,0.55)', minWidth: 90 }}>{row.key}</span>
          <span style={{ fontFamily: 'monospace', color: 'var(--lm-blue)', fontWeight: 500 }}>{row.value}</span>
        </div>
      ))}
    </div>
  )
}
