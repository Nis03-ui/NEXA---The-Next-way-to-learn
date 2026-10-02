import type { Metadata } from "next"
import "./globals.css"
import { AuthProvider } from "@/providers/AuthProvider"

export const metadata: Metadata = {
  title: "NEXA — The Next Way to Learn",
  description:
    "NEXA is an intelligent AI study companion that helps students understand, practice, and learn better.",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}