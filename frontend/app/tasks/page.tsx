import { TaskDashboard } from "@/components/tasks/task-dashboard"
import { mockAITasks } from "@/lib/mock-suggestions"

export default function TasksPage() {
  return (
    <div className="container mx-auto py-6">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Tasks</h1>
      </div>
      <TaskDashboard initialTasks={mockAITasks} />
    </div>
  )
}
