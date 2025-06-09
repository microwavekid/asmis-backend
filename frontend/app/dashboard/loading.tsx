import { Skeleton } from "@/components/ui/skeleton"
import { Header } from "@/components/layout/header"

export default function DashboardLoading() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header title="Dashboard" />
      <main className="flex-1 p-6">
        <Skeleton className="h-9 w-64 mb-6" />

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <div className="col-span-full lg:col-span-2">
            <Skeleton className="h-[400px] w-full rounded-xl" />
          </div>
          <div className="col-span-full lg:col-span-1">
            <Skeleton className="h-[400px] w-full rounded-xl" />
          </div>
          <div className="col-span-full lg:col-span-2">
            <Skeleton className="h-[400px] w-full rounded-xl" />
          </div>
          <div className="col-span-full lg:col-span-1">
            <Skeleton className="h-[400px] w-full rounded-xl" />
          </div>
          <div className="col-span-full">
            <Skeleton className="h-[400px] w-full rounded-xl" />
          </div>
        </div>
      </main>
    </div>
  )
}
