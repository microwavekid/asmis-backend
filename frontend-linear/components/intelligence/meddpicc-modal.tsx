// PATTERN_REF: MEDDPIC_ORCHESTRATOR_PATTERN
// DECISION_REF: DEC_2025-06-24_006: MEDDPICC detailed analysis modal

"use client"

import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { MEDDPICCCard } from "./meddpicc-card"
import type { MEDDPICCAnalysis, Evidence } from "@/types/meddpicc"

interface MEDDPICCModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  analysis: MEDDPICCAnalysis
  evidence: Evidence[]
  dealName: string
}

export function MEDDPICCModal({ 
  open, 
  onOpenChange, 
  analysis, 
  evidence, 
  dealName 
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
        
        <MEDDPICCCard 
          analysis={analysis}
          evidence={evidence}
          onEvidenceClick={(evidenceItem) => {
            // TODO: Integrate with evidence panel
            console.log("Evidence clicked:", evidenceItem)
          }}
        />
      </DialogContent>
    </Dialog>
  )
}