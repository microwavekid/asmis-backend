"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { useParams, useRouter } from "next/navigation"
import { Header } from "@/components/layout/header"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ArrowLeft, ChevronDown, ChevronRight, XCircle } from "lucide-react"
import Link from "next/link"
import { mockAccounts } from "@/lib/mock-data"
import {
  getTasksForAccount,
  getEmailSuggestionsForAccount,
  getTasksByTimeEstimate,
  type AITask,
  type AIEmailSuggestion,
} from "@/lib/mock-suggestions"
import { TaskDetailModal } from "@/components/tasks/task-detail-modal"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

export default function AccountSuggestionsPage() {
  const params = useParams()
  const router = useRouter()
  const accountId = params.id as string

  const [account, setAccount] = useState<any>(null)
  const [tasks, setTasks] = useState<AITask[]>([])
  const [completedTasks, setCompletedTasks] = useState<AITask[]>([])
  const [emailSuggestions, setEmailSuggestions] = useState<AIEmailSuggestion[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedTask, setSelectedTask] = useState<AITask | null>(null)
  const [isDetailOpen, setIsDetailOpen] = useState(false)
  const [isCompletedOpen, setIsCompletedOpen] = useState(false)
  const [fadingTaskIds, setFadingTaskIds] = useState<string[]>([])

  useEffect(() => {
    // Find the account
    const foundAccount = mockAccounts.find((acc) => acc.id === accountId)
    if (!foundAccount) {
      router.push("/accounts")
      return
    }

    setAccount(foundAccount)

    // Get tasks and email suggestions
    const accountTasks = getTasksForAccount(accountId)
    const accountEmails = getEmailSuggestionsForAccount(accountId)

    setTasks(accountTasks)
    setEmailSuggestions(accountEmails)
    setLoading(false)
  }, [accountId, router])

  const handleTaskClick = (task: AITask) => {
    setSelectedTask(task)
    setIsDetailOpen(true)
  }

  const handleTaskComplete = (taskId: string) => {
    // Add to fading tasks
    setFadingTaskIds((prev) => [...prev, taskId])

    // After animation, move to completed and remove from active
    setTimeout(() => {
      const taskToComplete = tasks.find((t) => t.id === taskId)
      if (taskToComplete) {
        setCompletedTasks((prev) => [...prev, { ...taskToComplete, status: "completed" }])
        setTasks((prev) => prev.filter((t) => t.id !== taskId))
      }
      setFadingTaskIds((prev) => prev.filter((id) => id !== taskId))
    }, 500)
  }

  const handleTaskDismiss = (taskId: string) => {
    setTasks((prev) => prev.filter((t) => t.id !== taskId))
    setIsDetailOpen(false)
  }

  if (loading) {
    return (
      <div className="flex flex-col min-h-screen">
        <Header title="AI Suggestions" />
        <main className="flex-1 p-6">
          <div className="animate-pulse">
            <div className="h-8 w-64 bg-muted rounded mb-4"></div>
            <div className="h-4 w-96 bg-muted rounded mb-8"></div>
            <div className="grid gap-6 grid-cols-1 md:grid-cols-2">
              <div className="h-[400px] bg-muted rounded"></div>
              <div className="h-[400px] bg-muted rounded"></div>
            </div>
          </div>
        </main>
      </div>
    )
  }

  // Group tasks by time estimate
  const quickTasks = getTasksByTimeEstimate(tasks, "0-5")
  const fifteenMinTasks = getTasksByTimeEstimate(tasks, "15")
  const thirtyMinTasks = getTasksByTimeEstimate(tasks, "30")
  const longTasks = getTasksByTimeEstimate(tasks, "30+")

  return (
    <div className="flex flex-col min-h-screen">
      <Header title="AI Suggestions" />
      <main className="flex-1 p-6">
        <div className="mb-6">
          <div className="flex items-center gap-2 mb-2">
            <Button variant="ghost" size="icon" asChild>
              <Link href="/accounts">
                <ArrowLeft className="h-4 w-4" />
              </Link>
            </Button>
            <h1 className="text-2xl font-bold">{account.name}: AI Suggestions</h1>
          </div>
          <p className="text-muted-foreground">
            AI-generated suggestions to help you engage with this account more effectively.
          </p>
        </div>

        <Tabs defaultValue="tasks" className="space-y-6">
          <TabsList>
            <TabsTrigger value="tasks">Tasks ({tasks.length})</TabsTrigger>
            <TabsTrigger value="emails">Email Approvals ({emailSuggestions.length})</TabsTrigger>
          </TabsList>

          <TabsContent value="tasks">
            <div className="space-y-6">
              {/* Quick Tasks (0-5 min) */}
              <Card>
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg font-medium">Quick Tasks (0-5 min)</CardTitle>
                    <Badge className="bg-blue-100 text-blue-800">{quickTasks.length}</Badge>
                  </div>
                  <CardDescription>Tasks that take less than 5 minutes to complete</CardDescription>
                </CardHeader>
                <CardContent>
                  {quickTasks.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                      {quickTasks.map((task) => (
                        <MiniTaskCard
                          key={task.id}
                          task={task}
                          onClick={() => handleTaskClick(task)}
                          onComplete={() => handleTaskComplete(task.id)}
                          isFading={fadingTaskIds.includes(task.id)}
                        />
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-muted-foreground">No quick tasks available</div>
                  )}
                </CardContent>
              </Card>

              {/* 15 Minute Tasks */}
              <Card>
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg font-medium">15 Minute Tasks</CardTitle>
                    <Badge className="bg-blue-100 text-blue-800">{fifteenMinTasks.length}</Badge>
                  </div>
                  <CardDescription>Tasks that take around 15 minutes to complete</CardDescription>
                </CardHeader>
                <CardContent>
                  {fifteenMinTasks.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                      {fifteenMinTasks.map((task) => (
                        <MiniTaskCard
                          key={task.id}
                          task={task}
                          onClick={() => handleTaskClick(task)}
                          onComplete={() => handleTaskComplete(task.id)}
                          isFading={fadingTaskIds.includes(task.id)}
                        />
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-muted-foreground">No 15-minute tasks available</div>
                  )}
                </CardContent>
              </Card>

              {/* 30 Minute Tasks */}
              <Card>
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg font-medium">30 Minute Tasks</CardTitle>
                    <Badge className="bg-blue-100 text-blue-800">{thirtyMinTasks.length}</Badge>
                  </div>
                  <CardDescription>Tasks that take around 30 minutes to complete</CardDescription>
                </CardHeader>
                <CardContent>
                  {thirtyMinTasks.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                      {thirtyMinTasks.map((task) => (
                        <MiniTaskCard
                          key={task.id}
                          task={task}
                          onClick={() => handleTaskClick(task)}
                          onComplete={() => handleTaskComplete(task.id)}
                          isFading={fadingTaskIds.includes(task.id)}
                        />
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-muted-foreground">No 30-minute tasks available</div>
                  )}
                </CardContent>
              </Card>

              {/* Longer Tasks (30+ min) */}
              <Card>
                <CardHeader className="pb-3">
                  <div className="flex items-center justify-between">
                    <CardTitle className="text-lg font-medium">Longer Tasks (30+ min)</CardTitle>
                    <Badge className="bg-blue-100 text-blue-800">{longTasks.length}</Badge>
                  </div>
                  <CardDescription>Tasks that take more than 30 minutes to complete</CardDescription>
                </CardHeader>
                <CardContent>
                  {longTasks.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                      {longTasks.map((task) => (
                        <MiniTaskCard
                          key={task.id}
                          task={task}
                          onClick={() => handleTaskClick(task)}
                          onComplete={() => handleTaskComplete(task.id)}
                          isFading={fadingTaskIds.includes(task.id)}
                        />
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-muted-foreground">No longer tasks available</div>
                  )}
                </CardContent>
              </Card>

              {/* Completed Tasks Section */}
              {completedTasks.length > 0 && (
                <Card>
                  <Collapsible open={isCompletedOpen} onOpenChange={setIsCompletedOpen}>
                    <div className="border-b">
                      <CollapsibleTrigger className="flex w-full items-center justify-between p-4 hover:bg-muted/50 cursor-pointer">
                        <div className="flex items-center gap-2">
                          <h3 className="text-lg font-medium">Completed Tasks</h3>
                          <Badge>{completedTasks.length}</Badge>
                        </div>
                        {isCompletedOpen ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
                      </CollapsibleTrigger>
                    </div>
                    <CollapsibleContent>
                      <div className="p-4">
                        <div className="rounded-md border">
                          <Table>
                            <TableHeader>
                              <TableRow>
                                <TableHead className="w-[30px]"></TableHead>
                                <TableHead>Task</TableHead>
                                <TableHead>Priority</TableHead>
                                <TableHead>Type</TableHead>
                                <TableHead>Time Estimate</TableHead>
                                <TableHead>Due Date</TableHead>
                              </TableRow>
                            </TableHeader>
                            <TableBody>
                              {completedTasks.map((task) => (
                                <TableRow key={task.id}>
                                  <TableCell>
                                    <div className="w-4 h-4 rounded-full border-2 border-green-500 bg-green-500 flex items-center justify-center">
                                      <svg
                                        width="10"
                                        height="10"
                                        viewBox="0 0 10 10"
                                        fill="none"
                                        xmlns="http://www.w3.org/2000/svg"
                                      >
                                        <path
                                          d="M8.33334 2.5L3.75001 7.08333L1.66667 5"
                                          stroke="white"
                                          strokeWidth="1.5"
                                          strokeLinecap="round"
                                          strokeLinejoin="round"
                                        />
                                      </svg>
                                    </div>
                                  </TableCell>
                                  <TableCell>
                                    <div>
                                      <div className="font-medium">{task.title}</div>
                                      <div className="text-xs text-muted-foreground">{task.description}</div>
                                    </div>
                                  </TableCell>
                                  <TableCell>
                                    <Badge
                                      className={
                                        task.priority === "high"
                                          ? "bg-red-100 text-red-800"
                                          : task.priority === "medium"
                                            ? "bg-amber-100 text-amber-800"
                                            : "bg-green-100 text-green-800"
                                      }
                                    >
                                      {task.priority}
                                    </Badge>
                                  </TableCell>
                                  <TableCell>{task.type}</TableCell>
                                  <TableCell>
                                    {task.timeEstimate === "0-5" ? "< 5 min" : `${task.timeEstimate} min`}
                                  </TableCell>
                                  <TableCell>
                                    {new Date(task.dueDate).toLocaleDateString("en-US", {
                                      month: "short",
                                      day: "numeric",
                                    })}
                                  </TableCell>
                                </TableRow>
                              ))}
                            </TableBody>
                          </Table>
                        </div>
                      </div>
                    </CollapsibleContent>
                  </Collapsible>
                </Card>
              )}
            </div>
          </TabsContent>

          <TabsContent value="emails">
            <Card>
              <CardHeader>
                <CardTitle>Email Approval Suggestions</CardTitle>
                <CardDescription>AI-generated emails that need your review and approval before sending</CardDescription>
              </CardHeader>
              <CardContent>
                {emailSuggestions.length > 0 ? (
                  <div className="space-y-4">
                    {emailSuggestions.map((email) => (
                      <EmailSuggestionCard key={email.id} email={email} />
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8 text-muted-foreground">No email suggestions available</div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>

      {/* Task Detail Modal */}
      <TaskDetailModal
        task={selectedTask}
        isOpen={isDetailOpen}
        onClose={() => setIsDetailOpen(false)}
        onDismiss={handleTaskDismiss}
      />
    </div>
  )
}

// Mini Task Card Component
function MiniTaskCard({
  task,
  onClick,
  onComplete,
  isFading,
}: {
  task: AITask
  onClick: () => void
  onComplete: () => void
  isFading: boolean
}) {
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

  const handleCheckboxClick = (e: React.MouseEvent) => {
    e.stopPropagation()
    onComplete()
  }

  return (
    <div
      className={`border rounded-lg p-3 hover:bg-muted/50 transition-all duration-500 h-full flex flex-col cursor-pointer ${
        isFading ? "opacity-0 scale-95" : "opacity-100 scale-100"
      }`}
      onClick={onClick}
    >
      <div className="flex items-start gap-2 mb-1">
        <div
          className="w-4 h-4 mt-1 rounded-full border-2 border-gray-300 hover:border-gray-500 flex-shrink-0 cursor-pointer"
          onClick={handleCheckboxClick}
        />
        <div className="flex-1 flex justify-between">
          <h3 className="font-medium text-sm line-clamp-2">{task.title}</h3>
          <Badge className={`${getPriorityColor(task.priority)} ml-1 shrink-0`} variant="outline">
            {task.priority}
          </Badge>
        </div>
      </div>
      <p className="text-xs text-muted-foreground mb-3 line-clamp-2 flex-grow pl-6">{task.description}</p>
      <div className="flex justify-end gap-2 mt-auto">
        <Button
          size="sm"
          variant="outline"
          className="h-8 text-xs px-2"
          onClick={(e) => {
            e.stopPropagation()
            // Dismiss functionality would go here
          }}
        >
          <XCircle className="h-3 w-3 mr-1" />
          Dismiss
        </Button>
      </div>
    </div>
  )
}

// Email Suggestion Card Component
function EmailSuggestionCard({ email }: { email: AIEmailSuggestion }) {
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

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString("en-US", { month: "short", day: "numeric" })
  }

  return (
    <div className="border rounded-lg p-4 hover:bg-muted/50 transition-colors">
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-medium">{email.subject}</h3>
        <Badge className={getPriorityColor(email.priority)}>{email.priority}</Badge>
      </div>
      <p className="text-sm text-muted-foreground mb-3">{email.preview}</p>
      <div className="flex flex-wrap gap-2 mb-3">
        <Badge variant="outline">To: {email.recipientName}</Badge>
        <Badge variant="secondary">{email.intent}</Badge>
      </div>
      <div className="flex justify-between items-center">
        <span className="text-xs text-muted-foreground">Generated: {formatDate(email.createdAt)}</span>
        <div className="flex gap-2">
          <Button size="sm" variant="outline">
            <XCircle className="h-4 w-4 mr-1" />
            Reject
          </Button>
          <Button size="sm">Approve</Button>
        </div>
      </div>
    </div>
  )
}
