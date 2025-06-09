// Generate random sentiment data with trends
function generateTrendData(
  length = 30,
  startValue = 0,
  trendDirection: "up" | "down" | "stable" = "stable",
  volatility = 1,
): number[] {
  const data: number[] = []
  let value = startValue

  // Set trend bias based on direction
  const trendBias = trendDirection === "up" ? 0.2 : trendDirection === "down" ? -0.2 : 0

  for (let i = 0; i < length; i++) {
    // Add value to data array (rounded to 1 decimal place)
    data.push(Number.parseFloat(value.toFixed(1)))

    // Random change with trend bias
    const change = (Math.random() - 0.5) * volatility + trendBias
    value += change
  }

  return data
}

// Generate opportunity sentiment data
export const opportunitySentimentData = [
  {
    id: "opp-1",
    name: "Enterprise SaaS Implementation",
    data: generateTrendData(30, 65, "up", 1.5),
    get value() {
      return Number.parseFloat((this.data[this.data.length - 1] - this.data[0]).toFixed(1))
    },
    get type() {
      return this.value > 3 ? "positive" : this.value < -3 ? "negative" : "neutral"
    },
  },
  {
    id: "opp-2",
    name: "Cloud Migration Project",
    data: generateTrendData(30, 72, "up", 1.2),
    get value() {
      return Number.parseFloat((this.data[this.data.length - 1] - this.data[0]).toFixed(1))
    },
    get type() {
      return this.value > 3 ? "positive" : this.value < -3 ? "negative" : "neutral"
    },
  },
  {
    id: "opp-3",
    name: "Data Analytics Platform",
    data: generateTrendData(30, 58, "down", 1.8),
    get value() {
      return Number.parseFloat((this.data[this.data.length - 1] - this.data[0]).toFixed(1))
    },
    get type() {
      return this.value > 3 ? "positive" : this.value < -3 ? "negative" : "neutral"
    },
  },
  {
    id: "opp-4",
    name: "Security Infrastructure Upgrade",
    data: generateTrendData(30, 45, "down", 1.4),
    get value() {
      return Number.parseFloat((this.data[this.data.length - 1] - this.data[0]).toFixed(1))
    },
    get type() {
      return this.value > 3 ? "positive" : this.value < -3 ? "negative" : "neutral"
    },
  },
  {
    id: "opp-5",
    name: "Digital Transformation Initiative",
    data: generateTrendData(30, 78, "up", 1.3),
    get value() {
      return Number.parseFloat((this.data[this.data.length - 1] - this.data[0]).toFixed(1))
    },
    get type() {
      return this.value > 3 ? "positive" : this.value < -3 ? "negative" : "neutral"
    },
  },
  {
    id: "opp-6",
    name: "Mobile App Development",
    data: generateTrendData(30, 62, "stable", 1.6),
    get value() {
      return Number.parseFloat((this.data[this.data.length - 1] - this.data[0]).toFixed(1))
    },
    get type() {
      return this.value > 3 ? "positive" : this.value < -3 ? "negative" : "neutral"
    },
  },
  {
    id: "opp-7",
    name: "Legacy System Replacement",
    data: generateTrendData(30, 40, "down", 1.7),
    get value() {
      return Number.parseFloat((this.data[this.data.length - 1] - this.data[0]).toFixed(1))
    },
    get type() {
      return this.value > 3 ? "positive" : this.value < -3 ? "negative" : "neutral"
    },
  },
  {
    id: "opp-8",
    name: "AI Implementation Project",
    data: generateTrendData(30, 55, "up", 2.0),
    get value() {
      return Number.parseFloat((this.data[this.data.length - 1] - this.data[0]).toFixed(1))
    },
    get type() {
      return this.value > 3 ? "positive" : this.value < -3 ? "negative" : "neutral"
    },
  },
]

// Generate account sentiment data
export const accountSentimentData = [
  {
    id: "acc-1",
    name: "Acme Corp",
    data: generateTrendData(30, 70, "up", 1.5),
    get value() {
      return Number.parseFloat((this.data[this.data.length - 1] - this.data[0]).toFixed(1))
    },
    get type() {
      return this.value > 3 ? "positive" : this.value < -3 ? "negative" : "neutral"
    },
  },
  {
    id: "acc-2",
    name: "Globex Corporation",
    data: generateTrendData(30, 55, "down", 1.3),
    get value() {
      return Number.parseFloat((this.data[this.data.length - 1] - this.data[0]).toFixed(1))
    },
    get type() {
      return this.value > 3 ? "positive" : this.value < -3 ? "negative" : "neutral"
    },
  },
  {
    id: "acc-3",
    name: "Initech",
    data: generateTrendData(30, 42, "down", 1.4),
    get value() {
      return Number.parseFloat((this.data[this.data.length - 1] - this.data[0]).toFixed(1))
    },
    get type() {
      return this.value > 3 ? "positive" : this.value < -3 ? "negative" : "neutral"
    },
  },
  {
    id: "acc-4",
    name: "Wayne Enterprises",
    data: generateTrendData(30, 80, "up", 1.2),
    get value() {
      return Number.parseFloat((this.data[this.data.length - 1] - this.data[0]).toFixed(1))
    },
    get type() {
      return this.value > 3 ? "positive" : this.value < -3 ? "negative" : "neutral"
    },
  },
  {
    id: "acc-5",
    name: "Stark Industries",
    data: generateTrendData(30, 65, "stable", 1.6),
    get value() {
      return Number.parseFloat((this.data[this.data.length - 1] - this.data[0]).toFixed(1))
    },
    get type() {
      return this.value > 3 ? "positive" : this.value < -3 ? "negative" : "neutral"
    },
  },
  {
    id: "acc-6",
    name: "Umbrella Corporation",
    data: generateTrendData(30, 50, "down", 1.8),
    get value() {
      return Number.parseFloat((this.data[this.data.length - 1] - this.data[0]).toFixed(1))
    },
    get type() {
      return this.value > 3 ? "positive" : this.value < -3 ? "negative" : "neutral"
    },
  },
]
