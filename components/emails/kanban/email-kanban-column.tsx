import type { ReactNode } from "react"
import type { DroppableProvided } from "@hello-pangea/dnd"
import { cn } from "@/lib/utils"

interface EmailKanbanColumnProps {
  title: string
  count: number
  children: ReactNode
  provided: DroppableProvided
  className?: string
  titleClassName?: string
}

export function EmailKanbanColumn({
  title,
  count,
  children,
  provided,
  className,
  titleClassName,
}: EmailKanbanColumnProps) {
  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between mb-4">
        <h2 className={cn("text-lg font-semibold", titleClassName)}>{title}</h2>
        <span className="text-sm font-medium bg-background rounded-full px-2 py-0.5">{count}</span>
      </div>
      <div
        ref={provided.innerRef}
        {...provided.droppableProps}
        className={cn("flex-1 rounded-lg border p-4 overflow-y-auto space-y-4", className)}
      >
        {children}
        {provided.placeholder}
      </div>
    </div>
  )
}
