"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Calendar } from "@/components/ui/calendar"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { CalendarIcon, Filter, Search, X } from "lucide-react"
import { format } from "date-fns"
import { cn } from "@/lib/utils"

interface EmailKanbanFiltersProps {
  filters: {
    account: string
    opportunity: string
    priority: string
    dateRange: {
      from: Date | undefined
      to: Date | undefined
    }
    search: string
  }
  setFilters: React.Dispatch<
    React.SetStateAction<{
      account: string
      opportunity: string
      priority: string
      dateRange: {
        from: Date | undefined
        to: Date | undefined
      }
      search: string
    }>
  >
  accounts: any[]
  opportunities: any[]
}

export function EmailKanbanFilters({ filters, setFilters, accounts, opportunities }: EmailKanbanFiltersProps) {
  const [isSearchOpen, setIsSearchOpen] = useState(false)

  const handleClearFilters = () => {
    setFilters({
      account: "",
      opportunity: "",
      priority: "",
      dateRange: {
        from: undefined,
        to: undefined,
      },
      search: "",
    })
  }

  const hasActiveFilters =
    filters.account !== "" ||
    filters.opportunity !== "" ||
    filters.priority !== "" ||
    filters.dateRange.from !== undefined ||
    filters.dateRange.to !== undefined ||
    filters.search !== ""

  return (
    <div className="flex items-center gap-2">
      {isSearchOpen ? (
        <div className="flex items-center gap-2">
          <Input
            placeholder="Search emails..."
            value={filters.search}
            onChange={(e) => setFilters((prev) => ({ ...prev, search: e.target.value }))}
            className="w-64"
          />
          <Button
            variant="ghost"
            size="icon"
            onClick={() => {
              setFilters((prev) => ({ ...prev, search: "" }))
              setIsSearchOpen(false)
            }}
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      ) : (
        <Button variant="outline" size="icon" onClick={() => setIsSearchOpen(true)}>
          <Search className="h-4 w-4" />
        </Button>
      )}

      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button variant="outline" className="gap-2">
            <Filter className="h-4 w-4" />
            <span>Filter</span>
            {hasActiveFilters && <span className="flex h-2 w-2 rounded-full bg-primary"></span>}
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end" className="w-[240px]">
          <DropdownMenuLabel>Filter Emails</DropdownMenuLabel>
          <DropdownMenuSeparator />

          <div className="p-2">
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-xs font-medium">Account</label>
                <Select
                  value={filters.account}
                  onValueChange={(value) => setFilters((prev) => ({ ...prev, account: value }))}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="All accounts" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All accounts</SelectItem>
                    {accounts.map((account) => (
                      <SelectItem key={account.id} value={account.id}>
                        {account.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <label className="text-xs font-medium">Opportunity</label>
                <Select
                  value={filters.opportunity}
                  onValueChange={(value) => setFilters((prev) => ({ ...prev, opportunity: value }))}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="All opportunities" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All opportunities</SelectItem>
                    {opportunities.map((opportunity) => (
                      <SelectItem key={opportunity.id} value={opportunity.id}>
                        {opportunity.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <label className="text-xs font-medium">Priority</label>
                <Select
                  value={filters.priority}
                  onValueChange={(value) => setFilters((prev) => ({ ...prev, priority: value }))}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="All priorities" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All priorities</SelectItem>
                    <SelectItem value="high">High</SelectItem>
                    <SelectItem value="medium">Medium</SelectItem>
                    <SelectItem value="low">Low</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <label className="text-xs font-medium">Date Range</label>
                <div className="grid gap-2">
                  <Popover>
                    <PopoverTrigger asChild>
                      <Button
                        variant="outline"
                        className={cn(
                          "justify-start text-left font-normal",
                          !filters.dateRange.from && "text-muted-foreground",
                        )}
                      >
                        <CalendarIcon className="mr-2 h-4 w-4" />
                        {filters.dateRange.from ? format(filters.dateRange.from, "PPP") : <span>From date</span>}
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0">
                      <Calendar
                        mode="single"
                        selected={filters.dateRange.from}
                        onSelect={(date) =>
                          setFilters((prev) => ({
                            ...prev,
                            dateRange: { ...prev.dateRange, from: date },
                          }))
                        }
                        initialFocus
                      />
                    </PopoverContent>
                  </Popover>

                  <Popover>
                    <PopoverTrigger asChild>
                      <Button
                        variant="outline"
                        className={cn(
                          "justify-start text-left font-normal",
                          !filters.dateRange.to && "text-muted-foreground",
                        )}
                      >
                        <CalendarIcon className="mr-2 h-4 w-4" />
                        {filters.dateRange.to ? format(filters.dateRange.to, "PPP") : <span>To date</span>}
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0">
                      <Calendar
                        mode="single"
                        selected={filters.dateRange.to}
                        onSelect={(date) =>
                          setFilters((prev) => ({
                            ...prev,
                            dateRange: { ...prev.dateRange, to: date },
                          }))
                        }
                        initialFocus
                      />
                    </PopoverContent>
                  </Popover>
                </div>
              </div>
            </div>
          </div>

          <DropdownMenuSeparator />
          <DropdownMenuItem
            onClick={handleClearFilters}
            disabled={!hasActiveFilters}
            className="justify-center text-center"
          >
            Clear all filters
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  )
}
