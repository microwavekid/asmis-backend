"use client"

import { useState } from "react"
import { TaskDetailModal } from "@/components/tasks/task-detail-modal"
import { TaskFilters } from "@/components/tasks/task-filters"
import { TaskGroupView } from "@/components/tasks/task-group-view"
import { CompletedTasksDrawer } from "@/components/tasks/completed-tasks-drawer"
import type { AITask } from "@/lib/mock-suggestions"

type GroupBy = "effort" | "account" | "opportunity" | "dueDate" | "priority" | "type"

interface TaskDashboardProps {
  initialTasks: AITask[]
}

export function TaskDashboard({ initialTasks }: TaskDashboardProps) {
  const [tasks, setTasks] = useState<AITask[]>(initialTasks)
  const [completedTasks, setCompletedTasks] = useState<AITask[]>([])
  const [groupBy, setGroupBy] = useState<GroupBy>("effort")
  const [selectedTask, setSelectedTask] = useState<AITask | null>(null)

  const handleCompleteTask = (taskId: string) => {
    const taskToComplete = tasks.find((task) => task.id === taskId)
    if (taskToComplete) {
      setTasks(tasks.filter((task) => task.id !== taskId))
      setCompletedTasks([...completedTasks, { ...taskToComplete, completed: true }])
    }
  }

  const handleDismissTask = (taskId: string) => {
    setTasks(tasks.filter((task) => task.id !== taskId))
  }

  const handleCompleteWithAI = (taskId: string) => {
    // In a real app, this would trigger an AI process
    // For now, we'll just mark it as completed
    handleCompleteTask(taskId)
  }

  const handleViewTaskDetails = (task: AITask) => {
    setSelectedTask(task)
  }

  const handleCloseTaskDetails = () => {
    setSelectedTask(null)
  }

  return (
    <div>
      <TaskFilters groupBy={groupBy} onGroupByChange={setGroupBy} />

      <TaskGroupView
        tasks={tasks}
        groupBy={groupBy}
        onCompleteTask={handleCompleteTask}
        onDismissTask={handleDismissTask}
        onCompleteWithAI={handleCompleteWithAI}
        onViewTaskDetails={handleViewTaskDetails}
      />

      <CompletedTasksDrawer completedTasks={completedTasks} onViewTaskDetails={handleViewTaskDetails} />

      {selectedTask && <TaskDetailModal task={selectedTask} open={!!selectedTask} onClose={handleCloseTaskDetails} />}
    </div>
  )
}
