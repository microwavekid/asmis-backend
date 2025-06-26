"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
  Brain,
  Building2,
  Target,
  User,
  Zap,
  Check,
  AlertCircle,
  Clock,
  Send
} from "lucide-react"

interface SmartCaptureDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

interface DetectedEntity {
  id: string
  type: "account" | "deal" | "stakeholder" | "partner" | "meddpicc"
  text: string
  confidence: number
  attributes: Record<string, any>
  startPos: number
  endPos: number
}

interface ContextInfo {
  type: "deal" | "account" | "stakeholder" | "global"
  id?: string
  name: string
  confidence: number
}

export function SmartCaptureDialog({ open, onOpenChange }: SmartCaptureDialogProps) {
  const router = useRouter()
  const [noteContent, setNoteContent] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)
  const [detectedEntities, setDetectedEntities] = useState<DetectedEntity[]>([])
  const [contextInfo, setContextInfo] = useState<ContextInfo | null>(null)
  const [title, setTitle] = useState("")

  // Detect context from current URL
  useEffect(() => {
    if (open) {
      detectPageContext()
      setNoteContent("")
      setDetectedEntities([])
      setIsProcessing(false)
      setTitle("")
    }
  }, [open])

  const detectPageContext = () => {
    // Simulate context detection from current URL
    if (typeof window !== 'undefined') {
      const path = window.location.pathname
      
      if (path.includes('/deals/')) {
        const dealId = path.split('/deals/')[1]?.split('/')[0]
        setContextInfo({
          type: "deal",
          id: dealId,
          name: "Enterprise Implementation - Optimizely",
          confidence: 0.95
        })
      } else if (path.includes('/accounts/')) {
        const accountId = path.split('/accounts/')[1]?.split('/')[0]
        setContextInfo({
          type: "account",
          id: accountId,
          name: "Optimizely Enterprise",
          confidence: 0.92
        })
      } else {
        setContextInfo({
          type: "global",
          name: "Global context",
          confidence: 0.80
        })
      }
    }
  }

  // Process note content for entity extraction
  useEffect(() => {
    if (noteContent.length > 10) {
      const timer = setTimeout(() => {
        extractEntities(noteContent)
      }, 500) // Debounce for 500ms

      return () => clearTimeout(timer)
    } else {
      setDetectedEntities([])
    }
  }, [noteContent])

  const extractEntities = async (content: string) => {
    // Simulate AI entity extraction
    const mockEntities: DetectedEntity[] = []

    // Simple pattern matching for demo
    const patterns = [
      {
        regex: /\b([A-Z][a-z]+ [A-Z][a-z]+)\b/g,
        type: "stakeholder" as const,
        confidence: 0.85
      },
      {
        regex: /\b(\d+%|percent)\b/gi,
        type: "meddpicc" as const,
        confidence: 0.90
      },
      {
        regex: /\b(budget|roi|revenue|cost|savings)\b/gi,
        type: "meddpicc" as const,
        confidence: 0.80
      },
      {
        regex: /\b([A-Z][a-z]+ (?:Corp|Inc|LLC|Ltd|Company))\b/g,
        type: "account" as const,
        confidence: 0.75
      }
    ]

    patterns.forEach(pattern => {
      let match
      while ((match = pattern.regex.exec(content)) !== null) {
        mockEntities.push({
          id: `entity-${mockEntities.length}`,
          type: pattern.type,
          text: match[1] || match[0],
          confidence: pattern.confidence,
          attributes: {
            category: pattern.type === "meddpicc" ? "metrics" : undefined,
            role: pattern.type === "stakeholder" ? "unknown" : undefined
          },
          startPos: match.index,
          endPos: match.index + match[0].length
        })
      }
    })

    setDetectedEntities(mockEntities)
  }

  const getEntityIcon = (type: string) => {
    switch (type) {
      case "stakeholder":
        return <User className="h-3 w-3" />
      case "account":
        return <Building2 className="h-3 w-3" />
      case "deal":
        return <Target className="h-3 w-3" />
      case "meddpicc":
        return <Brain className="h-3 w-3" />
      default:
        return <Zap className="h-3 w-3" />
    }
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return "bg-green-100 text-green-800 border-green-200"
    if (confidence >= 0.6) return "bg-yellow-100 text-yellow-800 border-yellow-200"
    return "bg-red-100 text-red-800 border-red-200"
  }

  const handleSave = async () => {
    if (!noteContent.trim()) return

    setIsProcessing(true)

    try {
      // Simulate API call to save note
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      // Close dialog and show success
      onOpenChange(false)
      
      // Navigate to context if available
      if (contextInfo?.type === "deal" && contextInfo.id) {
        router.push(`/intelligence/deals/${contextInfo.id}`)
      } else if (contextInfo?.type === "account" && contextInfo.id) {
        router.push(`/intelligence/accounts/${contextInfo.id}`)
      }
    } catch (error) {
      console.error("Failed to save note:", error)
    } finally {
      setIsProcessing(false)
    }
  }

  const generateTitle = () => {
    if (!noteContent) return ""
    
    // Simple title generation based on entities
    const stakeholders = detectedEntities.filter(e => e.type === "stakeholder")
    const accounts = detectedEntities.filter(e => e.type === "account")
    
    if (stakeholders.length > 0 && accounts.length > 0) {
      return `Call with ${stakeholders[0].text} - ${accounts[0].text}`
    } else if (stakeholders.length > 0) {
      return `Meeting with ${stakeholders[0].text}`
    } else if (detectedEntities.some(e => e.type === "meddpicc")) {
      return "MEDDPICC Update"
    } else {
      return "Sales Note"
    }
  }

  useEffect(() => {
    if (detectedEntities.length > 0 && !title) {
      setTitle(generateTitle())
    }
  }, [detectedEntities, title])

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[90vh] flex flex-col">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Zap className="h-5 w-5 text-blue-600" />
            Smart Capture
          </DialogTitle>
          <DialogDescription>
            Quickly capture freehand notes. AI will automatically extract entities and relationships.
          </DialogDescription>
        </DialogHeader>

        <div className="flex-1 grid grid-cols-2 gap-6 min-h-0">
          {/* Left side - Input */}
          <div className="flex flex-col gap-4">
            {/* Context Detection */}
            {contextInfo && (
              <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="flex items-center gap-2 text-sm">
                  <Brain className="h-4 w-4 text-blue-600" />
                  <span className="font-medium">Context Detected</span>
                  <Badge variant="secondary" className={getConfidenceColor(contextInfo.confidence)}>
                    {Math.round(contextInfo.confidence * 100)}%
                  </Badge>
                </div>
                <p className="text-sm text-gray-600 mt-1">{contextInfo.name}</p>
              </div>
            )}

            {/* Title */}
            <div>
              <label className="text-sm font-medium mb-2 block">Title (auto-generated)</label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Note title will be generated automatically..."
                className="w-full px-3 py-2 border border-gray-200 rounded-md text-sm"
              />
            </div>

            {/* Note Content */}
            <div className="flex-1 flex flex-col">
              <label className="text-sm font-medium mb-2 block">Your notes</label>
              <Textarea
                value={noteContent}
                onChange={(e) => setNoteContent(e.target.value)}
                placeholder="Capture your notes here... For example:

'Had a great call with Sarah Johnson from Optimizely. She mentioned they need 30% efficiency improvement and John Smith is the decision maker. Budget approved for Q4 implementation.'"
                className="flex-1 min-h-[200px] resize-none"
              />
              <div className="text-xs text-gray-500 mt-2">
                {noteContent.length} characters • AI processing in real-time
              </div>
            </div>
          </div>

          {/* Right side - Extracted Entities */}
          <div className="flex flex-col">
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-medium text-sm">Extracted Entities</h3>
              {detectedEntities.length > 0 && (
                <Badge variant="outline">{detectedEntities.length} found</Badge>
              )}
            </div>

            <ScrollArea className="flex-1 border rounded-lg p-3">
              {detectedEntities.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  <Brain className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p className="text-sm">Start typing to see AI entity extraction</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {detectedEntities.map((entity) => (
                    <div key={entity.id} className="border rounded-lg p-3 bg-gray-50">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center gap-2">
                          {getEntityIcon(entity.type)}
                          <span className="text-sm font-medium capitalize">
                            {entity.type}
                          </span>
                        </div>
                        <Badge 
                          variant="outline" 
                          className={getConfidenceColor(entity.confidence)}
                        >
                          {Math.round(entity.confidence * 100)}%
                        </Badge>
                      </div>
                      <p className="text-sm font-medium mb-1">"{entity.text}"</p>
                      {Object.keys(entity.attributes).length > 0 && (
                        <div className="text-xs text-gray-600">
                          {Object.entries(entity.attributes).map(([key, value]) => (
                            value && (
                              <span key={key} className="mr-2">
                                {key}: {value}
                              </span>
                            )
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </ScrollArea>

            {/* Processing Status */}
            {detectedEntities.length > 0 && (
              <div className="mt-3 p-2 bg-green-50 border border-green-200 rounded-lg">
                <div className="flex items-center gap-2 text-sm text-green-700">
                  <Check className="h-4 w-4" />
                  <span>Ready to save and create entity links</span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <Separator />
        <div className="flex justify-between items-center">
          <div className="text-xs text-gray-500">
            {detectedEntities.length > 0 ? (
              `${detectedEntities.length} entities will be linked to ${contextInfo?.name || 'global context'}`
            ) : (
              "Type your notes above to see AI extraction in action"
            )}
          </div>
          
          <div className="flex gap-2">
            <Button 
              variant="outline" 
              onClick={() => onOpenChange(false)}
              disabled={isProcessing}
            >
              Cancel
            </Button>
            <Button 
              onClick={handleSave}
              disabled={!noteContent.trim() || isProcessing}
              className="flex items-center gap-2"
            >
              {isProcessing ? (
                <>
                  <Clock className="h-4 w-4 animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  <Send className="h-4 w-4" />
                  Save & Process
                </>
              )}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}