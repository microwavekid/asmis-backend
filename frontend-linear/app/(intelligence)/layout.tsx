"use client"

import React, { useState, ReactNode } from "react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { WorkspaceSelector } from "@/components/intelligence/workspace-selector"
import { NavigationMenu } from "@/components/intelligence/navigation-menu"
import { AIProcessingStatus } from "@/components/intelligence/ai-processing-status"
import { EvidencePanel } from "@/components/intelligence/evidence-panel"
import { CommandPalette } from "@/components/intelligence/command-palette"
import { SmartCaptureDialog } from "@/components/intelligence/smart-capture-dialog"
import { PanelToggleIcon } from "@/components/intelligence/panel-toggle-icon"
import { ViewsDropdown } from "@/components/intelligence/views-dropdown"
import { Plus, Brain } from "lucide-react"

export default function IntelligenceLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const [evidencePanelOpen, setEvidencePanelOpen] = useState(true)
  const [commandPaletteOpen, setCommandPaletteOpen] = useState(false)
  const [smartCaptureOpen, setSmartCaptureOpen] = useState(false)
  const [currentView, setCurrentView] = useState('all')

  // Global keyboard shortcuts
  React.useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault()
        setCommandPaletteOpen(true)
      }
      if ((e.metaKey || e.ctrlKey) && e.key === "u") {
        e.preventDefault()
        setSmartCaptureOpen(true)
      }
    }
    
    window.addEventListener("keydown", handleKeyDown)
    return () => window.removeEventListener("keydown", handleKeyDown)
  }, [])

  return (
    <>
      <CommandPalette 
        open={commandPaletteOpen} 
        onOpenChange={setCommandPaletteOpen}
        onSmartCaptureOpen={() => setSmartCaptureOpen(true)}
      />
      <SmartCaptureDialog 
        open={smartCaptureOpen}
        onOpenChange={setSmartCaptureOpen}
      />
      
      <div className="h-screen bg-[var(--bg-sidebar)] p-0 lg:p-2 xl:p-[15px]">
        <div className="flex h-full bg-[var(--bg-base-color)] lg:rounded-lg overflow-hidden shadow-sm">
          {/* Left Navigation - Separate Column */}
          <nav className="hidden lg:flex w-[180px] xl:w-[200px] 2xl:w-[var(--sidebar-width)] bg-[var(--bg-sidebar)] flex-col border-r border-[var(--bg-border)]">
            <WorkspaceSelector />
            <NavigationMenu />
            <div className="mt-auto">
              <AIProcessingStatus />
            </div>
          </nav>
          
          {/* Workspace Area - Header + Body */}
          <div className="flex-1 flex flex-col">
            {/* Workspace Header - FIXED WIDTH - spans main content + evidence panel ALWAYS */}
            <div className="h-[52px] border-b border-[var(--bg-border)] bg-[var(--bg-base)] flex items-center">
              {/* Main header content */}
              <div className="flex-1 px-3 lg:px-4 xl:px-6 flex items-center justify-between">
                <div className="flex items-center gap-2 lg:gap-3">
                  <h1 className="text-lg font-semibold text-[var(--content-primary)]">
                    Deals
                  </h1>
                  <div className="h-5 w-px bg-[var(--bg-border)]" />
                  <ViewsDropdown
                    currentView={currentView}
                    onViewChange={setCurrentView}
                    onCreateView={() => {
                      // TODO: Implement create view modal
                      console.log('Create new view')
                    }}
                  />
                </div>
                
                <div className="flex items-center gap-2">
                  <Button variant="outline" size="sm" className="h-7 hidden md:flex">
                    <Plus className="mr-2 h-3.5 w-3.5" />
                    <span className="hidden xl:inline">Create Deal</span>
                  </Button>
                  <Button size="sm" className="h-7">
                    <Brain className="mr-2 h-3.5 w-3.5" />
                    <span className="hidden xl:inline">Generate Insights</span>
                  </Button>
                  <div className="w-3" />
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-7 w-7"
                    onClick={() => setEvidencePanelOpen(!evidencePanelOpen)}
                  >
                    <PanelToggleIcon isOpen={evidencePanelOpen} className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>
            
            {/* Workspace Body - Main content + Evidence panel */}
            <div className="flex flex-1 overflow-hidden">
              {/* Main Content Area */}
              <main className="flex-1 overflow-hidden">
                {children}
              </main>
              
              {/* Evidence Panel - Collapsible */}
              <aside 
                className={cn(
                  "bg-[var(--bg-base)] border-l border-[var(--bg-border)] transition-all duration-300 overflow-hidden flex-col",
                  "hidden", // Always hidden now to prevent layout cutoff
                  evidencePanelOpen ? "w-[280px]" : "w-0"
                )}
              >
                {evidencePanelOpen && <EvidencePanel onToggle={() => setEvidencePanelOpen(!evidencePanelOpen)} isOpen={evidencePanelOpen} />}
              </aside>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}