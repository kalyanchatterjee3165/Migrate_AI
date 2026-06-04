import ReactMarkdown from 'react-markdown'
import type { Message as MessageType } from '@/types'
import ConfigCard from './ConfigCard'

interface MessageProps {
  message: MessageType
}

const aiBubble: React.CSSProperties = {
  background: '#FFFFFF',
  border: '0.5px solid rgba(26,20,70,0.13)',
  borderRadius: '2px 12px 12px 12px',
  padding: '10px 14px',
  fontSize: 13,
  color: '#1A1446',
  boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
  lineHeight: 1.65,
}

const userBubble: React.CSSProperties = {
  background: '#1A1446',
  borderRadius: '12px 2px 12px 12px',
  padding: '10px 14px',
  fontSize: 13,
  color: '#FFFFFF',
  lineHeight: 1.65,
}

export default function Message({ message }: MessageProps) {
  const isAI = message.role === 'assistant'

  return (
    <div style={{ alignSelf: isAI ? 'flex-start' : 'flex-end', maxWidth: '80%' }}>
      {isAI ? (
        <div style={aiBubble}>
          <ReactMarkdown
            components={{
              p: ({ children }) => (
                <p style={{ margin: '0 0 6px', color: '#1A1446' }}>{children}</p>
              ),
              strong: ({ children }) => (
                <strong style={{ color: '#1A1446', fontWeight: 600 }}>{children}</strong>
              ),
              em: ({ children }) => <em style={{ color: '#1A1446' }}>{children}</em>,
              ul: ({ children }) => (
                <ul style={{ margin: '4px 0', paddingLeft: 18, color: '#1A1446' }}>{children}</ul>
              ),
              ol: ({ children }) => (
                <ol style={{ margin: '4px 0', paddingLeft: 18, color: '#1A1446' }}>{children}</ol>
              ),
              li: ({ children }) => <li style={{ color: '#1A1446', marginBottom: 2 }}>{children}</li>,
              code: ({ children }) => (
                <code
                  style={{
                    background: 'rgba(26,20,70,0.06)',
                    borderRadius: 4,
                    padding: '1px 4px',
                    fontSize: 12,
                    fontFamily: 'monospace',
                    color: '#1A1446',
                  }}
                >
                  {children}
                </code>
              ),
            }}
          >
            {message.content}
          </ReactMarkdown>
          {message.configCard && <ConfigCard data={message.configCard} />}
        </div>
      ) : (
        <div style={userBubble}>
          <span style={{ color: '#FFFFFF', whiteSpace: 'pre-wrap' }}>{message.content}</span>
        </div>
      )}
    </div>
  )
}
