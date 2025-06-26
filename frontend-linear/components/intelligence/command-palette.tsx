"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandShortcut,
} from "@/components/ui/command"
import {
  Building2,
  Target,
  FileText,
  Brain,
  Upload,
  Mail,
  Phone,
  Calculator,
  Search,
  Settings,
  Clock,
  Zap,
  PenTool,
} from "lucide-react"

interface CommandPaletteProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSmartCaptureOpen?: () => void
}

// Mock data for search results
const mockAccounts = [
  { id: "1", name: "Optimizely Enterprise", shortcut: "1" },
  { id: "2", name: "Stripe Payments", shortcut: "2" },
  { id: "3", name: "Linear Software", shortcut: "3" },
]

const mockDeals = [
  { id: "d1", name: "Enterprise Implementation", account: "Optimizely" },
  { id: "d2", name: "Payment Integration", account: "Stripe" },
  { id: "d3", name: "Team Expansion", account: "Linear" },
]

export function CommandPalette({ open, onOpenChange, onSmartCaptureOpen }: CommandPaletteProps) {
  const router = useRouter()
  const [searchValue, setSearchValue] = useState("")

  // Handle keyboard shortcuts
  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault()
        onOpenChange(!open)
      }
      
      if (e.key === "u" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault()
        onOpenChange(false)
        onSmartCaptureOpen?.()
      }
      
      if (e.key === "Escape") {
        onOpenChange(false)
      }
    }

    document.addEventListener("keydown", down)
    return () => document.removeEventListener("keydown", down)
  }, [open, onOpenChange, onSmartCaptureOpen])

  const runCommand = (command: () => void) => {
    onOpenChange(false)
    command()
  }

  return (
    <CommandDialog 
      open={open} 
      onOpenChange={onOpenChange}
      className="max-w-[640px]"
    >
      <CommandInput 
        placeholder="Search or type a command..." 
        value={searchValue}
        onValueChange={setSearchValue}
      />
      <CommandList>
        <CommandEmpty>
          No results found for "{searchValue}"
        </CommandEmpty>
        
        {/* Quick Actions */}
        <CommandGroup heading="Quick Actions">
          <CommandItem onSelect={() => runCommand(() => onSmartCaptureOpen?.())}>
            <PenTool className="mr-2 h-4 w-4" />
            <span>Smart Capture</span>
            <CommandShortcut>⌘U</CommandShortcut>
          </CommandItem>
          <CommandItem onSelect={() => runCommand(() => router.push("/intelligence/upload"))}>
            <Upload className="mr-2 h-4 w-4" />
            <span>Upload transcript</span>
            <CommandShortcut>⌘T</CommandShortcut>
          </CommandItem>
          <CommandItem onSelect={() => runCommand(() => router.push("/intelligence/email-connect"))}>
            <Mail className="mr-2 h-4 w-4" />
            <span>Connect email</span>
            <CommandShortcut>⌘E</CommandShortcut>
          </CommandItem>
          <CommandItem onSelect={() => runCommand(() => console.log("Generate MEDDPICC"))}>
            <Brain className="mr-2 h-4 w-4" />
            <span>Generate MEDDPICC analysis</span>
            <CommandShortcut>⌘M</CommandShortcut>
          </CommandItem>
          <CommandItem onSelect={() => runCommand(() => console.log("Calculate ROI"))}>
            <Calculator className="mr-2 h-4 w-4" />
            <span>Calculate ROI</span>
            <CommandShortcut>⌘R</CommandShortcut>
          </CommandItem>
        </CommandGroup>

        {/* Navigation */}
        <CommandGroup heading="Navigation">
          <CommandItem onSelect={() => runCommand(() => router.push("/intelligence/accounts"))}>
            <Building2 className="mr-2 h-4 w-4" />
            <span>Go to Accounts</span>
            <CommandShortcut>G A</CommandShortcut>
          </CommandItem>
          <CommandItem onSelect={() => runCommand(() => router.push("/intelligence/deals"))}>
            <Target className="mr-2 h-4 w-4" />
            <span>Go to Deals</span>
            <CommandShortcut>G D</CommandShortcut>
          </CommandItem>
          <CommandItem onSelect={() => runCommand(() => router.push("/intelligence/evidence"))}>
            <FileText className="mr-2 h-4 w-4" />
            <span>Go to Evidence</span>
            <CommandShortcut>G E</CommandShortcut>
          </CommandItem>
          <CommandItem onSelect={() => runCommand(() => router.push("/intelligence/insights"))}>
            <Brain className="mr-2 h-4 w-4" />
            <span>Go to AI Insights</span>
            <CommandShortcut>G I</CommandShortcut>
          </CommandItem>
          <CommandItem onSelect={() => runCommand(() => router.push("/intelligence/activity"))}>
            <Clock className="mr-2 h-4 w-4" />
            <span>Go to Recent Activity</span>
            <CommandShortcut>G R</CommandShortcut>
          </CommandItem>
        </CommandGroup>

        {/* Recent Accounts */}
        {mockAccounts.length > 0 && (
          <CommandGroup heading="Recent Accounts">
            {mockAccounts.map((account) => (
              <CommandItem
                key={account.id}
                onSelect={() => runCommand(() => router.push(`/intelligence/accounts/${account.id}`))}
              >
                <Building2 className="mr-2 h-4 w-4" />
                <span>{account.name}</span>
                <CommandShortcut>⌘{account.shortcut}</CommandShortcut>
              </CommandItem>
            ))}
          </CommandGroup>
        )}

        {/* Active Deals */}
        {mockDeals.length > 0 && (
          <CommandGroup heading="Active Deals">
            {mockDeals.map((deal) => (
              <CommandItem
                key={deal.id}
                onSelect={() => runCommand(() => router.push(`/intelligence/deals/${deal.id}`))}
              >
                <Target className="mr-2 h-4 w-4" />
                <span>{deal.name}</span>
                <span className="ml-auto text-xs text-muted-foreground">
                  {deal.account}
                </span>
              </CommandItem>
            ))}
          </CommandGroup>
        )}

        {/* AI Suggestions */}
        {searchValue.length === 0 && (
          <CommandGroup heading="AI Suggestions">
            <CommandItem onSelect={() => runCommand(() => console.log("Review stalled deals"))}>
              <Zap className="mr-2 h-4 w-4 text-[var(--confidence-medium)]" />
              <span>Review 3 stalled deals</span>
            </CommandItem>
            <CommandItem onSelect={() => runCommand(() => console.log("Follow up champions"))}>
              <Phone className="mr-2 h-4 w-4 text-[var(--ai-processing)]" />
              <span>Follow up with 2 champions</span>
            </CommandItem>
            <CommandItem onSelect={() => runCommand(() => console.log("Update MEDDPICC"))}>
              <Brain className="mr-2 h-4 w-4 text-[var(--confidence-high)]" />
              <span>Complete MEDDPICC for 4 deals</span>
            </CommandItem>
          </CommandGroup>
        )}

        {/* Search Results */}
        {searchValue.length > 0 && (
          <CommandGroup heading="Search Results">
            <CommandItem onSelect={() => runCommand(() => router.push("/intelligence/search?q=" + searchValue))}>
              <Search className="mr-2 h-4 w-4" />
              <span>Search for "{searchValue}"</span>
            </CommandItem>
          </CommandGroup>
        )}

        {/* Settings */}
        <CommandGroup heading="Settings">
          <CommandItem onSelect={() => runCommand(() => router.push("/intelligence/settings"))}>
            <Settings className="mr-2 h-4 w-4" />
            <span>Settings</span>
            <CommandShortcut>⌘,</CommandShortcut>
          </CommandItem>
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  )
}