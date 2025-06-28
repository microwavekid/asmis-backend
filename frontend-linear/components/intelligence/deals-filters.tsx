// PATTERN_REF: FRONTEND_ROUTING_PATTERN  
// DECISION_REF: DEC_2025-06-24_008: Deals filtering and search controls

"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { 
  Search,
  Filter,
  X,
  SlidersHorizontal
} from "lucide-react"

export interface FilterState {
  search: string
  stage: string[]
  healthBand: string[]
  valueBand: string[]
  priority: string[]
}

interface DealsFiltersProps {
  filters: FilterState
  onFiltersChange: (filters: FilterState) => void
  onClearFilters: () => void
}

const STAGE_OPTIONS = [
  "Discovery",
  "Technical Evaluation", 
  "Negotiation",
  "Closing",
  "Closed Won",
  "Closed Lost"
]

const HEALTH_BAND_OPTIONS = [
  { value: "high", label: "High (80%+)", color: "bg-[var(--confidence-high)]/20 text-[var(--confidence-high)]" },
  { value: "medium", label: "Medium (60-80%)", color: "bg-[var(--confidence-medium)]/20 text-[var(--confidence-medium)]" },
  { value: "low", label: "Low (<60%)", color: "bg-[var(--confidence-low)]/20 text-[var(--confidence-low)]" }
]

const VALUE_BAND_OPTIONS = [
  { value: "0-100k", label: "$0-100K" },
  { value: "100k-500k", label: "$100K-500K" },
  { value: "500k+", label: "$500K+" }
]

const PRIORITY_OPTIONS = [
  { value: "high", label: "High", color: "bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400" },
  { value: "medium", label: "Medium", color: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400" },
  { value: "low", label: "Low", color: "bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400" }
]

export function DealsFilters({ filters, onFiltersChange, onClearFilters }: DealsFiltersProps) {
  const [showFilters, setShowFilters] = useState(false)

  const updateFilters = (key: keyof FilterState, value: any) => {
    onFiltersChange({
      ...filters,
      [key]: value
    })
  }

  const toggleArrayFilter = (key: keyof FilterState, value: string) => {
    const currentArray = filters[key] as string[]
    const newArray = currentArray.includes(value)
      ? currentArray.filter(item => item !== value)
      : [...currentArray, value]
    
    updateFilters(key, newArray)
  }

  const hasActiveFilters = 
    filters.search.length > 0 ||
    filters.stage.length > 0 ||
    filters.healthBand.length > 0 ||
    filters.valueBand.length > 0 ||
    filters.priority.length > 0

  const activeFilterCount = 
    filters.stage.length + 
    filters.healthBand.length + 
    filters.valueBand.length + 
    filters.priority.length

  return (
    <div className="space-y-4">
      {/* Search and Filter Toggle */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
        <div className="relative flex-1 sm:max-w-sm lg:max-w-md">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-[var(--content-secondary)]" />
          <Input
            placeholder="Search deals..."
            value={filters.search}
            onChange={(e) => updateFilters('search', e.target.value)}
            className="pl-10 h-9"
          />
        </div>
        
        <div className="flex items-center gap-2">
        
        <Button
          variant={showFilters ? "secondary" : "outline"}
          size="sm"
          onClick={() => setShowFilters(!showFilters)}
          className="flex items-center gap-2"
        >
          <SlidersHorizontal className="h-4 w-4" />
          Filters
          {activeFilterCount > 0 && (
            <Badge variant="secondary" className="ml-1 text-xs">
              {activeFilterCount}
            </Badge>
          )}
        </Button>

        {hasActiveFilters && (
          <Button
            variant="ghost"
            size="sm"
            onClick={onClearFilters}
            className="text-[var(--content-secondary)] hover:text-[var(--content-primary)]"
          >
            <X className="h-4 w-4 mr-1" />
            Clear
          </Button>
        )}
        </div>
      </div>

      {/* Active Filters Display */}
      {hasActiveFilters && (
        <div className="flex flex-wrap gap-2">
          {filters.search && (
            <Badge variant="secondary" className="flex items-center gap-1">
              Search: "{filters.search}"
              <button 
                onClick={() => updateFilters('search', '')}
                className="ml-1 hover:bg-[var(--bg-border)] rounded-full p-0.5"
              >
                <X className="h-3 w-3" />
              </button>
            </Badge>
          )}
          
          {filters.stage.map(stage => (
            <Badge key={stage} variant="secondary" className="flex items-center gap-1">
              Stage: {stage}
              <button 
                onClick={() => toggleArrayFilter('stage', stage)}
                className="ml-1 hover:bg-[var(--bg-border)] rounded-full p-0.5"
              >
                <X className="h-3 w-3" />
              </button>
            </Badge>
          ))}

          {filters.healthBand.map(band => (
            <Badge key={band} variant="secondary" className="flex items-center gap-1">
              Health: {HEALTH_BAND_OPTIONS.find(h => h.value === band)?.label}
              <button 
                onClick={() => toggleArrayFilter('healthBand', band)}
                className="ml-1 hover:bg-[var(--bg-border)] rounded-full p-0.5"
              >
                <X className="h-3 w-3" />
              </button>
            </Badge>
          ))}

          {filters.valueBand.map(band => (
            <Badge key={band} variant="secondary" className="flex items-center gap-1">
              Value: {VALUE_BAND_OPTIONS.find(v => v.value === band)?.label}
              <button 
                onClick={() => toggleArrayFilter('valueBand', band)}
                className="ml-1 hover:bg-[var(--bg-border)] rounded-full p-0.5"
              >
                <X className="h-3 w-3" />
              </button>
            </Badge>
          ))}

          {filters.priority.map(priority => (
            <Badge key={priority} variant="secondary" className="flex items-center gap-1">
              Priority: {priority}
              <button 
                onClick={() => toggleArrayFilter('priority', priority)}
                className="ml-1 hover:bg-[var(--bg-border)] rounded-full p-0.5"
              >
                <X className="h-3 w-3" />
              </button>
            </Badge>
          ))}
        </div>
      )}

      {/* Filter Panel */}
      {showFilters && (
        <div className="p-3 lg:p-4 bg-[var(--bg-subtle)] rounded-lg border border-[var(--bg-border)]">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 lg:gap-4">
            {/* Stage Filter */}
            <div>
              <label className="text-sm font-medium text-[var(--content-primary)] mb-2 block">
                Stage
              </label>
              <div className="space-y-2">
                {STAGE_OPTIONS.map(stage => (
                  <label key={stage} className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      checked={filters.stage.includes(stage)}
                      onChange={() => toggleArrayFilter('stage', stage)}
                      className="rounded border-[var(--bg-border)]"
                    />
                    <span className="text-sm text-[var(--content-secondary)]">{stage}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Health Band Filter */}
            <div>
              <label className="text-sm font-medium text-[var(--content-primary)] mb-2 block">
                Health
              </label>
              <div className="space-y-2">
                {HEALTH_BAND_OPTIONS.map(health => (
                  <label key={health.value} className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      checked={filters.healthBand.includes(health.value)}
                      onChange={() => toggleArrayFilter('healthBand', health.value)}
                      className="rounded border-[var(--bg-border)]"
                    />
                    <span className="text-sm text-[var(--content-secondary)]">{health.label}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Value Band Filter */}
            <div>
              <label className="text-sm font-medium text-[var(--content-primary)] mb-2 block">
                Deal Value
              </label>
              <div className="space-y-2">
                {VALUE_BAND_OPTIONS.map(value => (
                  <label key={value.value} className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      checked={filters.valueBand.includes(value.value)}
                      onChange={() => toggleArrayFilter('valueBand', value.value)}
                      className="rounded border-[var(--bg-border)]"
                    />
                    <span className="text-sm text-[var(--content-secondary)]">{value.label}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Priority Filter */}
            <div>
              <label className="text-sm font-medium text-[var(--content-primary)] mb-2 block">
                Priority
              </label>
              <div className="space-y-2">
                {PRIORITY_OPTIONS.map(priority => (
                  <label key={priority.value} className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      checked={filters.priority.includes(priority.value)}
                      onChange={() => toggleArrayFilter('priority', priority.value)}
                      className="rounded border-[var(--bg-border)]"
                    />
                    <span className="text-sm text-[var(--content-secondary)]">{priority.label}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}