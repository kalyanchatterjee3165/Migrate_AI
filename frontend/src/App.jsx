import { useState, useEffect } from 'react'
import Hero from './components/Hero'
import Sidebar from './components/Sidebar'
import ChatArea from './components/ChatArea'
import InputBar from './components/InputBar'
import { useChat } from './hooks/useChat'
import { getStatus } from './api/chat'
import './styles/global.css'

export default function App() {
  const [activeTab, setActiveTab] = useState('chat')
  const [status, setStatus] = useState({ model: 'gpt-4o', connected: false })
  const { messages, isTyping, sendMessage, resetSession } = useChat()

  useEffect(() => {
    getStatus().then(setStatus).catch(() => {})
  }, [])

  const lastAIMsg = messages.filter(m => m.role === 'ai').slice(-1)[0] ?? null

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <Hero activeTab={activeTab} onTabChange={setActiveTab} status={status} />
      <div style={{ display: 'grid', gridTemplateColumns: '220px 1fr', flex: 1, overflow: 'hidden' }}>
        <Sidebar
          onQuickStart={sendMessage}
          onReset={resetSession}
          lastMigration={lastAIMsg}
        />
        <main style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          <ChatArea messages={messages} isTyping={isTyping} />
          <InputBar onSend={sendMessage} disabled={isTyping} />
        </main>
      </div>
    </div>
  )
}
