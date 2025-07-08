// PATTERN_REF: LINEAR_UI_PATTERN
// DECISION_REF: DEC_2025-06-24_008: Linear-style views dropdown

"use client"

import { useState } from "react"
import { 
  Target, 
  Plus, 
  Check,
  Filter,
  SortAsc,
  Eye,
  Star,
  Clock,
  TrendingUp
} from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

interface View {
  id: string
  name: string
  icon: React.ElementType
  filter?: string
  isDefault?: boolean
}

const defaultViews: View[] = [
  { id: "all", name: "All Deals", icon: Target, isDefault: true },
  { id: "my-deals", name: "My Deals", icon: Eye },
  { id: "high-value", name: "High Value", icon: TrendingUp, filter: "value > 100000" },
  { id: "closing-soon", name: "Closing Soon", icon: Clock, filter: "closeDate < 30d" },
  { id: "starred", name: "Starred", icon: Star, filter: "starred = true" },
]

interface ViewsDropdownProps {
  currentView: string
  onViewChange: (viewId: string) => void
  onCreateView: () => void
}

export function ViewsDropdown({ currentView, onViewChange, onCreateView }: ViewsDropdownProps) {
  const [views] = useState<View[]>(defaultViews)
  const selectedView = views.find(v => v.id === currentView) || views[0]

  return (
    <div className="flex items-center gap-2">
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button
            variant="ghost"
            size="sm"
            className="h-7 px-3 gap-2 border border-[var(--bg-border)] hover:bg-[var(--bg-border)]/50"
          >
            <selectedView.icon className="h-3.5 w-3.5" />
            <span className="text-sm">{selectedView.name}</span>
          </Button>
        </DropdownMenuTrigger>
        {/* PATTERN_REF: DROPDOWN_POSITIONING_PATTERN - Use proper collision detection */}
        <DropdownMenuContent 
          align="start" 
          side="bottom"
          sideOffset={8} 
          collisionPadding={16}
          className="w-56"
        >
          <DropdownMenuLabel className="text-xs text-[var(--content-secondary)]">
            Views
          </DropdownMenuLabel>
          <DropdownMenuSeparator />
          {views.map((view) => {
            const Icon = view.icon
            return (
              <DropdownMenuItem
                key={view.id}
                onClick={() => onViewChange(view.id)}
                className="gap-2"
              >
                <Icon className="h-4 w-4" />
                <span className="flex-1">{view.name}</span>
                {currentView === view.id && (
                  <Check className="h-4 w-4 text-[var(--ai-processing)]" />
                )}
              </DropdownMenuItem>
            )
          })}
          <DropdownMenuSeparator />
          <DropdownMenuItem onClick={onCreateView} className="gap-2">
            <Plus className="h-4 w-4" />
            <span>Create view</span>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
      
      {/* New View Button */}
      <Button
        variant="ghost"
        size="sm"
        className="h-7 px-3 gap-2 text-[var(--content-secondary)] hover:text-[var(--content-primary)]"
        onClick={onCreateView}
      >
        <Plus className="h-3.5 w-3.5" />
        <span className="text-sm">New view</span>
      </Button>
    </div>
  )
}