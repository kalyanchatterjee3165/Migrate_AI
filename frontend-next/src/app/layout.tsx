import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'MigrateAI',
  description: 'Conversational data migration powered by GPT-4o',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" style={{ height: '100%', overflow: 'hidden' }}>
      <body style={{ height: '100%', margin: 0, padding: 0, overflow: 'hidden' }}>
        {children}
      </body>
    </html>
  )
}
