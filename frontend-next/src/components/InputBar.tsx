'use client'

import { useState } from 'react'

interface InputBarProps {
  onSend: (text: string) => void
  disabled: boolean
}

export default function InputBar({ onSend, disabled }: InputBarProps) {
  const [value, setValue] = useState('')

  const submit = () => {
    if (!value.trim() || disabled) return
    onSend(value.trim())
    setValue('')
  }

  return (
    <div
      style={{
        background: '#FFFFFF',
        borderTop: '0.5px solid rgba(26,20,70,0.13)',
        padding: '10px 14px',
        display: 'flex',
        alignItems: 'center',
        gap: 9,
        flexShrink: 0,
      }}
    >
      {/* Input wrapper */}
      <div
        style={{
          flex: 1,
          background: '#F4F4F4',
          border: '0.5px solid rgba(26,20,70,0.13)',
          borderRadius: 10,
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          padding: '0 12px',
        }}
      >
        <input
          type="text"
          value={value}
          placeholder="Type your reply…"
          disabled={disabled}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault()
              submit()
            }
          }}
          style={{
            flex: 1,
            border: 'none',
            background: 'transparent',
            fontSize: 13,
            color: '#1A1446',
            padding: '9px 0',
            outline: 'none',
          }}
        />
      </div>

      {/* Send button */}
      <button
        onClick={submit}
        disabled={disabled || !value.trim()}
        style={{
          width: 34,
          height: 34,
          flexShrink: 0,
          background: '#FFD000',
          borderRadius: 8,
          border: 'none',
          cursor: disabled ? 'not-allowed' : 'pointer',
          color: '#1A1446',
          fontSize: 16,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          opacity: disabled ? 0.5 : 1,
          transition: 'background 0.15s',
        }}
        onMouseEnter={(e) => {
          if (!disabled) (e.currentTarget as HTMLButtonElement).style.background = '#E6BB00'
        }}
        onMouseLeave={(e) => {
          ;(e.currentTarget as HTMLButtonElement).style.background = '#FFD000'
        }}
      >
        ↑
      </button>
    </div>
  )
}
