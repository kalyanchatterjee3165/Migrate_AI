'use client'

import { useState, useEffect } from 'react'
import { v4 as uuidv4 } from 'uuid'

const SESSION_KEY = 'migrateai_session_id'

export function useSession(): { sessionId: string } {
  const [sessionId, setSessionId] = useState<string>('')

  useEffect(() => {
    const existing = sessionStorage.getItem(SESSION_KEY)
    if (existing) {
      setSessionId(existing)
    } else {
      const next = uuidv4()
      sessionStorage.setItem(SESSION_KEY, next)
      setSessionId(next)
    }
  }, [])

  return { sessionId }
}
