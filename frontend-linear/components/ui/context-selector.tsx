"use client"

import { useState, useEffect, useRef } from "react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"
import {
  Building2,
  Target,
  Search,
  ChevronDown,
  X,
  Clock
} from "lucide-react"

interface ContextEntity {
  id: string
  name: string
  type: "account" | "deal"
  accountId?: string // For deals, references parent account
  accountName?: string // For deals, parent account name
  lastInteraction?: string
  value?: number
  stage?: string
}

interface ContextSelectorProps {
  selectedAccount?: ContextEntity | null
  selectedDeal?: ContextEntity | null
  onAccountChange: (account: ContextEntity | null) => void
  onDealChange: (deal: ContextEntity | null) => void
  className?: string
}

export function ContextSelector({
  selectedAccount,
  selectedDeal,
  onAccountChange,
  onDealChange,
  className
}: ContextSelectorProps) {
  const [accountSearch, setAccountSearch] = useState("")
  const [dealSearch, setDealSearch] = useState("")
  const [accountOpen, setAccountOpen] = useState(false)
  const [dealOpen, setDealOpen] = useState(false)
  const [recentAccounts, setRecentAccounts] = useState<ContextEntity[]>([])
  const [recentDeals, setRecentDeals] = useState<ContextEntity[]>([])
  const [filteredAccounts, setFilteredAccounts] = useState<ContextEntity[]>([])
  const [filteredDeals, setFilteredDeals] = useState<ContextEntity[]>([])

  // Mock data - replace with real API calls
  const mockAccounts: ContextEntity[] = [
    {
      id: "1",
      name: "Optimizely Inc",
      type: "account",
      lastInteraction: "2024-06-24"
    },
    {
      id: "2", 
      name: "Salesforce Corp",
      type: "account",
      lastInteraction: "2024-06-23"
    },
    {
      id: "3",
      name: "HubSpot Inc",
      type: "account", 
      lastInteraction: "2024-06-22"
    },
    {
      id: "4",
      name: "Microsoft Corporation",
      type: "account",
      lastInteraction: "2024-06-21"
    }
  ]

  const mockDeals: ContextEntity[] = [
    {
      id: "1",
      name: "Q4 Implementation",
      type: "deal",
      accountId: "1",
      accountName: "Optimizely Inc",
      value: 150000,
      stage: "technical_evaluation",
      lastInteraction: "2024-06-24"
    },
    {
      id: "2",
      name: "Enterprise Expansion",
      type: "deal", 
      accountId: "2",
      accountName: "Salesforce Corp",
      value: 280000,
      stage: "negotiation",
      lastInteraction: "2024-06-23"
    },
    {
      id: "3",
      name: "Platform Migration",
      type: "deal",
      accountId: "1", 
      accountName: "Optimizely Inc",
      value: 95000,
      stage: "discovery",
      lastInteraction: "2024-06-22"
    },
    {
      id: "4",
      name: "Analytics Upgrade",
      type: "deal",
      accountId: "3",
      accountName: "HubSpot Inc",
      value: 45000,
      stage: "proposal",
      lastInteraction: "2024-06-21"
    }
  ]

  // Initialize recent entities (sorted by last interaction)
  useEffect(() => {
    setRecentAccounts(mockAccounts.sort((a, b) => 
      new Date(b.lastInteraction || 0).getTime() - new Date(a.lastInteraction || 0).getTime()
    ).slice(0, 5))
    
    setRecentDeals(mockDeals.sort((a, b) => 
      new Date(b.lastInteraction || 0).getTime() - new Date(a.lastInteraction || 0).getTime()
    ).slice(0, 5))
  }, [])

  // Filter accounts based on search
  useEffect(() => {
    if (accountSearch.trim()) {
      setFilteredAccounts(
        mockAccounts.filter(account =>
          account.name.toLowerCase().includes(accountSearch.toLowerCase())
        )
      )
    } else {
      setFilteredAccounts(recentAccounts)
    }
  }, [accountSearch, recentAccounts])

  // Filter deals based on search and selected account
  useEffect(() => {
    let baseDeals = mockDeals
    
    // Filter by selected account first
    if (selectedAccount) {
      baseDeals = mockDeals.filter(deal => deal.accountId === selectedAccount.id)
    }
    
    if (dealSearch.trim()) {
      setFilteredDeals(
        baseDeals.filter(deal =>
          deal.name.toLowerCase().includes(dealSearch.toLowerCase()) ||
          deal.accountName?.toLowerCase().includes(dealSearch.toLowerCase())
        )
      )
    } else {
      // Show recent deals filtered by account if account is selected
      const recentFiltered = selectedAccount 
        ? recentDeals.filter(deal => deal.accountId === selectedAccount.id)
        : recentDeals
      setFilteredDeals(recentFiltered)
    }
  }, [dealSearch, recentDeals, selectedAccount])

  const handleAccountSelect = (account: ContextEntity) => {
    onAccountChange(account)
    setAccountOpen(false)
    setAccountSearch("")
  }

  const handleDealSelect = (deal: ContextEntity) => {
    onDealChange(deal)
    
    // Auto-select parent account if not already selected
    if (deal.accountId && deal.accountName && (!selectedAccount || selectedAccount.id !== deal.accountId)) {
      const parentAccount = mockAccounts.find(acc => acc.id === deal.accountId)
      if (parentAccount) {
        onAccountChange(parentAccount)
      }
    }
    
    setDealOpen(false)
    setDealSearch("")
  }

  const formatLastInteraction = (dateString?: string) => {
    if (!dateString) return ""
    const date = new Date(dateString)
    const now = new Date()
    const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24))
    
    if (diffDays === 0) return "Today"
    if (diffDays === 1) return "Yesterday"
    if (diffDays < 7) return `${diffDays}d ago`
    return `${Math.floor(diffDays / 7)}w ago`
  }

  const formatValue = (value?: number) => {
    if (!value) return ""
    if (value >= 1000000) return `$${(value / 1000000).toFixed(1)}M`
    if (value >= 1000) return `$${(value / 1000).toFixed(0)}K`
    return `$${value.toLocaleString()}`
  }

  return (
    <div className={cn("flex flex-col gap-3", className)}>
      {/* Account Selector */}
      <div>
        <label className="text-sm font-medium mb-2 block">Account Context</label>
        <Popover open={accountOpen} onOpenChange={setAccountOpen}>
          <PopoverTrigger asChild>
            <Button
              variant="outline"
              role="combobox"
              aria-expanded={accountOpen}
              className="w-full justify-between h-auto p-3"
            >
              {selectedAccount ? (
                <div className="flex items-center gap-2">
                  <Building2 className="h-4 w-4 text-green-600" />
                  <span className="font-medium">{selectedAccount.name}</span>
                  {selectedAccount.lastInteraction && (
                    <Badge variant="outline" className="text-xs">
                      {formatLastInteraction(selectedAccount.lastInteraction)}
                    </Badge>
                  )}
                </div>
              ) : (
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Building2 className="h-4 w-4" />
                  <span>Select account...</span>
                </div>
              )}
              <div className="flex items-center gap-1">
                {selectedAccount && (
                  <Button
                    variant="ghost"
                    size="sm"
                    className="h-5 w-5 p-0"
                    onClick={(e) => {
                      e.stopPropagation()
                      onAccountChange(null)
                    }}
                  >
                    <X className="h-3 w-3" />
                  </Button>
                )}
                <ChevronDown className="h-4 w-4 opacity-50" />
              </div>
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-full p-0" align="start">
            <div className="p-3 border-b">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search accounts..."
                  value={accountSearch}
                  onChange={(e) => setAccountSearch(e.target.value)}
                  className="pl-9"
                />
              </div>
            </div>
            <ScrollArea className="max-h-60">
              <div className="p-2">
                {!accountSearch && (
                  <div className="flex items-center gap-2 px-2 py-1 text-xs text-muted-foreground mb-2">
                    <Clock className="h-3 w-3" />
                    Recent accounts
                  </div>
                )}
                {filteredAccounts.map((account) => (
                  <Button
                    key={account.id}
                    variant="ghost"
                    className="w-full justify-start h-auto p-2 font-normal"
                    onClick={() => handleAccountSelect(account)}
                  >
                    <div className="flex items-center gap-2 w-full">
                      <Building2 className="h-4 w-4 text-green-600 flex-shrink-0" />
                      <div className="flex-1 text-left">
                        <div className="font-medium">{account.name}</div>
                        {account.lastInteraction && (
                          <div className="text-xs text-muted-foreground">
                            Last interaction: {formatLastInteraction(account.lastInteraction)}
                          </div>
                        )}
                      </div>
                    </div>
                  </Button>
                ))}
                {filteredAccounts.length === 0 && (
                  <div className="text-center py-4 text-sm text-muted-foreground">
                    No accounts found
                  </div>
                )}
              </div>
            </ScrollArea>
          </PopoverContent>
        </Popover>
      </div>

      {/* Deal Selector */}
      <div>
        <label className="text-sm font-medium mb-2 block">Deal Context (optional)</label>
        <Popover open={dealOpen} onOpenChange={setDealOpen}>
          <PopoverTrigger asChild>
            <Button
              variant="outline"
              role="combobox"
              aria-expanded={dealOpen}
              className="w-full justify-between h-auto p-3"
            >
              {selectedDeal ? (
                <div className="flex items-center gap-2">
                  <Target className="h-4 w-4 text-purple-600" />
                  <div className="flex flex-col items-start">
                    <span className="font-medium">{selectedDeal.name}</span>
                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                      <span>{selectedDeal.accountName}</span>
                      {selectedDeal.value && (
                        <Badge variant="outline" className="text-xs">
                          {formatValue(selectedDeal.value)}
                        </Badge>
                      )}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="flex items-center gap-2 text-muted-foreground">
                  <Target className="h-4 w-4" />
                  <span>Select deal...</span>
                </div>
              )}
              <div className="flex items-center gap-1">
                {selectedDeal && (
                  <Button
                    variant="ghost"
                    size="sm"
                    className="h-5 w-5 p-0"
                    onClick={(e) => {
                      e.stopPropagation()
                      onDealChange(null)
                    }}
                  >
                    <X className="h-3 w-3" />
                  </Button>
                )}
                <ChevronDown className="h-4 w-4 opacity-50" />
              </div>
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-full p-0" align="start">
            <div className="p-3 border-b">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  placeholder="Search deals..."
                  value={dealSearch}
                  onChange={(e) => setDealSearch(e.target.value)}
                  className="pl-9"
                />
              </div>
            </div>
            <ScrollArea className="max-h-60">
              <div className="p-2">
                {!dealSearch && (
                  <div className="flex items-center gap-2 px-2 py-1 text-xs text-muted-foreground mb-2">
                    <Clock className="h-3 w-3" />
                    Recent deals
                  </div>
                )}
                {filteredDeals.map((deal) => (
                  <Button
                    key={deal.id}
                    variant="ghost"
                    className="w-full justify-start h-auto p-2 font-normal"
                    onClick={() => handleDealSelect(deal)}
                  >
                    <div className="flex items-center gap-2 w-full">
                      <Target className="h-4 w-4 text-purple-600 flex-shrink-0" />
                      <div className="flex-1 text-left">
                        <div className="font-medium">{deal.name}</div>
                        <div className="text-xs text-muted-foreground">
                          {deal.accountName}
                          {deal.value && ` • ${formatValue(deal.value)}`}
                          {deal.stage && ` • ${deal.stage.replace("_", " ")}`}
                        </div>
                      </div>
                    </div>
                  </Button>
                ))}
                {filteredDeals.length === 0 && (
                  <div className="text-center py-4 text-sm text-muted-foreground">
                    No deals found
                  </div>
                )}
              </div>
            </ScrollArea>
          </PopoverContent>
        </Popover>
      </div>
    </div>
  )
}