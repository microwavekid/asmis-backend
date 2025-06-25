import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { ScrollArea } from "@/components/ui/scroll-area"

export function GlobalTasksOverview() {
  // Mock data for tasks
  const taskCategories = [
    {
      name: "Follow-ups",
      completed: 12,
      total: 18,
      percentage: 67,
    },
    {
      name: "Proposals",
      completed: 5,
      total: 8,
      percentage: 63,
    },
    {
      name: "Meetings",
      completed: 15,
      total: 15,
      percentage: 100,
    },
    {
      name: "Research",
      completed: 7,
      total: 12,
      percentage: 58,
    },
  ]

  const recentTasks = [
    {
      id: 1,
      title: "Send follow-up email to Acme Corp",
      dueDate: "Today",
      status: "pending",
    },
    {
      id: 2,
      title: "Prepare presentation for TechGiant meeting",
      dueDate: "Tomorrow",
      status: "in-progress",
    },
    {
      id: 3,
      title: "Review proposal for NextGen",
      dueDate: "Yesterday",
      status: "overdue",
    },
    {
      id: 4,
      title: "Schedule demo with Finance Solutions Inc",
      dueDate: "Next week",
      status: "pending",
    },
  ]

  return (
    <Card className="h-[400px]">
      <CardHeader>
        <CardTitle>Tasks Overview</CardTitle>
        <CardDescription>Progress across all task categories</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {taskCategories.map((category) => (
            <div key={category.name} className="space-y-1">
              <div className="flex items-center justify-between text-sm">
                <span>{category.name}</span>
                <span className="text-muted-foreground">
                  {category.completed}/{category.total}
                </span>
              </div>
              <Progress value={category.percentage} className="h-2" />
            </div>
          ))}
        </div>

        <div className="mt-6">
          <h4 className="mb-3 text-sm font-medium">Recent Tasks</h4>
          <ScrollArea className="h-[120px]">
            <div className="space-y-2">
              {recentTasks.map((task) => (
                <div key={task.id} className="flex items-center justify-between rounded-md border px-3 py-2">
                  <span className="text-sm">{task.title}</span>
                  <span
                    className={`text-xs ${task.status === "overdue" ? "text-destructive" : "text-muted-foreground"}`}
                  >
                    {task.dueDate}
                  </span>
                </div>
              ))}
            </div>
          </ScrollArea>
        </div>
      </CardContent>
    </Card>
  )
}
