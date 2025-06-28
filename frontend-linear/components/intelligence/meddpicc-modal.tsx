// PATTERN_REF: MEDDPIC_ORCHESTRATOR_PATTERN
// DECISION_REF: DEC_2025-06-24_006: MEDDPICC detailed analysis modal

"use client"

import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { MEDDPICCCard } from "./meddpicc-card"
import { Skeleton } from "@/components/ui/skeleton"
import { Card, CardContent } from "@/components/ui/card"
import type { MEDDPICCAnalysis, Evidence } from "@/types/meddpicc"

interface MEDDPICCModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  analysis?: MEDDPICCAnalysis | null
  evidence: Evidence[]
  dealName: string
  isLoading?: boolean
}

export function MEDDPICCModal({ 
  open, 
  onOpenChange, 
  analysis, 
  evidence, 
  dealName,
  isLoading = false
}: MEDDPICCModalProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>MEDDPICC Analysis - {dealName}</DialogTitle>
          <DialogDescription>
            Detailed qualification analysis with evidence backing
          </DialogDescription>
        </DialogHeader>
        
        {isLoading ? (
          <Card>
            <CardContent className="p-6 space-y-4">
              <div className="flex items-center justify-between">
                <Skeleton className="h-6 w-48" />
                <Skeleton className="h-8 w-16" />
              </div>
              <Skeleton className="h-2 w-full" />
              <div className="space-y-3">
                {[...Array(8)].map((_, i) => (
                  <div key={i} className="border rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <Skeleton className="h-5 w-32" />
                      <Skeleton className="h-6 w-12" />
                    </div>
                    <Skeleton className="h-4 w-full" />
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        ) : analysis ? (
          <MEDDPICCCard 
            analysis={analysis}
            evidence={evidence}
            onEvidenceClick={(evidenceItem) => {
              // TODO: Integrate with evidence panel
              console.log("Evidence clicked:", evidenceItem)
            }}
          />
        ) : (
          <Card>
            <CardContent className="p-6 text-center">
              <p className="text-muted-foreground">No MEDDPICC analysis available for this deal.</p>
            </CardContent>
          </Card>
        )}
      </DialogContent>
    </Dialog>
  )
}