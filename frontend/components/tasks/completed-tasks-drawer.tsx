"use client"

import { useState } from "react"
import type { AITask } from "@/lib/mock-suggestions"
import { Button } from "@/components/ui/button"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { CheckCircle, ChevronDown, ChevronUp, FolderOpen } from "lucide-react"

interface CompletedTasksDrawerProps {
  completedTasks: AITask[]
  onViewTaskDetails: (task: AITask) => void
}

export function CompletedTasksDrawer({ completedTasks, onViewTaskDetails }: CompletedTasksDrawerProps) {
  const [isOpen, setIsOpen] = useState(false)

  if (completedTasks.length === 0) {
    return null
  }

  return (
    <Collapsible open={isOpen} onOpenChange={setIsOpen} className="border rounded-md mt-8 bg-muted/30">
      <CollapsibleTrigger asChild>
        <Button variant="ghost" className="flex w-full justify-between p-4 h-auto hover:bg-muted/50 transition-colors">
          <div className="flex items-center">
            <FolderOpen className="h-5 w-5 mr-2 text-muted-foreground" />
            <span className="font-medium">Completed Tasks ({completedTasks.length})</span>
          </div>
          <div className="flex items-center text-sm text-muted-foreground">
            {isOpen ? "Collapse" : "Expand"}
            {isOpen ? <ChevronUp className="h-5 w-5 ml-1" /> : <ChevronDown className="h-5 w-5 ml-1" />}
          </div>
        </Button>
      </CollapsibleTrigger>

      <CollapsibleContent className="data-[state=open]:animate-collapsible-down data-[state=closed]:animate-collapsible-up">
        <div className="p-4 pt-0">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-[50px]"></TableHead>
                <TableHead>Task</TableHead>
                <TableHead className="w-[200px]">Completed On</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {completedTasks.map((task) => (
                <TableRow key={task.id} className="hover:bg-muted/50">
                  <TableCell className="py-2">
                    <CheckCircle className="h-5 w-5 text-green-500" />
                  </TableCell>
                  <TableCell className="py-2">
                    <div
                      className="font-medium cursor-pointer hover:text-primary"
                      onClick={() => onViewTaskDetails(task)}
                    >
                      {task.title}
                    </div>
                  </TableCell>
                  <TableCell className="py-2 text-muted-foreground">{new Date().toLocaleDateString()}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      </CollapsibleContent>
    </Collapsible>
  )
}
