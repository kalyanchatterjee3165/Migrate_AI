import { useState, useRef, useEffect } from 'react'
import { Paperclip, ArrowUp } from 'lucide-react'

export default function InputBar({ onSend, disabled }) {
  const [text, setText] = useState('')
  const textareaRef = useRef(null)

  // Auto-grow textarea height as content expands
  useEffect(() => {
    const el = textareaRef.current
    if (!el) return
    el.style.height = 'auto'
    el.style.height = `${el.scrollHeight}px`
  }, [text])

  function submit() {
    if (!text.trim() || disabled) return
    onSend(text.trim())
    setText('')
  }

  function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
    // Shift+Enter falls through and inserts a newline naturally
  }

  return (
    <div style={{
      background: '#fff', borderTop: '1px solid var(--lm-border)',
      padding: '12px 16px',
    }}>
      <div style={{
        display: 'flex', alignItems: 'flex-end', gap: 10,
        background: 'var(--lm-light-gray)', border: '1px solid var(--lm-border)',
        borderRadius: 10, padding: '6px 10px',
      }}>
        <Paperclip size={17} style={{ color: 'rgba(26,20,70,0.35)', flexShrink: 0, marginBottom: 8 }} />
        <textarea
          ref={textareaRef}
          value={text}
          onChange={e => setText(e.target.value)}
          onKeyDown={handleKey}
          disabled={disabled}
          placeholder="Type your reply… (Shift+Enter for new line)"
          rows={1}
          style={{
            flex: 1, border: 'none', background: 'none', outline: 'none',
            fontSize: 14, color: 'var(--lm-blue)', resize: 'none',
            lineHeight: 1.5, maxHeight: 160, overflowY: 'auto',
            fontFamily: 'inherit', padding: '4px 0',
          }}
        />
        <button onClick={submit} disabled={disabled || !text.trim()}
          style={{
            width: 34, height: 34, borderRadius: 8, border: 'none',
            background: disabled || !text.trim() ? 'rgba(255,208,0,0.4)' : 'var(--lm-yellow)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            cursor: disabled || !text.trim() ? 'not-allowed' : 'pointer',
            flexShrink: 0, transition: 'background 0.15s', marginBottom: 2,
          }}>
          <ArrowUp size={17} color="#1A1446" />
        </button>
      </div>
    </div>
  )
}
