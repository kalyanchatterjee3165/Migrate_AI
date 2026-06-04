export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  configCard?: ConfigCardData
  timestamp: Date
}

export interface ConfigCardData {
  title: string
  rows: { key: string; value: string }[]
}

export interface LastMigration {
  label: string
  detail: string
  time: string
}

export interface StatusResponse {
  model: string
  connected: boolean
  active_sessions: number
}

export interface ChatResponse {
  reply: string
  session_id: string
}
