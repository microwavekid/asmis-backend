import { Skeleton } from "@/components/ui/skeleton"

export default function Loading() {
  return (
    <div className="flex flex-col h-screen">
      <div className="h-16 border-b px-6 flex items-center">
        <Skeleton className="h-8 w-64" />
      </div>
      <div className="flex-1 p-6 overflow-hidden">
        <div className="flex justify-between items-center mb-6">
          <Skeleton className="h-10 w-64" />
          <Skeleton className="h-10 w-96" />
        </div>
        <div className="grid grid-cols-3 gap-6 h-[calc(100vh-12rem)]">
          {Array(3)
            .fill(0)
            .map((_, i) => (
              <div key={i} className="flex flex-col h-full">
                <div className="flex items-center justify-between mb-4">
                  <Skeleton className="h-6 w-40" />
                  <Skeleton className="h-6 w-10" />
                </div>
                <div className="flex-1 bg-muted/30 rounded-lg p-4 space-y-4">
                  {Array(4)
                    .fill(0)
                    .map((_, j) => (
                      <Skeleton key={j} className="h-40 w-full rounded-lg" />
                    ))}
                </div>
              </div>
            ))}
        </div>
      </div>
    </div>
  )
}
