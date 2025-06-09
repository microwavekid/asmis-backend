"use client"

import { useEffect, useState } from "react"
import { Sparkline, SparklineChart, SparklinePoint } from "@/components/ui/chart"

interface SentimentSparklineProps {
  data: number[]
  type: "positive" | "neutral" | "negative"
  height?: number
  showPoint?: boolean
}

export function SentimentSparkline({ data, type, height = 24, showPoint = true }: SentimentSparklineProps) {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return <div style={{ height }} />

  const getColor = () => {
    switch (type) {
      case "positive":
        return "var(--chart-positive, hsl(142.1 76.2% 36.3%))"
      case "negative":
        return "var(--chart-negative, hsl(0 84.2% 60.2%))"
      case "neutral":
      default:
        return "var(--chart-neutral, hsl(215.4 16.3% 46.9%))"
    }
  }

  const color = getColor()

  return (
    <SparklineChart
      data={data}
      height={height}
      config={{
        value: {
          color,
        },
      }}
    >
      <Sparkline dataKey="value" />
      {showPoint && <SparklinePoint dataKey="value" />}
    </SparklineChart>
  )
}
