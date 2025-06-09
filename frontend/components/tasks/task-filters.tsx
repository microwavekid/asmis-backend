"use client"

import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { ChevronDown } from "lucide-react"

interface TaskFiltersProps {
  groupBy: string
  onGroupByChange: (value: any) => void
}

export function TaskFilters({ groupBy, onGroupByChange }: TaskFiltersProps) {
  return (
    <div className="flex flex-wrap items-center gap-4">
      <div>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="gap-1">
              Group by: {formatGroupByLabel(groupBy)}
              <ChevronDown className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="start" className="w-56">
            <DropdownMenuRadioGroup value={groupBy} onValueChange={onGroupByChange}>
              <DropdownMenuRadioItem value="effort">Effort Level</DropdownMenuRadioItem>
              <DropdownMenuRadioItem value="account">Account</DropdownMenuRadioItem>
              <DropdownMenuRadioItem value="opportunity">Opportunity</DropdownMenuRadioItem>
              <DropdownMenuRadioItem value="dueDate">Due Date</DropdownMenuRadioItem>
              <DropdownMenuRadioItem value="priority">Priority</DropdownMenuRadioItem>
              <DropdownMenuRadioItem value="type">Task Type</DropdownMenuRadioItem>
            </DropdownMenuRadioGroup>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </div>
  )
}

function formatGroupByLabel(groupBy: string): string {
  switch (groupBy) {
    case "effort":
      return "Effort Level"
    case "account":
      return "Account"
    case "opportunity":
      return "Opportunity"
    case "dueDate":
      return "Due Date"
    case "priority":
      return "Priority"
    case "type":
      return "Task Type"
    default:
      return groupBy
  }
}
