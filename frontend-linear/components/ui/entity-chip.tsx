"use client"

import { useState } from "react"
import { cn } from "@/lib/utils"
import { getEntityColor } from "@/lib/utils/colors"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from "@/components/ui/hover-card"
import {
  Building2,
  Target,
  User,
  Handshake,
  Brain,
  X,
  ExternalLink,
  Calendar,
  Mail,
  Phone
} from "lucide-react"

export interface Entity {
  id: string
  type: "stakeholder" | "account" | "deal" | "partner" | "meddpicc"
  name: string
  confidence: number
  attributes: {
    title?: string
    email?: string
    phone?: string
    company?: string
    department?: string
    role?: string
    lastContact?: string
    dealValue?: number
    dealStage?: string
    category?: string
    metric_type?: string
    [key: string]: any
  }
}

interface EntityChipProps {
  entity: Entity
  isEditable?: boolean
  onRemove?: (entityId: string) => void
  onEdit?: (entityId: string) => void
  onClick?: (entityId: string) => void
  className?: string
}

export function EntityChip({ 
  entity, 
  isEditable = false, 
  onRemove, 
  onEdit, 
  onClick,
  className 
}: EntityChipProps) {
  const [isHovered, setIsHovered] = useState(false)

  const getEntityIcon = (type: string) => {
    switch (type) {
      case "stakeholder":
        return <User className="h-3 w-3" />
      case "account":
        return <Building2 className="h-3 w-3" />
      case "deal":
        return <Target className="h-3 w-3" />
      case "partner":
        return <Handshake className="h-3 w-3" />
      case "meddpicc":
        return <Brain className="h-3 w-3" />
      default:
        return <User className="h-3 w-3" />
    }
  }

  const getEntityColorClasses = (type: string, confidence: number) => {
    // Handle meddpicc separately as it's not in the main entity types
    if (type === "meddpicc") {
      const opacity = confidence >= 0.8 ? "" : confidence >= 0.6 ? " opacity-80" : " opacity-60"
      return `bg-indigo-100 text-indigo-800 border-indigo-200 hover:bg-indigo-200${opacity}`
    }
    
    return getEntityColor(type as any, confidence)
  }

  const formatLastContact = (dateString?: string) => {
    if (!dateString) return null
    const date = new Date(dateString)
    const now = new Date()
    const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24))
    
    if (diffDays === 0) return "Today"
    if (diffDays === 1) return "Yesterday"
    if (diffDays < 7) return `${diffDays} days ago`
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
    return `${Math.floor(diffDays / 30)} months ago`
  }

  const formatValue = (value: number) => {
    if (value >= 1000000) return `$${(value / 1000000).toFixed(1)}M`
    if (value >= 1000) return `$${(value / 1000).toFixed(0)}K`
    return `$${value.toLocaleString()}`
  }

  const handleChipClick = (e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (onClick) {
      onClick(entity.id)
    }
  }

  const handleRemove = (e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (onRemove) {
      onRemove(entity.id)
    }
  }

  return (
    <HoverCard>
      <HoverCardTrigger asChild>
        <span
          className={cn(
            "inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-md border cursor-pointer transition-colors",
            getEntityColorClasses(entity.type, entity.confidence),
            isEditable && "pr-1",
            className
          )}
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
          onClick={handleChipClick}
        >
          {getEntityIcon(entity.type)}
          <span className="truncate max-w-[120px]">{entity.name}</span>
          
          {/* Confidence indicator */}
          {entity.confidence < 0.8 && (
            <Badge variant="outline" className="ml-1 px-1 py-0 text-xs h-4">
              {Math.round(entity.confidence * 100)}%
            </Badge>
          )}
          
          {/* Remove button for editable chips */}
          {isEditable && isHovered && (
            <Button
              variant="ghost"
              size="sm"
              className="h-4 w-4 p-0 ml-1 hover:bg-red-100"
              onClick={handleRemove}
            >
              <X className="h-3 w-3" />
            </Button>
          )}
        </span>
      </HoverCardTrigger>
      
      <HoverCardContent className="w-80" side="top">
        <div className="space-y-3">
          {/* Header */}
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-2">
              {getEntityIcon(entity.type)}
              <div>
                <h4 className="font-semibold text-sm">{entity.name}</h4>
                <p className="text-xs text-muted-foreground capitalize">{entity.type}</p>
              </div>
            </div>
            <Button variant="ghost" size="sm" className="h-6 w-6 p-0">
              <ExternalLink className="h-3 w-3" />
            </Button>
          </div>

          {/* Entity-specific details */}
          {entity.type === "stakeholder" && (
            <div className="space-y-2">
              {entity.attributes.title && (
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-muted-foreground">Title:</span>
                  <span>{entity.attributes.title}</span>
                </div>
              )}
              {entity.attributes.department && (
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-muted-foreground">Department:</span>
                  <span>{entity.attributes.department}</span>
                </div>
              )}
              {entity.attributes.email && (
                <div className="flex items-center gap-2 text-sm">
                  <Mail className="h-3 w-3 text-muted-foreground" />
                  <span className="text-muted-foreground">Email:</span>
                  <span className="font-mono text-xs">{entity.attributes.email}</span>
                </div>
              )}
              {entity.attributes.lastContact && (
                <div className="flex items-center gap-2 text-sm">
                  <Calendar className="h-3 w-3 text-muted-foreground" />
                  <span className="text-muted-foreground">Last contact:</span>
                  <span>{formatLastContact(entity.attributes.lastContact)}</span>
                </div>
              )}
            </div>
          )}

          {entity.type === "deal" && (
            <div className="space-y-2">
              {entity.attributes.dealValue && (
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-muted-foreground">Value:</span>
                  <span className="font-semibold">{formatValue(entity.attributes.dealValue)}</span>
                </div>
              )}
              {entity.attributes.dealStage && (
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-muted-foreground">Stage:</span>
                  <Badge variant="outline" className="capitalize">
                    {entity.attributes.dealStage.replace("_", " ")}
                  </Badge>
                </div>
              )}
            </div>
          )}

          {entity.type === "meddpicc" && (
            <div className="space-y-2">
              {entity.attributes.category && (
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-muted-foreground">Category:</span>
                  <Badge variant="outline" className="capitalize">
                    {entity.attributes.category.replace("_", " ")}
                  </Badge>
                </div>
              )}
              {entity.attributes.metric_type && (
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-muted-foreground">Type:</span>
                  <span className="capitalize">{entity.attributes.metric_type.replace("_", " ")}</span>
                </div>
              )}
            </div>
          )}

          {/* Confidence indicator */}
          <div className="pt-2 border-t">
            <div className="flex items-center justify-between text-xs">
              <span className="text-muted-foreground">Confidence</span>
              <div className="flex items-center gap-2">
                <div className="w-16 bg-gray-200 rounded-full h-1">
                  <div 
                    className={cn(
                      "h-1 rounded-full",
                      entity.confidence >= 0.8 ? "bg-green-500" : 
                      entity.confidence >= 0.6 ? "bg-yellow-500" : "bg-red-500"
                    )}
                    style={{ width: `${entity.confidence * 100}%` }}
                  />
                </div>
                <span className="font-mono">{Math.round(entity.confidence * 100)}%</span>
              </div>
            </div>
          </div>
        </div>
      </HoverCardContent>
    </HoverCard>
  )
}