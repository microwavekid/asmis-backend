"use client"

import type { AITask } from "@/lib/mock-suggestions"
import { TaskTable } from "@/components/tasks/task-table"

interface TaskGroupViewProps {
  tasks: AITask[]
  groupBy: string
  onCompleteTask: (taskId: string) => void
  onDismissTask: (taskId: string) => void
  onViewTaskDetails: (task: AITask) => void
  onCompleteWithAI: (taskId: string) => void
}

export function TaskGroupView({
  tasks,
  groupBy,
  onCompleteTask,
  onDismissTask,
  onViewTaskDetails,
  onCompleteWithAI,
}: TaskGroupViewProps) {
  // Group tasks based on the selected grouping option
  const groupedTasks = groupTasks(tasks, groupBy)

  return (
    <div className="space-y-8">
      {Object.entries(groupedTasks).map(([groupName, tasksInGroup]) => (
        <div key={groupName} className="space-y-3">
          <h3 className="text-lg font-medium">{formatGroupTitle(groupBy, groupName)}</h3>
          <TaskTable
            tasks={tasksInGroup}
            onComplete={onCompleteTask}
            onDismiss={onDismissTask}
            onViewDetails={onViewTaskDetails}
            onCompleteWithAI={onCompleteWithAI}
          />
        </div>
      ))}
    </div>
  )
}

// Helper function to group tasks
function groupTasks(tasks: AITask[], groupBy: string): Record<string, AITask[]> {
  const grouped: Record<string, AITask[]> = {}

  tasks.forEach((task) => {
    let groupKey = ""

    switch (groupBy) {
      case "effort":
        groupKey = task.timeEstimate
        break
      case "account":
        groupKey = task.accountId
        break
      case "opportunity":
        groupKey = task.relatedTo?.type === "opportunity" ? task.relatedTo.id : "none"
        break
      case "dueDate":
        // Group by week
        const dueDate = new Date(task.dueDate)
        const today = new Date()
        const diffTime = dueDate.getTime() - today.getTime()
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

        if (diffDays < 0) groupKey = "overdue"
        else if (diffDays === 0) groupKey = "today"
        else if (diffDays <= 7) groupKey = "this-week"
        else if (diffDays <= 14) groupKey = "next-week"
        else groupKey = "later"
        break
      case "priority":
        groupKey = task.priority
        break
      case "type":
        groupKey = task.type
        break
      default:
        groupKey = "ungrouped"
    }

    if (!grouped[groupKey]) {
      grouped[groupKey] = []
    }

    grouped[groupKey].push(task)
  })

  return grouped
}

// Helper function to format group titles
function formatGroupTitle(groupBy: string, groupKey: string): string {
  switch (groupBy) {
    case "effort":
      switch (groupKey) {
        case "0-5":
          return "Quick Tasks (< 5 min)"
        case "15":
          return "Short Tasks (15 min)"
        case "30":
          return "Medium Tasks (30 min)"
        case "30+":
          return "Long Tasks (30+ min)"
        default:
          return groupKey
      }
    case "account":
      // In a real app, you would look up the account name
      return `Account ${groupKey}`
    case "opportunity":
      if (groupKey === "none") return "No Opportunity"
      // In a real app, you would look up the opportunity name
      return `Opportunity ${groupKey}`
    case "dueDate":
      switch (groupKey) {
        case "overdue":
          return "Overdue"
        case "today":
          return "Due Today"
        case "this-week":
          return "Due This Week"
        case "next-week":
          return "Due Next Week"
        case "later":
          return "Due Later"
        default:
          return groupKey
      }
    case "priority":
      return `${groupKey.charAt(0).toUpperCase() + groupKey.slice(1)} Priority`
    case "type":
      switch (groupKey) {
        case "research":
          return "Research"
        case "follow-up":
          return "Follow-up"
        case "preparation":
          return "Preparation"
        case "outreach":
          return "Outreach"
        case "analysis":
          return "Analysis"
        default:
          return groupKey
      }
    default:
      return groupKey
  }
}
