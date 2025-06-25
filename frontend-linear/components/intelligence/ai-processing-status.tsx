"use client"

import { useEffect, useState } from "react"
import { FileText, Loader2, CheckCircle, AlertCircle } from "lucide-react"
import { Progress } from "@/components/ui/progress"
import { cn } from "@/lib/utils"
import type { ProcessingItem } from "@/types/intelligence"

// Mock data - in real app this would come from WebSocket/API
const mockProcessingQueue: ProcessingItem[] = [
  {
    id: "1",
    type: "transcript",
    name: "Demo Call - Sarah Chen",
    status: "processing",
    progress: 65,
    currentStep: "Extracting MEDDPICC insights...",
  },
  {
    id: "2",
    type: "email",
    name: "Follow-up thread",
    status: "queued",
  },
]

export function AIProcessingStatus() {
  const [queue, setQueue] = useState<ProcessingItem[]>(mockProcessingQueue)
  
  // Simulate progress updates
  useEffect(() => {
    const interval = setInterval(() => {
      setQueue(prev => prev.map(item => {
        if (item.status === 'processing' && item.progress && item.progress < 100) {
          return {
            ...item,
            progress: Math.min(item.progress + 5, 100)
          }
        }
        return item
      }))
    }, 1000)
    
    return () => clearInterval(interval)
  }, [])
  
  const activeItems = queue.filter(item => 
    item.status === 'processing' || item.status === 'queued'
  )
  
  if (activeItems.length === 0) return null
  
  return (
    <div className="p-4 border-t border-[var(--bg-border)]">
      <h4 className="text-xs font-medium text-[var(--content-secondary)] mb-3">
        AI Processing
      </h4>
      
      <div className="space-y-3">
        {activeItems.map((item) => (
          <ProcessingItemDisplay key={item.id} item={item} />
        ))}
      </div>
    </div>
  )
}

function ProcessingItemDisplay({ item }: { item: ProcessingItem }) {
  const getIcon = () => {
    switch (item.status) {
      case 'processing':
        return <Loader2 className="h-4 w-4 animate-spin text-[var(--ai-processing)]" />
      case 'complete':
        return <CheckCircle className="h-4 w-4 text-[var(--confidence-high)]" />
      case 'failed':
        return <AlertCircle className="h-4 w-4 text-[var(--confidence-low)]" />
      default:
        return <FileText className="h-4 w-4 text-[var(--content-secondary)]" />
    }
  }
  
  return (
    <div className="space-y-2">
      <div className="flex items-center gap-3">
        <div className="relative">
          {getIcon()}
          {item.status === 'processing' && (
            <div className="absolute inset-0 animate-pulse bg-[var(--ai-processing)] rounded-full opacity-20" />
          )}
        </div>
        
        <div className="flex-1 min-w-0">
          <p className="text-sm truncate text-[var(--content-primary)]">
            {item.name}
          </p>
          <p className="text-xs text-[var(--content-secondary)]">
            {item.currentStep || 'Queued for processing'}
          </p>
        </div>
      </div>
      
      {item.status === 'processing' && item.progress && (
        <Progress 
          value={item.progress} 
          className="h-1"
          indicatorClassName="bg-[var(--ai-processing)]"
        />
      )}
    </div>
  )
}