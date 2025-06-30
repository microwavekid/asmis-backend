// PATTERN_REF: ENTITY_SELECTION_PATTERN
// DECISION_REF: DEC_2025-06-27_001: Bonusly UI Pattern Integration

"use client"

import { Button } from "@/components/ui/button"
import { entityColors, EntityType } from "@/lib/utils/colors"
import { User, Building2, Target } from "lucide-react"
import { cn } from "@/lib/utils"

interface EntitySelectorButtonsProps {
  onEntityTypeSelect: (type: EntityType, trigger: string) => void
  activeType?: EntityType | null
  linkedEntityTypes?: EntityType[]
  className?: string
}

export function EntitySelectorButtons({ 
  onEntityTypeSelect, 
  activeType,
  linkedEntityTypes = [],
  className 
}: EntitySelectorButtonsProps) {
  const buttons = [
    {
      type: "stakeholder" as EntityType,
      icon: User,
      label: "Stakeholder",
      trigger: "@"
    },
    {
      type: "deal" as EntityType,
      icon: Target,
      label: "Deal", 
      trigger: "#"
    },
    {
      type: "account" as EntityType,
      icon: Building2,
      label: "Account",
      trigger: "+"
    }
  ]

  return (
    <div className={cn("flex gap-2", className)}>
      {buttons.map(({ type, icon: Icon, label, trigger }) => {
        const colors = entityColors[type]
        const isActive = activeType === type
        const hasLinkedEntities = linkedEntityTypes.includes(type)
        
        return (
          <button
            key={type}
            onClick={() => onEntityTypeSelect(type, trigger)}
            className={cn(
              "flex items-center gap-2 px-3 py-1.5 rounded-full border transition-all duration-200",
              "bg-gray-100 text-gray-700 border-gray-200",
              "hover:border-gray-300",
              isActive && `bg-${type === 'stakeholder' ? 'blue' : type === 'deal' ? 'purple' : 'green'}-500 text-white border-${type === 'stakeholder' ? 'blue' : type === 'deal' ? 'purple' : 'green'}-500`
            )}
            style={{
              backgroundColor: isActive ? colors.primary : undefined,
              borderColor: isActive ? colors.primary : undefined,
              color: isActive ? 'white' : undefined
            }}
            onMouseEnter={(e) => {
              if (!isActive) {
                e.currentTarget.style.backgroundColor = colors.primary
                e.currentTarget.style.borderColor = colors.primary
                e.currentTarget.style.color = 'white'
              }
            }}
            onMouseLeave={(e) => {
              if (!isActive) {
                e.currentTarget.style.backgroundColor = ''
                e.currentTarget.style.borderColor = ''
                e.currentTarget.style.color = ''
              }
            }}
          >
            <span className="text-sm font-medium">{trigger}</span>
            <span className="text-sm font-medium">{label}</span>
            {hasLinkedEntities && (
              <div className={cn(
                "w-2 h-2 rounded-full ml-1",
                `bg-${type === 'stakeholder' ? 'blue' : type === 'deal' ? 'purple' : 'green'}-500`
              )} 
              style={{
                backgroundColor: colors.primary
              }} />
            )}
          </button>
        )
      })}
    </div>
  )
}