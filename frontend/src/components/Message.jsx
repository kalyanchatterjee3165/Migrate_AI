import ReactMarkdown from 'react-markdown'
import ConfigCard from './ConfigCard'

const AvatarAI = () => (
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
)

const AvatarUser = () => (
  <div style={{
    width: 27, height: 27, borderRadius: '50%', background: '#e2e0ec',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    flexShrink: 0, fontSize: 12, fontWeight: 700, color: 'var(--lm-blue)',
  }}>U</div>
)

export default function Message({ message }) {
  const isAI = message.role === 'ai'

  return (
    <div style={{
      display: 'flex', alignItems: 'flex-start', gap: 8,
      marginBottom: 12, flexDirection: isAI ? 'row' : 'row-reverse',
    }}>
      {isAI ? <AvatarAI /> : <AvatarUser />}
      <div style={{ maxWidth: '72%' }}>
        <div style={{
          background: isAI ? '#fff' : 'var(--lm-blue)',
          color: isAI ? 'var(--lm-blue)' : '#fff',
          border: isAI ? '1px solid var(--lm-border)' : 'none',
          borderRadius: isAI ? '2px 12px 12px 12px' : '12px 2px 12px 12px',
          padding: '10px 14px', fontSize: 14, lineHeight: 1.55,
          wordBreak: 'break-word',
        }}>
          <ReactMarkdown
            components={{
              p:      ({ children }) => <p style={{ margin: '0 0 6px' }}>{children}</p>,
              ul:     ({ children }) => <ul style={{ margin: '4px 0', paddingLeft: 18 }}>{children}</ul>,
              ol:     ({ children }) => <ol style={{ margin: '4px 0', paddingLeft: 18 }}>{children}</ol>,
              li:     ({ children }) => <li style={{ marginBottom: 2 }}>{children}</li>,
              strong: ({ children }) => <strong style={{ fontWeight: 700, color: 'inherit' }}>{children}</strong>,
              em:     ({ children }) => <em style={{ color: 'inherit' }}>{children}</em>,
              code:   ({ children }) => (
                <code style={{
                  background: isAI ? 'rgba(26,20,70,0.07)' : 'rgba(255,255,255,0.15)',
                  borderRadius: 4, padding: '1px 5px', fontSize: 13, fontFamily: 'monospace',
                }}>{children}</code>
              ),
            }}
          >
            {message.text}
          </ReactMarkdown>
        </div>
        {message.configCard && (
          <ConfigCard title={message.configCard.title} rows={message.configCard.rows} />
        )}
      </div>
    </div>
  )
}
