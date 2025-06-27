"use client"

import { useState, useEffect, useCallback } from "react"
import { useRouter } from "next/navigation"
import {
  Dialog,
  DialogContent,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { MentionAutocomplete, MentionEntity } from "@/components/ui/mention-autocomplete"
import { LinearDropdown, DropdownOption } from "@/components/ui/linear-dropdown"
import { cn } from "@/lib/utils"
import {
  Zap,
  Clock,
  Send,
  Maximize2,
  MoreHorizontal,
  Hash,
  Building,
  User
} from "lucide-react"

interface SmartCaptureDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function SmartCaptureDialog({ open, onOpenChange }: SmartCaptureDialogProps) {
  const router = useRouter()
  const [noteContent, setNoteContent] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)
  const [mentions, setMentions] = useState<MentionEntity[]>([])
  const [selectedDealId, setSelectedDealId] = useState<string>("")
  const [selectedAccountId, setSelectedAccountId] = useState<string>("")
  const [title, setTitle] = useState("")
  const [isExpanded, setIsExpanded] = useState(false)

  // Reset dialog when opened
  useEffect(() => {
    if (open) {
      setNoteContent("")
      setMentions([])
      setSelectedDealId("")
      setSelectedAccountId("")
      setIsProcessing(false)
      setTitle("")
      setIsExpanded(false)
    }
  }, [open])

  // Mock data for dropdowns
  const dealOptions: DropdownOption[] = [
    { id: "d1", name: "Q4 Implementation", subtitle: "Optimizely Inc • $150k", icon: <Hash className="h-3.5 w-3.5" /> },
    { id: "d2", name: "Q4 Expansion", subtitle: "Salesforce Corp • $200k", icon: <Hash className="h-3.5 w-3.5" /> },
    { id: "d3", name: "Q4 Renewal", subtitle: "Linear Software • $50k", icon: <Hash className="h-3.5 w-3.5" /> }
  ]

  const accountOptions: DropdownOption[] = [
    { id: "a1", name: "Optimizely Inc", subtitle: "Enterprise • Technology", icon: <Building className="h-3.5 w-3.5" /> },
    { id: "a2", name: "Salesforce Corp", subtitle: "Enterprise • Technology", icon: <Building className="h-3.5 w-3.5" /> },
    { id: "a3", name: "Linear Software", subtitle: "Mid-Market • Technology", icon: <Building className="h-3.5 w-3.5" /> }
  ]

  // Deal to Account mapping
  const dealToAccountMapping: Record<string, string> = {
    "d1": "a1", // Q4 Implementation -> Optimizely Inc
    "d2": "a2", // Q4 Expansion -> Salesforce Corp  
    "d3": "a3"  // Q4 Renewal -> Linear Software
  }

  // Handle mentions change - auto-select deal/account if mentioned
  const handleMentionsChange = useCallback((newMentions: MentionEntity[]) => {
    setMentions(newMentions)
    
    // Auto-select deal if mentioned
    const dealMention = newMentions.find(m => m.type === "deal")
    if (dealMention && !selectedDealId) {
      setSelectedDealId(dealMention.id)
    }
    
    // Auto-select account if mentioned
    const accountMention = newMentions.find(m => m.type === "account")
    if (accountMention && !selectedAccountId) {
      setSelectedAccountId(accountMention.id)
    }
  }, [selectedDealId, selectedAccountId])

  // Handle deal selection and auto-select associated account
  const handleDealChange = useCallback((dealId: string) => {
    console.log("Deal selected:", dealId)
    console.log("Deal to account mapping:", dealToAccountMapping)
    setSelectedDealId(dealId)
    
    // Auto-select the associated account
    const associatedAccountId = dealToAccountMapping[dealId]
    console.log("Associated account ID:", associatedAccountId)
    if (associatedAccountId) {
      console.log("Setting account to:", associatedAccountId)
      setSelectedAccountId(associatedAccountId)
    }
  }, [dealToAccountMapping])

  const handleSave = async () => {
    if (!noteContent.trim()) return

    setIsProcessing(true)

    try {
      // Prepare request data
      const requestData = {
        content: noteContent,
        title: title || generateTitle(),
        deal_id: selectedDealId || null,
        account_id: selectedAccountId || null,
        linked_entities: mentions.map(m => ({
          id: m.id,
          type: m.type,
          name: m.name,
          confidence: m.confidence || 0.9
        })),
        capture_method: "manual",
        capture_location: window.location.pathname
      }

      // Call Smart Capture API
      const response = await fetch("http://localhost:8000/api/smart-capture/notes", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(requestData)
      })

      if (!response.ok) {
        throw new Error(`API call failed: ${response.statusText}`)
      }

      const result = await response.json()
      console.log("Smart Capture note created:", result)
      
      // Close dialog and show success
      onOpenChange(false)
      
      // Navigate to deal if selected
      if (selectedDealId) {
        router.push(`/deals`)
      } else if (selectedAccountId) {
        router.push(`/accounts`)
      }
    } catch (error) {
      console.error("Failed to save note:", error)
      // TODO: Show error toast to user
    } finally {
      setIsProcessing(false)
    }
  }

  // Generate title based on mentions and context
  const generateTitle = useCallback(() => {
    if (!noteContent) return ""
    
    const stakeholders = mentions.filter(m => m.type === "stakeholder")
    const dealOption = dealOptions.find(d => d.id === selectedDealId)
    const accountOption = accountOptions.find(a => a.id === selectedAccountId)
    
    if (dealOption && stakeholders.length > 0) {
      return `${dealOption.name}: Call with ${stakeholders[0].name}`
    }
    
    if (accountOption && stakeholders.length > 0) {
      return `${accountOption.name}: Meeting with ${stakeholders[0].name}`
    }
    
    if (stakeholders.length > 0) {
      return `Meeting with ${stakeholders[0].name}`
    }
    
    if (dealOption) {
      return `${dealOption.name}: Update`
    }
    
    if (accountOption) {
      return `${accountOption.name}: Note`
    }
    
    return "Sales Note"
  }, [noteContent, mentions, selectedDealId, selectedAccountId, dealOptions, accountOptions])

  useEffect(() => {
    if ((mentions.length > 0 || selectedDealId || selectedAccountId) && !title) {
      setTitle(generateTitle())
    }
  }, [mentions, selectedDealId, selectedAccountId, title, generateTitle])

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent 
        className={cn(
          "flex flex-col p-0 gap-0 border-gray-200",
          isExpanded ? "max-w-4xl max-h-[90vh]" : "max-w-2xl max-h-[600px]"
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b">
          <div className="flex items-center gap-2">
            <Zap className="h-4 w-4 text-blue-600" />
            <span className="font-medium">Smart Capture</span>
          </div>
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-1 hover:bg-gray-100 rounded transition-colors"
            type="button"
          >
            <Maximize2 className="h-4 w-4" />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 flex flex-col gap-4 p-4 overflow-y-auto">
          {/* Title */}
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Note title (auto-generated)"
            className="w-full text-sm font-medium bg-transparent border-0 outline-none focus:ring-0 placeholder:text-gray-400"
          />

          {/* Note Content */}
          <div className="flex-1">
            <MentionAutocomplete
              value={noteContent}
              onChange={setNoteContent}
              onMentionsChange={handleMentionsChange}
              className={cn(
                "border-0 shadow-none resize-none",
                isExpanded ? "min-h-[400px]" : "min-h-[300px]"
              )}
              disabled={isProcessing}
            />
          </div>
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between px-4 py-3 border-t bg-gray-50 dark:bg-gray-900">
          <div className="flex items-center gap-2">
            <LinearDropdown
              value={selectedDealId}
              onValueChange={handleDealChange}
              options={dealOptions}
              placeholder="Deal"
              searchPlaceholder="Search deals..."
              buttonClassName="text-xs"
              disabled={isProcessing}
            />
            <LinearDropdown
              value={selectedAccountId}
              onValueChange={setSelectedAccountId}
              options={accountOptions}
              placeholder="Account"
              searchPlaceholder="Search accounts..."
              buttonClassName="text-xs"
              disabled={isProcessing}
            />
            <button
              type="button"
              className="p-1.5 hover:bg-gray-200 dark:hover:bg-gray-700 rounded transition-colors"
              disabled={isProcessing}
            >
              <MoreHorizontal className="h-4 w-4" />
            </button>
          </div>

          <div className="flex items-center gap-2">
            {noteContent.length > 0 && (
              <span className="text-xs text-gray-500 mr-2">
                {mentions.length} linked • {noteContent.length} chars
              </span>
            )}
            <Button
              variant="default"
              size="sm"
              onClick={handleSave}
              disabled={!noteContent.trim() || isProcessing}
              className="text-xs"
            >
              {isProcessing ? (
                <>
                  <Clock className="h-3 w-3 mr-1 animate-spin" />
                  Processing...
                </>
              ) : (
                "Create"
              )}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}