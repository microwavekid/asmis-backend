"use client"

import { useState, useEffect } from "react"
import { DragDropContext, Droppable, Draggable, type DropResult } from "@hello-pangea/dnd"
import { EmailKanbanColumn } from "./email-kanban-column"
import { EmailKanbanCard } from "./email-kanban-card"
import { EmailKanbanFilters } from "./email-kanban-filters"
import { EmailDetailDialog } from "./email-detail-dialog"
import { mockEmails } from "@/lib/mock-emails"
import { mockAccounts, mockOpportunities } from "@/lib/mock-data"
import { Button } from "@/components/ui/button"
import { RefreshCw } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

// Define the email status types
type EmailStatus = "pending" | "drafting" | "approved"

// Define the email interface with additional properties
interface KanbanEmail {
  id: string
  subject: string
  body: string
  status: EmailStatus
  accountId: string
  opportunityId: string
  recipientName: string
  recipientEmail: string
  senderName: string
  senderEmail: string
  priority: "high" | "medium" | "low"
  createdAt: string
  intent: string
}

export function EmailKanbanBoard() {
  const { toast } = useToast()
  const [emails, setEmails] = useState<KanbanEmail[]>([])
  const [filteredEmails, setFilteredEmails] = useState<KanbanEmail[]>([])
  const [selectedEmail, setSelectedEmail] = useState<KanbanEmail | null>(null)
  const [isDetailOpen, setIsDetailOpen] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [filters, setFilters] = useState({
    account: "",
    opportunity: "",
    priority: "",
    dateRange: {
      from: undefined as Date | undefined,
      to: undefined as Date | undefined,
    },
    search: "",
  })

  // Initialize with mock data
  useEffect(() => {
    // Transform mock emails to KanbanEmail format
    const transformedEmails: KanbanEmail[] = mockEmails.map((email) => {
      const account = mockAccounts.find((a) => a.id === email.accountId)
      const opportunity = mockOpportunities.find((o) => o.accountId === email.accountId)

      return {
        id: email.id,
        subject: email.subject,
        body: email.content || "", // Use content instead of body, with fallback
        status: email.status === "pending" ? "pending" : email.status === "draft" ? "drafting" : "approved",
        accountId: email.accountId || "",
        opportunityId: opportunity?.id || "",
        recipientName: email.to ? email.to.split("@")[0] : "", // Extract name from email.to
        recipientEmail: email.to || "",
        senderName: "AI Assistant",
        senderEmail: "ai-assistant@company.com",
        priority: ["high", "medium", "low"][Math.floor(Math.random() * 3)] as "high" | "medium" | "low",
        createdAt: email.createdAt,
        intent: `${account?.name || "Unknown"} - ${email.subject.substring(0, 30)}...`,
      }
    })

    setEmails(transformedEmails)
    setFilteredEmails(transformedEmails)
    setIsLoading(false)
  }, [])

  // Apply filters
  useEffect(() => {
    let result = [...emails]

    if (filters.account) {
      result = result.filter((email) => email.accountId === filters.account)
    }

    if (filters.opportunity) {
      result = result.filter((email) => email.opportunityId === filters.opportunity)
    }

    if (filters.priority) {
      result = result.filter((email) => email.priority === filters.priority)
    }

    if (filters.dateRange.from) {
      result = result.filter((email) => new Date(email.createdAt) >= filters.dateRange.from!)
    }

    if (filters.dateRange.to) {
      result = result.filter((email) => new Date(email.createdAt) <= filters.dateRange.to!)
    }

    if (filters.search) {
      const searchLower = filters.search.toLowerCase()
      result = result.filter(
        (email) =>
          email.subject.toLowerCase().includes(searchLower) ||
          email.body.toLowerCase().includes(searchLower) ||
          email.recipientName.toLowerCase().includes(searchLower) ||
          email.intent.toLowerCase().includes(searchLower),
      )
    }

    setFilteredEmails(result)
  }, [filters, emails])

  // Handle drag and drop
  const handleDragEnd = (result: DropResult) => {
    const { destination, source, draggableId } = result

    // If there's no destination or the item is dropped in the same place
    if (!destination || (destination.droppableId === source.droppableId && destination.index === source.index)) {
      return
    }

    // Find the email that was dragged
    const emailIndex = emails.findIndex((email) => email.id === draggableId)
    if (emailIndex === -1) return

    // Create a new array with the updated status
    const newEmails = [...emails]
    newEmails[emailIndex] = {
      ...newEmails[emailIndex],
      status: destination.droppableId as EmailStatus,
    }

    setEmails(newEmails)

    toast({
      title: "Email moved",
      description: `Email moved to ${
        destination.droppableId === "pending"
          ? "Pending Approval"
          : destination.droppableId === "drafting"
            ? "Drafting"
            : "Approved"
      }`,
    })
  }

  // Handle opening email detail
  const handleOpenEmailDetail = (email: KanbanEmail) => {
    setSelectedEmail(email)
    setIsDetailOpen(true)
  }

  // Handle email approval
  const handleApproveEmail = (emailId: string) => {
    const emailIndex = emails.findIndex((email) => email.id === emailId)
    if (emailIndex === -1) return

    const newEmails = [...emails]
    newEmails[emailIndex] = {
      ...newEmails[emailIndex],
      status: "approved",
    }

    setEmails(newEmails)
    setIsDetailOpen(false)

    toast({
      title: "Email approved",
      description: "Email has been moved to the Approved column",
    })
  }

  // Handle email update
  const handleUpdateEmail = (updatedEmail: KanbanEmail) => {
    const emailIndex = emails.findIndex((email) => email.id === updatedEmail.id)
    if (emailIndex === -1) return

    const newEmails = [...emails]
    newEmails[emailIndex] = updatedEmail

    setEmails(newEmails)
    setSelectedEmail(updatedEmail)

    toast({
      title: "Email updated",
      description: "Email has been updated successfully",
    })
  }

  // Group emails by status
  const pendingEmails = filteredEmails.filter((email) => email.status === "pending")
  const draftingEmails = filteredEmails.filter((email) => email.status === "drafting")
  const approvedEmails = filteredEmails.filter((email) => email.status === "approved")

  // Refresh emails (simulate AI prioritization)
  const handleRefreshPriorities = () => {
    setIsLoading(true)

    // Simulate API call delay
    setTimeout(() => {
      const newEmails = emails.map((email) => ({
        ...email,
        priority: ["high", "medium", "low"][Math.floor(Math.random() * 3)] as "high" | "medium" | "low",
      }))

      setEmails(newEmails)
      setIsLoading(false)

      toast({
        title: "Priorities refreshed",
        description: "AI has reprioritized emails based on latest data",
      })
    }, 1000)
  }

  return (
    <div className="h-full flex flex-col">
      <div className="flex justify-between items-center mb-6">
        <div className="flex items-center gap-2">
          <h1 className="text-2xl font-bold">Email Approval Workflow</h1>
          <Button variant="outline" size="icon" onClick={handleRefreshPriorities} disabled={isLoading}>
            <RefreshCw className={`h-4 w-4 ${isLoading ? "animate-spin" : ""}`} />
          </Button>
        </div>
        <EmailKanbanFilters
          filters={filters}
          setFilters={setFilters}
          accounts={mockAccounts}
          opportunities={mockOpportunities}
        />
      </div>

      <DragDropContext onDragEnd={handleDragEnd}>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 h-[calc(100vh-12rem)]">
          <Droppable droppableId="pending">
            {(provided) => (
              <EmailKanbanColumn
                title="Pending Approval"
                count={pendingEmails.length}
                provided={provided}
                className="bg-amber-50 border-amber-200"
                titleClassName="text-amber-700"
              >
                {pendingEmails.map((email, index) => (
                  <Draggable key={email.id} draggableId={email.id} index={index}>
                    {(provided) => (
                      <EmailKanbanCard email={email} provided={provided} onClick={() => handleOpenEmailDetail(email)} />
                    )}
                  </Draggable>
                ))}
              </EmailKanbanColumn>
            )}
          </Droppable>

          <Droppable droppableId="drafting">
            {(provided) => (
              <EmailKanbanColumn
                title="Drafting"
                count={draftingEmails.length}
                provided={provided}
                className="bg-blue-50 border-blue-200"
                titleClassName="text-blue-700"
              >
                {draftingEmails.map((email, index) => (
                  <Draggable key={email.id} draggableId={email.id} index={index}>
                    {(provided) => (
                      <EmailKanbanCard email={email} provided={provided} onClick={() => handleOpenEmailDetail(email)} />
                    )}
                  </Draggable>
                ))}
              </EmailKanbanColumn>
            )}
          </Droppable>

          <Droppable droppableId="approved">
            {(provided) => (
              <EmailKanbanColumn
                title="Approved"
                count={approvedEmails.length}
                provided={provided}
                className="bg-green-50 border-green-200"
                titleClassName="text-green-700"
              >
                {approvedEmails.map((email, index) => (
                  <Draggable key={email.id} draggableId={email.id} index={index}>
                    {(provided) => (
                      <EmailKanbanCard email={email} provided={provided} onClick={() => handleOpenEmailDetail(email)} />
                    )}
                  </Draggable>
                ))}
              </EmailKanbanColumn>
            )}
          </Droppable>
        </div>
      </DragDropContext>

      {selectedEmail && (
        <EmailDetailDialog
          email={selectedEmail}
          isOpen={isDetailOpen}
          onClose={() => setIsDetailOpen(false)}
          onApprove={handleApproveEmail}
          onUpdate={handleUpdateEmail}
        />
      )}
    </div>
  )
}
