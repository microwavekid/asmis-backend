"use client"

import type { AITask } from "@/lib/mock-suggestions"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Bot, Clock, Calendar, Trash2 } from "lucide-react"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

interface TaskTableProps {
  tasks: AITask[]
  onComplete: (taskId: string) => void
  onDismiss: (taskId: string) => void
  onViewDetails: (task: AITask) => void
  onCompleteWithAI: (taskId: string) => void
}

export function TaskTable({ tasks, onComplete, onDismiss, onViewDetails, onCompleteWithAI }: TaskTableProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString("en-US", { month: "short", day: "numeric" })
  }

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

  // Determine if a task can be completed by AI
  const canBeCompletedByAI = (task: AITask) => {
    return ["research", "analysis"].includes(task.type)
  }

  return (
    <div className="border rounded-md overflow-hidden">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[50px]">Done</TableHead>
            <TableHead>Task</TableHead>
            <TableHead className="w-[120px]">Priority</TableHead>
            <TableHead className="w-[120px]">Effort</TableHead>
            <TableHead className="w-[120px]">Due Date</TableHead>
            <TableHead className="w-[180px]">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {tasks.map((task) => (
            <TableRow key={task.id} className="hover:bg-muted/50">
              <TableCell className="py-2">
                <Checkbox
                  checked={task.status === "completed"}
                  onCheckedChange={() => onComplete(task.id)}
                  aria-label="Mark task as complete"
                />
              </TableCell>
              <TableCell className="py-2">
                <div className="font-medium cursor-pointer hover:text-primary" onClick={() => onViewDetails(task)}>
                  {task.title}
                </div>
              </TableCell>
              <TableCell className="py-2">
                <Badge className={getPriorityColor(task.priority)} variant="secondary">
                  {task.priority}
                </Badge>
              </TableCell>
              <TableCell className="py-2">
                <div className="flex items-center gap-1 text-sm text-muted-foreground">
                  <Clock className="h-3.5 w-3.5" />
                  {task.timeEstimate === "0-5" ? "< 5 min" : `${task.timeEstimate} min`}
                </div>
              </TableCell>
              <TableCell className="py-2">
                <div className="flex items-center gap-1 text-sm text-muted-foreground">
                  <Calendar className="h-3.5 w-3.5" />
                  {formatDate(task.dueDate)}
                </div>
              </TableCell>
              <TableCell className="py-2">
                <div className="flex items-center gap-2">
                  {canBeCompletedByAI(task) && (
                    <Button
                      variant="outline"
                      size="sm"
                      className="h-8 gap-1.5 bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100 hover:text-blue-800"
                      onClick={() => onCompleteWithAI(task.id)}
                    >
                      <Bot className="h-3.5 w-3.5" />
                      Complete with AI
                    </Button>
                  )}

                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <Button
                          variant="outline"
                          size="icon"
                          className="h-8 w-8 text-red-500 hover:text-red-600 hover:bg-red-50"
                          onClick={() => onDismiss(task.id)}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </TooltipTrigger>
                      <TooltipContent>
                        <p>Dismiss task</p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
