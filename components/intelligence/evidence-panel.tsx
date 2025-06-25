"use client"

import { useState } from "react"
import { useParams } from "next/navigation"
import { 
  FileText, 
  Phone, 
  Mail, 
  FileCheck, 
  Search,
  Filter,
  PanelRightClose,
  PanelRightOpen,
  ExternalLink,
  Copy,
  Flag
} from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { cn } from "@/lib/utils"
import { PanelToggleIcon } from "@/components/intelligence/panel-toggle-icon"
import type { Evidence } from "@/types/meddpicc"
import type { EvidenceFilters } from "@/types/evidence"

// Mock evidence data - in real app this would come from API
const mockEvidence: Evidence[] = [
  {
    id: "1",
    type: "transcript",
    content: "We need to reduce our processing costs by at least 40% to meet our targets for next year.",
    excerpt: "reduce our processing costs by at least 40%",
    source: {
      id: "tr-1",
      name: "Demo Call - Oct 23",
      timestamp: "14:23",
    },
    position: {
      start: 1523,
      end: 1565,
    },
    confidence: 92,
    businessImplication: "Clear cost reduction metric identified",
    extractedBy: "MEDDPICC Agent",
    createdAt: new Date("2024-10-23T14:23:00"),
  },
  {
    id: "2",
    type: "email",
    content: "Sarah mentioned she has budget approval for Q1 if we can demonstrate the ROI.",
    excerpt: "budget approval for Q1",
    source: {
      id: "em-1",
      name: "Follow-up thread",
    },
    position: {
      start: 234,
      end: 256,
    },
    confidence: 78,
    businessImplication: "Budget and timeline confirmed",
    extractedBy: "Email Agent",
    createdAt: new Date("2024-10-24T09:15:00"),
  },
  {
    id: "3",
    type: "document",
    content: "Integration must be completed within 2 weeks with minimal disruption to existing systems.",
    excerpt: "completed within 2 weeks",
    source: {
      id: "doc-1",
      name: "Technical Requirements v2",
    },
    position: {
      start: 4521,
      end: 4545,
    },
    confidence: 85,
    businessImplication: "Technical timeline constraint identified",
    extractedBy: "Document Agent",
    createdAt: new Date("2024-10-22T16:30:00"),
  },
]

interface EvidencePanelProps {
  onToggle?: () => void
  isOpen?: boolean
}

export function EvidencePanel({ onToggle, isOpen = true }: EvidencePanelProps) {
  const params = useParams()
  const dealId = params?.dealId as string
  
  const [searchQuery, setSearchQuery] = useState("")
  const [filters, setFilters] = useState<EvidenceFilters>({})
  const [selectedEvidence, setSelectedEvidence] = useState<Evidence | null>(null)
  
  const getEvidenceIcon = (type: Evidence['type']) => {
    switch (type) {
      case 'transcript':
        return Phone
      case 'email':
        return Mail
      case 'document':
        return FileCheck
      default:
        return FileText
    }
  }
  
  const getConfidenceBadgeColor = (confidence: number) => {
    if (confidence >= 80) return "bg-[var(--confidence-high)] text-white"
    if (confidence >= 60) return "bg-[var(--confidence-medium)] text-white"
    return "bg-[var(--confidence-low)] text-white"
  }
  
  const filteredEvidence = mockEvidence.filter(item => {
    if (searchQuery && !item.content.toLowerCase().includes(searchQuery.toLowerCase())) {
      return false
    }
    if (filters.types && filters.types.length > 0 && !filters.types.includes(item.type)) {
      return false
    }
    if (filters.confidenceMin && item.confidence < filters.confidenceMin) {
      return false
    }
    return true
  })
  
  return (
    <div className="h-full flex flex-col bg-[var(--bg-base)]">
      {/* Search and Filter */}
      <div className="p-3 border-b border-[var(--bg-border)]">
        <div className="flex gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-[var(--content-secondary)]" />
            <Input
              placeholder="Search..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-8 h-8 bg-[var(--bg-border)]/50 border-[var(--bg-border)] text-xs"
            />
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="outline" size="icon" className="h-8 w-8">
                <Filter className="h-4 w-4" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-48">
              <DropdownMenuLabel>Filter by type</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem>
                <Phone className="mr-2 h-4 w-4" />
                Transcripts
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Mail className="mr-2 h-4 w-4" />
                Emails
              </DropdownMenuItem>
              <DropdownMenuItem>
                <FileCheck className="mr-2 h-4 w-4" />
                Documents
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
      
      {/* Evidence List */}
      <ScrollArea className="flex-1">
        <div className="p-3 space-y-2">
          {filteredEvidence.map((evidence) => (
            <EvidenceCard
              key={evidence.id}
              evidence={evidence}
              isSelected={selectedEvidence?.id === evidence.id}
              onClick={() => setSelectedEvidence(evidence)}
            />
          ))}
          
          {filteredEvidence.length === 0 && (
            <div className="text-center py-8 text-[var(--content-secondary)]">
              <FileText className="h-8 w-8 mx-auto mb-2 opacity-50" />
              <p className="text-sm">No evidence found</p>
            </div>
          )}
        </div>
      </ScrollArea>
      
      {/* Quick Actions */}
      <div className="p-3 border-t border-[var(--bg-border)] space-y-2">
        <Button 
          variant="outline" 
          className="w-full justify-start text-xs h-8"
          onClick={() => {/* Open upload modal */}}
        >
          <FileText className="mr-2 h-3 w-3" />
          Upload Transcript
        </Button>
        <Button 
          variant="outline" 
          className="w-full justify-start text-xs h-8"
          onClick={() => {/* Connect email */}}
        >
          <Mail className="mr-2 h-3 w-3" />
          Connect Email
        </Button>
      </div>
    </div>
  )
}

function EvidenceCard({ 
  evidence, 
  isSelected, 
  onClick 
}: { 
  evidence: Evidence
  isSelected: boolean
  onClick: () => void 
}) {
  const Icon = evidence.type === 'transcript' ? Phone : 
               evidence.type === 'email' ? Mail : 
               evidence.type === 'document' ? FileCheck : FileText
  
  return (
    <div
      className={cn(
        "p-2 rounded-md border cursor-pointer transition-all",
        isSelected 
          ? "border-[var(--ai-processing)] bg-[var(--evidence-highlight)]" 
          : "border-[var(--bg-border)] hover:border-[var(--content-secondary)]/50 hover:bg-[var(--bg-border)]/30"
      )}
      onClick={onClick}
    >
      {/* Header */}
      <div className="flex items-start gap-2 mb-1">
        <div className="p-1 rounded bg-[var(--bg-border)] flex-shrink-0">
          <Icon className="h-3 w-3 text-[var(--content-secondary)]" />
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-xs font-medium text-[var(--content-primary)] truncate">
            {evidence.source.name}
          </p>
          <p className="text-xs text-[var(--content-secondary)]">
            {evidence.source.timestamp || new Date(evidence.createdAt).toLocaleDateString()}
          </p>
        </div>
        <Badge 
          className={cn(
            "text-xs px-1.5 py-0 h-5 flex-shrink-0",
            evidence.confidence >= 80 
              ? "bg-[var(--confidence-high)]/20 text-[var(--confidence-high)]"
              : evidence.confidence >= 60
              ? "bg-[var(--confidence-medium)]/20 text-[var(--confidence-medium)]"
              : "bg-[var(--confidence-low)]/20 text-[var(--confidence-low)]"
          )}
        >
          {evidence.confidence}%
        </Badge>
      </div>
      
      {/* Content */}
      <p className="text-xs text-[var(--content-primary)] line-clamp-2 mb-1 leading-relaxed">
        {evidence.content}
      </p>
      
      {/* Business Implication */}
      {evidence.businessImplication && (
        <p className="text-xs text-[var(--content-secondary)] italic line-clamp-1">
          💡 {evidence.businessImplication}
        </p>
      )}
      
      {/* Actions (shown on selection) */}
      {isSelected && (
        <div className="flex gap-1 mt-2 pt-2 border-t border-[var(--bg-border)]">
          <Button variant="ghost" size="sm" className="text-xs h-7 px-2">
            <ExternalLink className="mr-1 h-3 w-3" />
            View
          </Button>
          <Button variant="ghost" size="sm" className="text-xs h-7 px-2">
            <Copy className="mr-1 h-3 w-3" />
            Copy
          </Button>
          <Button variant="ghost" size="sm" className="text-xs h-7 px-2">
            <Flag className="mr-1 h-3 w-3" />
            Flag
          </Button>
        </div>
      )}
    </div>
  )
}