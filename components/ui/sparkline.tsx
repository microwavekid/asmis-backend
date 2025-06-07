"use client"

import { useEffect, useState } from "react"

interface SparklineProps {
  data: number[]
  color?: string
  height?: number
  width?: number
  showEndPoints?: boolean
}

export function Sparkline({ data, color = "#f87171", height = 30, width = 120, showEndPoints = true }: SparklineProps) {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return <div style={{ height, width }} />

  // Find min and max values for scaling
  const min = Math.min(...data)
  const max = Math.max(...data)
  const range = max - min || 1 // Avoid division by zero

  // Calculate the middle point for the zero line (if needed)
  const hasNegative = min < 0
  const hasPositive = max > 0
  const zeroY = hasNegative && hasPositive ? height - ((0 - min) / range) * height : null

  // Calculate points for the path
  const points = data.map((value, index) => {
    const x = (index / (data.length - 1)) * width
    const y = height - ((value - min) / range) * height
    return `${x},${y}`
  })

  // Create the SVG path
  const path = `M ${points.join(" L ")}`

  return (
    <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} fill="none" style={{ display: "block" }}>
      {/* Optional zero line */}
      {zeroY !== null && (
        <line x1="0" y1={zeroY} x2={width} y2={zeroY} stroke="#e5e7eb" strokeWidth="1" strokeDasharray="2,2" />
      )}

      <path d={path} stroke={color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none" />

      {showEndPoints && (
        <>
          {/* Start point */}
          <circle cx={0} cy={height - ((data[0] - min) / range) * height} r="2.5" fill={color} />

          {/* End point */}
          <circle cx={width} cy={height - ((data[data.length - 1] - min) / range) * height} r="2.5" fill={color} />
        </>
      )}
    </svg>
  )
}
