"use client"

import type { DraggableProvided } from "@hello-pangea/dnd"
import { Card, CardContent } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { mockAccounts, mockOpportunities } from "@/lib/mock-data"
import { CalendarDays, User } from "lucide-react"

interface EmailKanbanCardProps {
  email: any
  provided: DraggableProvided
  onClick: () => void
}

export function EmailKanbanCard({ email, provided, onClick }: EmailKanbanCardProps) {
  const account = mockAccounts.find((a) => a.id === (email.accountId || ""))
  const opportunity = mockOpportunities.find((o) => o.id === (email.opportunityId || ""))

  // Format date
  const formattedDate = new Date(email.createdAt).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
  })

  return (
    <div ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps} onClick={onClick}>
      <Card className="cursor-pointer hover:shadow-md transition-shadow">
        <CardContent className="p-4 space-y-3">
          <div className="flex justify-between items-start">
            <div className="flex items-center gap-2">
              <Avatar className="h-6 w-6">
                <AvatarImage src={account?.logo || "/placeholder.svg"} alt={account?.name} />
                <AvatarFallback>{account?.name.charAt(0)}</AvatarFallback>
              </Avatar>
              <span className="text-sm font-medium truncate max-w-[120px]">{account?.name || "Unknown Account"}</span>
            </div>
            <Badge
              className={
                email.priority === "high"
                  ? "bg-red-100 text-red-800 hover:bg-red-100"
                  : email.priority === "medium"
                    ? "bg-amber-100 text-amber-800 hover:bg-amber-100"
                    : "bg-green-100 text-green-800 hover:bg-green-100"
              }
            >
              {email.priority}
            </Badge>
          </div>

          <div>
            <h3 className="font-medium line-clamp-1">{email.subject}</h3>
            <p className="text-sm text-muted-foreground line-clamp-2 mt-1">{email.intent}</p>
          </div>

          <div className="pt-2 border-t flex justify-between items-center text-xs text-muted-foreground">
            <div className="flex items-center gap-1">
              <User className="h-3 w-3" />
              <span className="truncate max-w-[100px]">{email.recipientName}</span>
            </div>
            <div className="flex items-center gap-1">
              <CalendarDays className="h-3 w-3" />
              <span>{formattedDate}</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
