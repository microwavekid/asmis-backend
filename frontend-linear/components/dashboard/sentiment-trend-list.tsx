"use client"

import { useState } from "react"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Sparkline } from "@/components/ui/sparkline"

interface SentimentTrendItem {
  id: string
  name: string
  data: number[]
  value: number
  type: "positive" | "neutral" | "negative"
}

interface SentimentTrendListProps {
  items: SentimentTrendItem[]
  title: string
}

export function SentimentTrendList({ items, title }: SentimentTrendListProps) {
  const [sortBy, setSortBy] = useState<"name" | "value">("value")

  const sortedItems = [...items].sort((a, b) => {
    if (sortBy === "name") {
      return a.name.localeCompare(b.name)
    } else {
      return Math.abs(b.value) - Math.abs(a.value) // Sort by absolute value
    }
  })

  const getSparklineColor = (value: number) => {
    if (value > 3) return "#10b981" // green for positive
    if (value < -3) return "#ef4444" // red for negative
    return "#6b7280" // gray for neutral
  }

  const getValueColor = (value: number) => {
    if (value > 3) return "text-green-600"
    if (value < -3) return "text-red-600"
    return "text-gray-600"
  }

  const formatValue = (value: number) => {
    // Always show the sign (+ or -) except for exactly 0
    return value > 0 ? `+${value}` : value.toString()
  }

  return (
    <div className="space-y-2">
      <div className="flex justify-between items-center">
        <h3 className="text-sm font-medium">{title}</h3>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setSortBy("name")}
            className={`text-xs px-2 py-1 rounded ${
              sortBy === "name" ? "bg-muted font-medium" : "text-muted-foreground"
            }`}
          >
            Name
          </button>
          <button
            onClick={() => setSortBy("value")}
            className={`text-xs px-2 py-1 rounded ${
              sortBy === "value" ? "bg-muted font-medium" : "text-muted-foreground"
            }`}
          >
            Change
          </button>
        </div>
      </div>
      <ScrollArea className="h-[300px]">
        <div className="space-y-0">
          {sortedItems.map((item) => (
            <div key={item.id} className="py-4 flex items-center justify-between border-b last:border-b-0">
              <div className="font-medium truncate max-w-[200px]">{item.name}</div>
              <div className="flex items-center gap-4">
                <div className={`text-sm font-medium ${getValueColor(item.value)}`}>{formatValue(item.value)}</div>
                <Sparkline data={item.data} color={getSparklineColor(item.value)} width={120} height={30} />
              </div>
            </div>
          ))}
        </div>
      </ScrollArea>
    </div>
  )
}
