'use client'

import { useEffect, useRef } from 'react'
import type { Message } from '@/types'
import MessageBubble from './Message'
import TypingIndicator from './TypingIndicator'

interface ChatAreaProps {
  messages: Message[]
  isTyping: boolean
}

export default function ChatArea({ messages, isTyping }: ChatAreaProps) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  return (
    <div
      style={{
        flex: 1,
        overflowY: 'auto',
        overflowX: 'hidden',
        padding: '18px 18px 20px',
        background: '#F4F4F4',
        display: 'flex',
        flexDirection: 'column',
        gap: 14,
      }}
    >
      {messages.map((m) => (
        <MessageBubble key={m.id} message={m} />
      ))}
      {isTyping && <TypingIndicator />}
      <div ref={bottomRef} />
    </div>
  )
}
