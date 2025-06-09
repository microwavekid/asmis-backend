"use client"

import type { AITask } from "@/lib/mock-suggestions"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Clock, Calendar, Bot, X } from "lucide-react"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

interface TaskCardProps {
  task: AITask
  onComplete: () => void
  onDismiss: () => void
  onViewDetails: () => void
  onCompleteWithAI: () => void
}

export function TaskCard({ task, onComplete, onDismiss, onViewDetails, onCompleteWithAI }: TaskCardProps) {
  // Determine if this task can be completed by AI
  // For this demo, let's say research and analysis tasks can be done by AI
  const canBeCompletedByAI = ["research", "analysis"].includes(task.type)

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

  return (
    <Card className="overflow-hidden hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <div className="flex items-start gap-3">
          {/* Completion circle */}
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <button
                  onClick={onComplete}
                  className="mt-1 flex-shrink-0 h-5 w-5 rounded-full border-2 border-gray-300 hover:border-primary focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
                  aria-label="Complete task"
                />
              </TooltipTrigger>
              <TooltipContent>
                <p>Mark as complete</p>
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>

          <div className="flex-1 min-w-0">
            {/* Task title and badges */}
            <div className="space-y-1.5">
              <h3
                className="font-medium text-sm leading-tight cursor-pointer hover:text-primary"
                onClick={onViewDetails}
              >
                {task.title}
              </h3>

              <div className="flex flex-wrap gap-1.5">
                <Badge className={getPriorityColor(task.priority)} variant="secondary">
                  {task.priority}
                </Badge>

                <Badge variant="outline" className="flex items-center gap-1 text-xs">
                  <Clock className="h-3 w-3" />
                  {task.timeEstimate === "0-5" ? "< 5 min" : `${task.timeEstimate} min`}
                </Badge>
              </div>
            </div>

            {/* Due date */}
            <div className="mt-2 flex items-center text-xs text-muted-foreground">
              <Calendar className="h-3 w-3 mr-1" />
              Due {formatDate(task.dueDate)}
            </div>

            {/* Action buttons */}
            <div className="mt-3 flex items-center justify-between">
              <div className="flex gap-1">
                {canBeCompletedByAI && (
                  <TooltipProvider>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <Button variant="ghost" size="icon" className="h-7 w-7" onClick={onCompleteWithAI}>
                          <Bot className="h-4 w-4" />
                        </Button>
                      </TooltipTrigger>
                      <TooltipContent>
                        <p>Complete with AI</p>
                      </TooltipContent>
                    </Tooltip>
                  </TooltipProvider>
                )}

                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button variant="ghost" size="icon" className="h-7 w-7" onClick={onDismiss}>
                        <X className="h-4 w-4" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>
                      <p>Dismiss task</p>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </div>

              <Button variant="ghost" size="sm" className="text-xs h-7" onClick={onViewDetails}>
                Details
              </Button>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
