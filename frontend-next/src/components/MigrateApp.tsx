'use client'

import { useChat } from '@/hooks/useChat'
import Hero from './Hero'
import Sidebar from './Sidebar'
import ChatArea from './ChatArea'
import InputBar from './InputBar'

export default function MigrateApp() {
  const { messages, isTyping, lastMigrations, sendMessage, resetChat, status } = useChat()

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100vh',
        overflow: 'hidden',
      }}
    >
      <Hero status={status} />

      <div
        style={{
          display: 'flex',
          flex: 1,
          overflow: 'hidden',
          minHeight: 0,
        }}
      >
        <Sidebar
          lastMigrations={lastMigrations}
          onQuickStart={sendMessage}
          onReset={resetChat}
        />

        <main
          style={{
            display: 'flex',
            flexDirection: 'column',
            flex: 1,
            overflow: 'hidden',
            background: '#F4F4F4',
          }}
        >
          <ChatArea messages={messages} isTyping={isTyping} />
          <InputBar onSend={sendMessage} disabled={isTyping} />
        </main>
      </div>
    </div>
  )
}
