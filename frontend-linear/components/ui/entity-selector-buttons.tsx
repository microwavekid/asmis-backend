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
          <Button
            key={type}
            variant="ghost"
            size="default"
            onClick={() => onEntityTypeSelect(type, trigger)}
            className={cn(
              "flex items-center gap-2 transition-all duration-200 relative border-0 px-3 py-2",
              isActive && `${colors.background} ${colors.text}`,
              !isActive && hasLinkedEntities && `${colors.background} ${colors.text}`,
              !isActive && !hasLinkedEntities && `hover:bg-gray-100`
            )}
            style={{
              backgroundColor: isActive || hasLinkedEntities 
                ? colors.primary + '20'
                : undefined
            }}
            onMouseEnter={(e) => {
              if (!isActive && !hasLinkedEntities) {
                e.currentTarget.style.backgroundColor = colors.primary + '10'
                e.currentTarget.style.color = colors.primary
              }
            }}
            onMouseLeave={(e) => {
              if (!isActive && !hasLinkedEntities) {
                e.currentTarget.style.backgroundColor = ''
                e.currentTarget.style.color = ''
              }
            }}
          >
            <div className="relative">
              <div className={cn(
                "w-6 h-6 rounded-full flex items-center justify-center",
                isActive || hasLinkedEntities ? "bg-white" : "bg-gray-200"
              )}>
                <span className={cn(
                  "text-sm font-medium transition-colors duration-200",
                  isActive || hasLinkedEntities ? colors.text : "text-gray-600"
                )}>{trigger}</span>
              </div>
            </div>
            <span className={cn(
              "text-base font-medium transition-colors duration-200",
              isActive || hasLinkedEntities ? colors.text : "text-gray-700"
            )}>{label}</span>
            {hasLinkedEntities && !isActive && (
              <div className={cn(
                "absolute -top-1 -right-1 w-2 h-2 rounded-full",
                colors.selection
              )} />
            )}
          </Button>
        )
      })}
    </div>
  )
}