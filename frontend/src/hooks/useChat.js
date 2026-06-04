import { useState, useCallback } from 'react'
import { sendMessage as apiSend, resetSession as apiReset } from '../api/chat'

const WELCOME = {
  id: 'welcome',
  role: 'ai',
  text: "Hi! I'm migrate.ai — your AI-powered data migration assistant. Tell me what you'd like to migrate and I'll guide you through it.\n\nFor example: *\"I want to migrate my Postgres table to BigQuery\"*",
}

export function useChat() {
  const [messages, setMessages] = useState([WELCOME])
  const [isTyping, setIsTyping] = useState(false)

  const sendMessage = useCallback(async (text) => {
    if (!text.trim()) return
    const userMsg = { id: Date.now(), role: 'user', text }
    setMessages(prev => [...prev, userMsg])
    setIsTyping(true)
    try {
      const { reply } = await apiSend(text)
      setMessages(prev => [...prev, { id: Date.now() + 1, role: 'ai', text: reply }])
    } catch {
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'ai',
        text: 'Sorry, I encountered an error. Please try again.',
      }])
    } finally {
      setIsTyping(false)
    }
  }, [])

  const resetSession = useCallback(async () => {
    await apiReset().catch(() => {})
    setMessages([WELCOME])
    setIsTyping(false)
  }, [])

  return { messages, isTyping, sendMessage, resetSession }
}
