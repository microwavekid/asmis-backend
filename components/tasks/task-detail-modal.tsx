"use client"

import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Clock, XCircle } from "lucide-react"
import type { AITask } from "@/lib/mock-suggestions"

interface TaskDetailModalProps {
  task: AITask | null
  isOpen: boolean
  onClose: () => void
  onDismiss: (taskId: string) => void
}

export function TaskDetailModal({ task, isOpen, onClose, onDismiss }: TaskDetailModalProps) {
  if (!task) return null

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "high":
        return "bg-red-100 text-red-800 hover:bg-red-100"
      case "medium":
        return "bg-amber-100 text-amber-800 hover:bg-amber-100"
      case "low":
        return "bg-green-100 text-green-800 hover:bg-green-100"
      default:
        return ""
    }
  }

  const getTypeColor = (type: string) => {
    switch (type) {
      case "research":
        return "bg-purple-100 text-purple-800 hover:bg-purple-100"
      case "follow-up":
        return "bg-blue-100 text-blue-800 hover:bg-blue-100"
      case "preparation":
        return "bg-indigo-100 text-indigo-800 hover:bg-indigo-100"
      case "outreach":
        return "bg-green-100 text-green-800 hover:bg-green-100"
      case "analysis":
        return "bg-orange-100 text-orange-800 hover:bg-orange-100"
      default:
        return ""
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString("en-US", { month: "short", day: "numeric" })
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle className="text-xl">{task.title}</DialogTitle>
        </DialogHeader>

        <div className="space-y-4 mt-2">
          <div className="flex flex-wrap gap-2">
            <Badge className={getPriorityColor(task.priority)}>{task.priority} priority</Badge>
            <Badge className={getTypeColor(task.type)}>{task.type}</Badge>
            <Badge variant="outline" className="flex items-center gap-1">
              <Clock className="h-3 w-3" />
              {task.timeEstimate === "0-5" ? "< 5 min" : `${task.timeEstimate} min`}
            </Badge>
            {task.relatedTo && (
              <Badge variant="outline">
                {task.relatedTo.type}: {task.relatedTo.name}
              </Badge>
            )}
          </div>

          <div>
            <h4 className="text-sm font-medium mb-1">Description</h4>
            <p className="text-sm">{task.description}</p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <h4 className="text-sm font-medium mb-1">Due Date</h4>
              <p className="text-sm">{formatDate(task.dueDate)}</p>
            </div>
            <div>
              <h4 className="text-sm font-medium mb-1">Created</h4>
              <p className="text-sm">{formatDate(task.createdAt)}</p>
            </div>
          </div>

          <div className="flex justify-end pt-4">
            <Button variant="outline" onClick={() => onDismiss(task.id)}>
              <XCircle className="h-4 w-4 mr-2" />
              Dismiss Task
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
