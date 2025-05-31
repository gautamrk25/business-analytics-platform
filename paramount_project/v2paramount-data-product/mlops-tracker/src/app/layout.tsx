export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen">
          <header className="h-16 bg-white border-b border-gray-200">
            Header Content
          </header>
          {children}
        </div>
      </body>
    </html>
  )
} 