import { Header } from "@/components/layout/header"
import { EmailKanbanBoard } from "@/components/emails/kanban/email-kanban-board"

export default function EmailKanbanPage() {
  return (
    <div className="flex flex-col h-screen">
      <Header title="Email Approval Kanban" />
      <div className="flex-1 p-6 overflow-hidden">
        <EmailKanbanBoard />
      </div>
    </div>
  )
}
