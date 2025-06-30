// PATTERN_REF: FRONTEND_ROUTING_PATTERN
// DECISION_REF: DEC_2025-06-24_003: Root layout for v0 intelligence UI

import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import { ThemeProvider } from "@/components/theme-provider"
import { QueryProvider } from "@/components/providers/query-provider"
import { SidebarProvider } from "@/components/ui/sidebar"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "ASMIS Intelligence Platform",
  description: "AI-powered sales intelligence and deal insights",
  generator: 'v0.dev'
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <QueryProvider>
          <ThemeProvider attribute="class" defaultTheme="light" enableSystem disableTransitionOnChange>
            <SidebarProvider>
              {children}
            </SidebarProvider>
          </ThemeProvider>
        </QueryProvider>
      </body>
    </html>
  )
}