export async function sendMessage(message) {
  const res = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  })
  if (!res.ok) throw new Error(`Chat error ${res.status}`)
  return res.json()
}

export async function resetSession() {
  const res = await fetch('/api/reset', { method: 'POST' })
  if (!res.ok) throw new Error(`Reset error ${res.status}`)
  return res.json()
}

export async function getStatus() {
  const res = await fetch('/api/status')
  if (!res.ok) throw new Error(`Status error ${res.status}`)
  return res.json()
}

export async function getOutputFiles() {
  const res = await fetch('/api/output')
  if (!res.ok) throw new Error(`Output error ${res.status}`)
  return res.json()
}
