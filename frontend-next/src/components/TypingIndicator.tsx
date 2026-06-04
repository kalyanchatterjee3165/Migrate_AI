export default function TypingIndicator() {
  return (
    <div style={{ alignSelf: 'flex-start', maxWidth: '80%' }}>
      <div
        style={{
          background: '#FFFFFF',
          border: '0.5px solid rgba(26,20,70,0.13)',
          borderRadius: '2px 12px 12px 12px',
          padding: '10px 14px',
          boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
          display: 'flex',
          alignItems: 'center',
          gap: 4,
        }}
      >
        {[0, 0.2, 0.4].map((delay, i) => (
          <span
            key={i}
            style={{
              width: 6,
              height: 6,
              borderRadius: '50%',
              background: '#1A1446',
              opacity: 0.35,
              display: 'inline-block',
              animation: `bounce 1.2s ${delay}s infinite`,
            }}
          />
        ))}
        <style>{`
          @keyframes bounce {
            0%,60%,100% { transform: translateY(0); }
            30%          { transform: translateY(-6px); }
          }
        `}</style>
      </div>
    </div>
  )
}
