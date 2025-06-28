// PATTERN_REF: ENTITY_SELECTION_PATTERN
// DECISION_REF: DEC_2025-06-27_001: Bonusly UI Pattern Integration

export const entityColors = {
  stakeholder: {
    primary: "#3B82F6", // Blue
    background: "bg-blue-100",
    text: "text-blue-800",
    border: "border-blue-200",
    hover: "hover:bg-blue-200",
    selection: "bg-blue-500",
    selectionText: "text-white",
    trigger: "@"
  },
  account: {
    primary: "#10B981", // Green
    background: "bg-green-100",
    text: "text-green-800",
    border: "border-green-200", 
    hover: "hover:bg-green-200",
    selection: "bg-green-500",
    selectionText: "text-white",
    trigger: "+"
  },
  deal: {
    primary: "#8B5CF6", // Purple
    background: "bg-purple-100",
    text: "text-purple-800",
    border: "border-purple-200",
    hover: "hover:bg-purple-200",
    selection: "bg-purple-500",
    selectionText: "text-white",
    trigger: "#"
  },
  partner: {
    primary: "#F59E0B", // Orange
    background: "bg-orange-100",
    text: "text-orange-800",
    border: "border-orange-200",
    hover: "hover:bg-orange-200",
    selection: "bg-orange-500",
    selectionText: "text-white",
    trigger: "&"
  }
} as const

export type EntityType = keyof typeof entityColors

export function getEntityColor(type: EntityType, confidence: number) {
  const colors = entityColors[type]
  const opacity = confidence >= 0.8 ? "" : confidence >= 0.6 ? " opacity-80" : " opacity-60"
  return `${colors.background} ${colors.text} ${colors.border} ${colors.hover}${opacity}`
}

export function getEntitySelectionClasses(type: EntityType) {
  const colors = entityColors[type]
  return `${colors.selection} ${colors.selectionText}`
}