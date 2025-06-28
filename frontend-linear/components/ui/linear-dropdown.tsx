"use client"

import * as React from "react"
import { Check, ChevronDown, Search } from "lucide-react"
import { cn } from "@/lib/utils"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import { Input } from "@/components/ui/input"

export interface DropdownOption {
  id: string
  name: string
  subtitle?: string
  metadata?: string
  icon?: React.ReactNode
}

interface LinearDropdownProps {
  value?: string
  onValueChange?: (value: string) => void
  options: DropdownOption[]
  placeholder?: string
  searchPlaceholder?: string
  className?: string
  buttonClassName?: string
  disabled?: boolean
  loading?: boolean
}

export function LinearDropdown({
  value,
  onValueChange,
  options,
  placeholder = "Select...",
  searchPlaceholder = "Search...",
  className,
  buttonClassName,
  disabled = false,
  loading = false,
}: LinearDropdownProps) {
  const [open, setOpen] = React.useState(false)
  const [search, setSearch] = React.useState("")
  const inputRef = React.useRef<HTMLInputElement>(null)

  const selectedOption = options.find(opt => opt.id === value)

  const filteredOptions = React.useMemo(() => {
    if (!search) return options
    const searchLower = search.toLowerCase()
    return options.filter(opt => 
      opt.name.toLowerCase().includes(searchLower) ||
      opt.subtitle?.toLowerCase().includes(searchLower)
    )
  }, [options, search])

  React.useEffect(() => {
    if (open && inputRef.current) {
      // Focus search input when dropdown opens
      setTimeout(() => inputRef.current?.focus(), 0)
    }
  }, [open])

  const handleSelect = (optionId: string) => {
    onValueChange?.(optionId)
    setOpen(false)
    setSearch("")
  }

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <button
          className={cn(
            "inline-flex items-center gap-1.5 px-2.5 py-1.5 text-sm font-medium rounded-md",
            "bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700",
            "text-gray-700 dark:text-gray-300",
            "transition-colors cursor-pointer",
            "focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500",
            disabled && "opacity-50 cursor-not-allowed",
            buttonClassName
          )}
          disabled={disabled}
        >
          {loading ? (
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-gray-500 border-t-transparent" />
          ) : (
            <>
              {selectedOption?.icon}
              <span className="max-w-[120px] truncate">
                {selectedOption?.name || placeholder}
              </span>
              <ChevronDown className="h-3 w-3 opacity-50" />
            </>
          )}
        </button>
      </PopoverTrigger>
      <PopoverContent 
        className={cn("w-64 p-0", className)} 
        align="start"
        sideOffset={4}
      >
        <div className="p-1.5 border-b">
          <div className="relative">
            <Search className="absolute left-2 top-2.5 h-4 w-4 text-gray-400" />
            <Input
              ref={inputRef}
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder={searchPlaceholder}
              className="h-9 pl-8 pr-3 text-sm border-0 focus:ring-0"
            />
          </div>
        </div>
        <div className="max-h-64 overflow-y-auto p-1">
          {filteredOptions.length === 0 ? (
            <div className="px-2 py-6 text-center text-sm text-gray-500">
              No results found
            </div>
          ) : (
            filteredOptions.map((option) => (
              <button
                key={option.id}
                onClick={() => handleSelect(option.id)}
                className={cn(
                  "w-full flex items-center gap-2 px-2 py-1.5 text-sm rounded",
                  "hover:bg-gray-100 dark:hover:bg-gray-800",
                  "transition-colors text-left",
                  value === option.id && "bg-gray-100 dark:bg-gray-800"
                )}
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    {option.icon}
                    <span className="font-medium truncate">{option.name}</span>
                  </div>
                  {option.subtitle && (
                    <div className="text-xs text-gray-500 truncate">
                      {option.subtitle}
                    </div>
                  )}
                </div>
                {value === option.id && (
                  <Check className="h-4 w-4 text-blue-600 flex-shrink-0" />
                )}
              </button>
            ))
          )}
        </div>
      </PopoverContent>
    </Popover>
  )
}