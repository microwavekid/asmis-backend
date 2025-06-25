"use client"

import { ChevronDown, Building2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export function WorkspaceSelector() {
  // In a real app, this would come from context/API
  const currentWorkspace = {
    name: "Optimizely Sales",
    plan: "Enterprise",
  }

  return (
    <div className="p-4 border-b border-[var(--bg-border)]">
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button 
            variant="ghost" 
            className="w-full justify-start gap-2 h-auto py-2 px-3 hover:bg-[var(--bg-border)]"
          >
            <div className="flex items-center justify-between w-full">
              <div className="flex items-center gap-3">
                <div className="p-1.5 bg-[var(--ai-processing)] rounded">
                  <Building2 className="h-4 w-4 text-white" />
                </div>
                <div className="text-left">
                  <div className="text-sm font-medium text-[var(--content-primary)]">
                    {currentWorkspace.name}
                  </div>
                  <div className="text-xs text-[var(--content-secondary)]">
                    {currentWorkspace.plan}
                  </div>
                </div>
              </div>
              <ChevronDown className="h-4 w-4 text-[var(--content-secondary)]" />
            </div>
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent 
          className="w-[var(--sidebar-width)]" 
          align="start"
        >
          <DropdownMenuLabel>Workspaces</DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuItem>
            <Building2 className="mr-2 h-4 w-4" />
            <span>Optimizely Sales</span>
          </DropdownMenuItem>
          <DropdownMenuItem>
            <Building2 className="mr-2 h-4 w-4" />
            <span>Test Workspace</span>
          </DropdownMenuItem>
          <DropdownMenuSeparator />
          <DropdownMenuItem>
            Create workspace
          </DropdownMenuItem>
          <DropdownMenuItem>
            Workspace settings
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  )
}