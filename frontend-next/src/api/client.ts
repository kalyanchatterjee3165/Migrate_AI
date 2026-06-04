import type { ChatResponse, StatusResponse } from '@/types'

const BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })
  if (!res.ok) {
    let detail = res.statusText
    try {
      const body = await res.json()
      detail = body.detail ?? body.message ?? detail
    } catch {}
    throw new Error(detail)
  }
  return res.json() as Promise<T>
}

export async function sendChat(
  message: string,
  sessionId: string,
): Promise<ChatResponse> {
  return request<ChatResponse>('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ message, session_id: sessionId }),
  })
}

export async function resetSession(
  sessionId: string,
): Promise<{ status: string }> {
  return request<{ status: string }>('/api/reset', {
    method: 'POST',
    body: JSON.stringify({ session_id: sessionId }),
  })
}

export async function getStatus(): Promise<StatusResponse> {
  return request<StatusResponse>('/api/status')
}

export async function getOutputFiles(): Promise<{
  files: Array<{ filename: string; path: string; size_bytes: number }>
  count: number
}> {
  return request('/api/output')
}
