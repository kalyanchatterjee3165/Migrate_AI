const dotStyle = (delay) => ({
  display: 'inline-block',
  width: 7,
  height: 7,
  borderRadius: '50%',
  background: 'var(--lm-blue)',
  opacity: 0.35,
  animation: 'bounce 1.2s infinite',
  animationDelay: delay,
})

export default function TypingIndicator() {
  return (
    <>
      <style>{`
        @keyframes bounce {
          0%, 80%, 100% { transform: translateY(0); }
          40% { transform: translateY(-5px); opacity: 0.65; }
        }
      `}</style>
      <div style={{ display: 'flex', alignItems: 'flex-end', gap: 8, marginBottom: 12 }}>
        <div style={{
          width: 27, height: 27, borderRadius: '50%', background: 'var(--lm-blue)',
          display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
        }}>
          <svg width="14" height="10" viewBox="0 0 14 10" fill="none">
            <rect x="0" y="0" width="5" height="7" rx="1" fill="#FFD000" />
            <rect x="9" y="0" width="5" height="7" rx="1" fill="#FFD000" opacity="0.7" />
            <path d="M5 3.5 L7 1 L9 3.5" stroke="#FFD000" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" fill="none" />
            <line x1="7" y1="1" x2="7" y2="6" stroke="#FFD000" strokeWidth="1.2" strokeLinecap="round" />
          </svg>
        </div>
        <div style={{
          background: '#fff', border: '1px solid var(--lm-border)',
          borderRadius: '2px 12px 12px 12px', padding: '10px 14px',
          display: 'flex', gap: 4, alignItems: 'center',
        }}>
          <span style={dotStyle('0s')} />
          <span style={dotStyle('0.2s')} />
          <span style={dotStyle('0.4s')} />
        </div>
      </div>
    </>
  )
}
