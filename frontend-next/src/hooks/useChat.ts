'use client'

import { useState, useEffect, useCallback } from 'react'
import { v4 as uuidv4 } from 'uuid'
import { sendChat, resetSession, getStatus } from '@/api/client'
import type { Message, LastMigration, StatusResponse } from '@/types'
import { useSession } from './useSession'

const COMPLETION_WORDS = ['rows', 'migrated', 'complete', 'success', 'transferred']

const MIGRATION_PAIRS: Array<{
  srcKeys: string[]
  dstKeys: string[]
  label: string
}> = [
  { srcKeys: ['postgres'], dstKeys: ['bigquery'], label: 'Postgres → BigQuery' },
  { srcKeys: ['csv'],      dstKeys: ['sqlite'],   label: 'CSV → SQLite' },
  { srcKeys: ['s3'],       dstKeys: ['snowflake'], label: 'S3 → Snowflake' },
  { srcKeys: ['mongo'],    dstKeys: ['s3'],        label: 'Mongo → S3' },
]

const WELCOME_MESSAGE: Message = {
  id: 'welcome',
  role: 'assistant',
  content:
    "👋 Hey! I'm **MigrateAI** — your intelligent data migration assistant.\n\n" +
    'I can help you move data between systems in minutes, just by having a conversation. ' +
    'No scripts, no pipelines, no engineers needed.\n\n' +
    '**To get started, either:**\n' +
    '- Click a **Quick Start** path in the sidebar\n' +
    '- Or tell me what you want to migrate in your own words\n\n' +
    '**Supported sources:** Postgres · CSV · S3 · MongoDB\n\n' +
    '**Supported destinations:** BigQuery · SQLite · S3 · Snowflake',
  timestamp: new Date(),
}

function detectMigration(text: string): string | null {
  const low = text.toLowerCase()
  if (!COMPLETION_WORDS.some((w) => low.includes(w))) return null
  for (const { srcKeys, dstKeys, label } of MIGRATION_PAIRS) {
    if (srcKeys.some((k) => low.includes(k)) && dstKeys.some((k) => low.includes(k))) {
      return label
    }
  }
  return null
}

export function useChat() {
  const { sessionId } = useSession()
  const [messages, setMessages] = useState<Message[]>([WELCOME_MESSAGE])
  const [isTyping, setIsTyping] = useState(false)
  const [lastMigrations, setLastMigrations] = useState<LastMigration[]>([])
  const [status, setStatus] = useState<StatusResponse | null>(null)

  useEffect(() => {
    getStatus()
      .then(setStatus)
      .catch(() => {})
  }, [])

  const sendMessage = useCallback(
    async (text: string) => {
      if (!text.trim() || !sessionId) return

      const userMsg: Message = {
        id: uuidv4(),
        role: 'user',
        content: text.trim(),
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, userMsg])
      setIsTyping(true)

      try {
        const data = await sendChat(text.trim(), sessionId)
        const aiMsg: Message = {
          id: uuidv4(),
          role: 'assistant',
          content: data.reply,
          timestamp: new Date(),
        }
        setMessages((prev) => [...prev, aiMsg])

        // Check both user and AI text for migration completion
        const label = detectMigration(text) ?? detectMigration(data.reply)
        if (label) {
          const entry: LastMigration = {
            label,
            detail: 'done',
            time: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
          }
          setLastMigrations((prev) => [entry, ...prev].slice(0, 3))
        }
      } catch (err) {
        const errMsg: Message = {
          id: uuidv4(),
          role: 'assistant',
          content: `⚠️ Error: ${err instanceof Error ? err.message : 'Unknown error'}`,
          timestamp: new Date(),
        }
        setMessages((prev) => [...prev, errMsg])
      } finally {
        setIsTyping(false)
      }
    },
    [sessionId],
  )

  const resetChat = useCallback(async () => {
    if (!sessionId) return
    try {
      await resetSession(sessionId)
    } catch {}
    setMessages([{ ...WELCOME_MESSAGE, timestamp: new Date() }])
    setLastMigrations([])
  }, [sessionId])

  return { messages, isTyping, lastMigrations, sendMessage, resetChat, status }
}
