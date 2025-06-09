import { Header } from "@/components/layout/header"
import { Skeleton } from "@/components/ui/skeleton"
import { Card, CardContent, CardHeader } from "@/components/ui/card"

export default function SuggestionsLoading() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header title="AI Suggestions" />
      <main className="flex-1 p-6">
        <div className="mb-6">
          <Skeleton className="h-8 w-64 mb-2" />
          <Skeleton className="h-4 w-96" />
        </div>

        <div className="mb-6">
          <Skeleton className="h-10 w-64" />
        </div>

        <div className="space-y-6">
          {Array(4)
            .fill(0)
            .map((_, i) => (
              <Card key={i}>
                <CardHeader>
                  <div className="flex justify-between">
                    <Skeleton className="h-6 w-48 mb-2" />
                    <Skeleton className="h-6 w-10" />
                  </div>
                  <Skeleton className="h-4 w-64" />
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                    {Array(4)
                      .fill(0)
                      .map((_, j) => (
                        <div key={j} className="border rounded-lg p-3">
                          <div className="flex justify-between mb-2">
                            <Skeleton className="h-5 w-3/4" />
                            <Skeleton className="h-5 w-10" />
                          </div>
                          <Skeleton className="h-4 w-full mb-3" />
                          <div className="flex justify-between gap-2">
                            <Skeleton className="h-8 w-1/2" />
                            <Skeleton className="h-8 w-1/2" />
                          </div>
                        </div>
                      ))}
                  </div>
                </CardContent>
              </Card>
            ))}
        </div>
      </main>
    </div>
  )
}
