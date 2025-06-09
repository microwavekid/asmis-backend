"use client"

import { useEffect, useState } from "react"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts"

export function GlobalSentimentChart() {
  // Mock data for sentiment trends
  const data = [
    { month: "Jan", positive: 65, neutral: 28, negative: 7 },
    { month: "Feb", positive: 59, neutral: 32, negative: 9 },
    { month: "Mar", positive: 80, neutral: 13, negative: 7 },
    { month: "Apr", positive: 81, neutral: 15, negative: 4 },
    { month: "May", positive: 56, neutral: 37, negative: 7 },
    { month: "Jun", positive: 55, neutral: 30, negative: 15 },
    { month: "Jul", positive: 40, neutral: 43, negative: 17 },
  ]

  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return <div className="h-[300px] flex items-center justify-center">Loading chart...</div>

  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={data} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="positive" stroke="#10b981" strokeWidth={2} />
        <Line type="monotone" dataKey="neutral" stroke="#6b7280" strokeWidth={2} />
        <Line type="monotone" dataKey="negative" stroke="#ef4444" strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  )
}
